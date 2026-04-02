package com.jc.trip_assistant.controller;

import com.jc.trip_assistant.common.Result;
import com.jc.trip_assistant.common.UserHolder;
import com.jc.trip_assistant.dto.LoginRequest;
import com.jc.trip_assistant.dto.LoginResponse;
import com.jc.trip_assistant.dto.SendCodeRequest;
import com.jc.trip_assistant.dto.UserDTO;
import com.jc.trip_assistant.service.LoginService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import lombok.extern.slf4j.Slf4j;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.HashMap;
import java.util.Map;

/**
 * 登录控制器，统一接收登录模块相关请求。
 */
@Slf4j
@Controller
public class LoginController {

    /**
     * 登录业务服务对象。
     */
    private final LoginService loginService;

    /**
     * 构造函数，注入登录业务服务。
     *
     * @param loginService 登录业务服务对象
     * @return 无
     */
    public LoginController(LoginService loginService) {
        this.loginService = loginService;
    }

    /**
     * 首页入口，重定向到登录页。
     *
     * @param 无
     * @return 登录页重定向地址
     */
    @GetMapping("/")
    public String index() {
        // 入口页面统一跳转至登录页面。
        return "redirect:/login";
    }

    /**
     * 登录页面路由。
     *
     * @param 无
     * @return 登录模板名称
     */
    @GetMapping("/login")
    public String login() {
        // 返回登录页面模板。
        return "login";
    }

    /**
     * 看板页面路由。
     *
     * @param 无
     * @return 看板模板名称
     */
    @GetMapping("/trip/dashboard")
    public String dashboard() {
        // 返回行程看板页面模板。
        return "dashboard";
    }

    /**
     * 发送邮箱验证码接口。
     *
     * @param request 发送验证码请求参数
     * @return 统一响应结果
     */
    @PostMapping("/api/auth/send-code")
    @ResponseBody
    public Result<Object> sendCode(@RequestBody SendCodeRequest request) {
        // Controller 只负责透传请求参数与返回结果。
        return loginService.sendCode(request.getEmail());
    }

    /**
     * 邮箱验证码登录接口。
     *
     * @param request 登录请求参数
     * @return 统一响应结果
     */
    @PostMapping("/api/auth/login")
    @ResponseBody
    public Result<LoginResponse> authLogin(@Valid @RequestBody LoginRequest request) {
        // Controller 只负责透传请求参数与返回结果。
        return loginService.login(request);
    }

    /**
     * 查询当前登录用户接口。
     *
     * @param request HTTP请求对象
     * @return 统一响应结果
     */
    @GetMapping("/api/auth/me")
    @ResponseBody
    public Result<Map<String, Object>> me(HttpServletRequest request) {
        // 从ThreadLocal中获取当前登录用户，减少重复解析token的开销。
        UserDTO currentUser = UserHolder.getUser();
        if (currentUser == null) {
            return Result.fail(401, "请先登录");
        }

        // 返回前端展示所需的基础用户信息。
        Map<String, Object> data = new HashMap<>();
        data.put("userId", currentUser.getUserId());
        data.put("email", currentUser.getEmail());
        data.put("nickname", currentUser.getNickname());
        return Result.success(data);
    }

    /**
     * 退出登录接口。
     *
     * @param request HTTP请求对象
     * @return 统一响应结果
     */
    @PostMapping("/api/auth/logout")
    @ResponseBody
    public Result<Object> logout(HttpServletRequest request) {
        // 提取token后交由Service清理Redis登录态。
        String token = extractBearerToken(request);
        return loginService.logout(token);
    }

    /**
     * 从请求头提取Bearer令牌。
     *
     * @param request HTTP请求对象
     * @return JWT令牌字符串
     */
    private String extractBearerToken(HttpServletRequest request) {
        // 读取Authorization请求头并校验Bearer前缀。
        String authorization = request.getHeader("Authorization");
        if (authorization == null || !authorization.startsWith("Bearer ")) {
            throw new IllegalArgumentException("缺少有效的Authorization令牌");
        }

        // 去除Bearer前缀并返回纯令牌内容。
        String token = authorization.substring(7).trim();
        if (token.isEmpty()) {
            throw new IllegalArgumentException("令牌不能为空");
        }
        return token;
    }
}

