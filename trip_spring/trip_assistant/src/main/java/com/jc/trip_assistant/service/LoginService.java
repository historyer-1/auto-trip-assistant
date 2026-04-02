package com.jc.trip_assistant.service;

import com.jc.trip_assistant.common.Result;
import com.jc.trip_assistant.dto.LoginRequest;
import com.jc.trip_assistant.dto.LoginResponse;

/**
 * 登录业务服务接口，封装验证码登录相关核心逻辑。
 */
public interface LoginService {

    /**
     * 发送邮箱验证码并缓存到Redis。
     *
     * @param email 登录邮箱
     * @return 发送后的提示信息
     */
    Result<Object> sendCode(String email);

    /**
     * 校验验证码并完成登录，返回JWT令牌。
     *
     * @param request 登录请求参数
     * @return 登录响应数据
     */
    Result<LoginResponse> login(LoginRequest request);

    /**
     * 执行用户退出登录逻辑。
     *
     * @param token JWT令牌
     * @return 退出提示信息
     */
    Result<Object> logout(String token);
}
