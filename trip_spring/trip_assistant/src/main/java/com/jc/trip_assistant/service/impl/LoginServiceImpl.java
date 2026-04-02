package com.jc.trip_assistant.service.impl;

import com.jc.trip_assistant.common.Result;
import com.jc.trip_assistant.dao.UserDao;
import com.jc.trip_assistant.dto.LoginRequest;
import com.jc.trip_assistant.dto.LoginResponse;
import com.jc.trip_assistant.entity.Mail;
import com.jc.trip_assistant.entity.User;
import com.jc.trip_assistant.service.LoginService;
import com.jc.trip_assistant.util.JwtUtil;
import com.jc.trip_assistant.util.MailUtil;
import jakarta.mail.MessagingException;
import jakarta.mail.internet.MimeMessage;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Service;
import lombok.extern.slf4j.Slf4j;

import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ThreadLocalRandom;

/**
 * 登录服务实现类，承接验证码、用户注册登录、JWT签发与Redis会话管理。
 */
@Service
@Slf4j
public class LoginServiceImpl implements LoginService {

    /**
     * 验证码Redis键前缀。
     */
    private static final String CODE_KEY_PREFIX = "auth:code:";

    /**
     * JWT Redis键前缀。
     */
    private static final String TOKEN_KEY_PREFIX = "auth:token:";

    /**
     * 验证码过期时间。
     */
    private static final Duration CODE_TTL = Duration.ofMinutes(3);

    /**
     * 登录令牌过期时间。
     */
    private static final Duration TOKEN_TTL = Duration.ofMinutes(30);

    /**
     * 用户数据访问对象。
     */
    private final UserDao userDao;

    /**
     * Redis操作模板。
     */
    private final StringRedisTemplate stringRedisTemplate;

    /**
     * 邮件发送器。
     */
    private final JavaMailSender javaMailSender;

    /**
     * JWT工具对象。
     */
    private final JwtUtil jwtUtil;

    /**
     * 发件邮箱地址。
     */
    @Value("${spring.mail.username}")
    private String fromEmail;

    @Autowired
    private MailUtil mailUtil;
    @Autowired
    private Mail mail;

    /**
     * 构造函数，注入依赖组件。
     *
     * @param userDao 用户数据访问对象
     * @param stringRedisTemplate Redis操作模板
     * @param javaMailSender 邮件发送器
     * @param jwtUtil JWT工具对象
     * @return 无
     */
    public LoginServiceImpl(UserDao userDao,
                            StringRedisTemplate stringRedisTemplate,
                            JavaMailSender javaMailSender,
                            JwtUtil jwtUtil) {
        this.userDao = userDao;
        this.stringRedisTemplate = stringRedisTemplate;
        this.javaMailSender = javaMailSender;
        this.jwtUtil = jwtUtil;
    }

    /**
     * 发送邮箱验证码并缓存到Redis。
     *
     * @param email 登录邮箱
     * @return 发送后的提示信息
     */
    @Override
    public Result<Object> sendCode(String email) {
        // 邮箱格式校验，格式不对直接返回fail。
        if (email == null || !email.matches("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+$")) {
            return Result.fail("邮箱格式不正确");
        }
        // 生成6位随机验证码，并写入Redis做短期校验。
        String code = String.format("%06d", ThreadLocalRandom.current().nextInt(1000000));
        String codeRedisKey = buildCodeKey(email);
        stringRedisTemplate.opsForValue().set(codeRedisKey, code, CODE_TTL);

        // 输出日志便于开发调试验证码流程。
        log.info("邮箱验证码已生成，email={}, code={}", email, code);

        // 调用邮件组件发送验证码给用户邮箱。
        boolean success = sendMail(email, code);
        if (!success) {
            return Result.fail("邮件发送失败");
        }
        return Result.success("邮件发送成功");
    }

    /**
     * 校验验证码并完成登录，返回JWT令牌。
     *
     * @param request 登录请求参数
     * @return 登录响应数据
     */
    @Override
    public Result<LoginResponse> login(LoginRequest request) {
        String email = request.getEmail().trim();
        String code = request.getCode().trim();

        // 从Redis读取验证码并执行匹配校验。
        String cachedCode = stringRedisTemplate.opsForValue().get(buildCodeKey(email));
        if (cachedCode == null || !cachedCode.equals(code)) {
            return Result.fail("验证码错误或已过期");
        }

        // 校验通过后查询用户，不存在则自动注册。
        User user = userDao.findByEmail(email);
        if (user == null) {
            user = createUser(email);
            if (user == null) {
                return Result.fail("创建用户失败");
            }
        }

        // 构建JWT声明并签发令牌。
        Map<String, Object> claims = new HashMap<>();
        claims.put("userId", user.getId());
        claims.put("email", user.getEmail());
        claims.put("nickname", user.getNickname());
        String token = jwtUtil.generateToken(claims);

        // 将令牌写入Redis用于服务端会话校验，并设置30分钟过期。
        stringRedisTemplate.opsForValue().set(buildTokenKey(token), String.valueOf(user.getId()), TOKEN_TTL);

        // 登录成功后删除验证码，避免验证码重复使用。
        stringRedisTemplate.delete(buildCodeKey(email));

        // 组装登录响应对象返回给前端。
        LoginResponse response = new LoginResponse();
        response.setToken(token);
        response.setUserId(user.getId());
        response.setEmail(user.getEmail());
        response.setNickname(user.getNickname());
        return Result.success("登录成功", response);
    }

    /**
     * 执行用户退出登录逻辑。
     *
     * @param token JWT令牌
     * @return 退出提示信息
     */
    @Override
    public Result<Object> logout(String token) {
        if (token == null || token.isBlank()) {
            return Result.fail("令牌不能为空");
        }
        // 删除Redis中的会话令牌，立即使token失效。
        stringRedisTemplate.delete(buildTokenKey(token));
        return Result.success("退出登录成功");
    }

    /**
     * 发送验证码邮件。
     *
     * @param email 收件邮箱
     * @param code 验证码
     * @return 无
     */
    private Boolean sendMail(String email, String code) {

        // 构建包含验证码信息的HTML邮件正文。
        String content = "您好，您的登录验证码为：" + code
                + "\n验证码3分钟内有效，请勿泄露给他人。";

        // 创建MimeMessage对象并使用MimeMessageHelper设置邮件属性。
        mail.setRecipient(email);
        mail.setSubject("验证码测试");
        mail.setContent(content);

        // 执行邮件发送。
        return mailUtil.sendSimpleMail(mail);
    }
    /**
     * 创建新用户。
     *
     * @param email 登录邮箱
     * @return 新创建的用户对象
     */
    private User createUser(String email) {
        // 初始化用户基本信息，并生成默认昵称。
        User user = new User();
        user.setEmail(email);
        user.setNickname("用户" + UUID.randomUUID().toString().replace("-", "").substring(0, 6));

        // 写入数据库并校验写入结果。
        int rows = userDao.insert(user);
        if (rows <= 0 || user.getId() == null) {
            return null;
        }
        return user;
    }

    /**
     * 构建验证码Redis键。
     *
     * @param email 登录邮箱
     * @return 验证码Redis键
     */
    private String buildCodeKey(String email) {
        // 将邮箱统一转为小写，避免同一邮箱大小写差异导致缓存不一致。
        return CODE_KEY_PREFIX + email.toLowerCase();
    }

    /**
     * 构建令牌Redis键。
     *
     * @param token JWT令牌
     * @return 令牌Redis键
     */
    private String buildTokenKey(String token) {
        // 对token直接拼接前缀，作为服务端会话唯一键。
        return TOKEN_KEY_PREFIX + token;
    }
}
