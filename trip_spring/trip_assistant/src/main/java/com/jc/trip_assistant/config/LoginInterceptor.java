package com.jc.trip_assistant.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.jc.trip_assistant.common.Result;
import com.jc.trip_assistant.common.UserHolder;
import com.jc.trip_assistant.dto.UserDTO;
import com.jc.trip_assistant.util.JwtUtil;
import io.jsonwebtoken.Claims;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

import java.nio.charset.StandardCharsets;

/**
 * 登录拦截器，校验除登录接口外的请求是否携带并通过JWT令牌验证。
 */
@Component
public class LoginInterceptor implements HandlerInterceptor {

    /**
     * 令牌Redis键前缀。
     */
    private static final String TOKEN_KEY_PREFIX = "auth:token:";

    /**
     * JWT工具对象。
     */
    private final JwtUtil jwtUtil;

    /**
     * Redis操作模板。
     */
    private final StringRedisTemplate stringRedisTemplate;

    /**
     * JSON序列化工具。
     */
    private final ObjectMapper objectMapper;

    /**
     * 构造函数，注入依赖组件。
     *
     * @param jwtUtil JWT工具对象
     * @param stringRedisTemplate Redis操作模板
     * @param objectMapper JSON序列化工具
     * @return 无
     */
    public LoginInterceptor(JwtUtil jwtUtil,
                            StringRedisTemplate stringRedisTemplate,
                            ObjectMapper objectMapper) {
        this.jwtUtil = jwtUtil;
        this.stringRedisTemplate = stringRedisTemplate;
        this.objectMapper = objectMapper;
    }

    /**
     * 请求前置处理，校验JWT令牌并判断会话是否有效。
     *
     * @param request HTTP请求对象
     * @param response HTTP响应对象
     * @param handler 目标处理器
     * @return true表示放行，false表示拦截
     * @throws Exception 处理异常
     */
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        // 从请求头读取Authorization，并直接提取token。
        String authHeader = request.getHeader("Authorization");
        if (authHeader == null || authHeader.isBlank()) {
            writeUnauthorized(response, "缺少有效的Authorization令牌");
            return false;
        }
        String token = authHeader.trim();
        if (token.isEmpty()) {
            writeUnauthorized(response, "令牌不能为空");
            return false;
        }


            // 解析JWT并校验签名、过期时间等基础合法性。
            Claims claims = jwtUtil.parseToken(token);

            // 二次校验Redis会话是否存在，支持服务端主动失效控制。
            String tokenRedisKey = TOKEN_KEY_PREFIX + token;
            String cacheValue = stringRedisTemplate.opsForValue().get(tokenRedisKey);
            if (cacheValue == null) {
                writeUnauthorized(response, "登录已失效，请重新登录");
                return false;
            }

            // 将JWT中的用户信息转换为UserDTO，并保存到ThreadLocal供后续业务使用。
            UserDTO userDTO = new UserDTO();
            userDTO.setUserId(Long.valueOf(String.valueOf(claims.get("userId"))));
            userDTO.setEmail(String.valueOf(claims.get("email")));
            userDTO.setNickname(String.valueOf(claims.get("nickname")));
            UserHolder.setUser(userDTO);

            // 同时把令牌和用户信息放到请求属性，方便特定场景临时读取。
            request.setAttribute("currentUserId", userDTO.getUserId());
            request.setAttribute("currentUserEmail", userDTO.getEmail());
            request.setAttribute("currentUserNickname", userDTO.getNickname());
            return true;
 
        
    }

    /**
     * 请求完成后清理ThreadLocal中的用户信息。
     *
     * @param request HTTP请求对象
     * @param response HTTP响应对象
     * @param handler 目标处理器
     * @param ex 请求执行过程中产生的异常
     * @return 无
     */
    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) {
        // 请求结束后及时清理用户上下文，避免线程复用引发数据污染。
        UserHolder.removeUser();
    }

    /**
     * 写出未授权响应。
     *
     * @param response HTTP响应对象
     * @param message 错误提示信息
     * @return 无
     * @throws Exception 写响应异常
     */
    private void writeUnauthorized(HttpServletResponse response, String message) throws Exception {
        // 统一返回Result结构，便于前端一致处理401状态。
        response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
        response.setCharacterEncoding(StandardCharsets.UTF_8.name());
        response.setContentType(MediaType.APPLICATION_JSON_VALUE);
        String body = objectMapper.writeValueAsString(Result.fail(401, message));
        response.getWriter().write(body);
    }
}
