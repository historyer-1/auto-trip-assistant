package com.jc.trip_assistant.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;

/**
 * 登录请求参数对象。
 */
public class LoginRequest {

    /**
     * 登录邮箱。
     */
    @NotBlank(message = "邮箱不能为空")
    @Email(message = "邮箱格式不正确")
    private String email;

    /**
     * 邮箱验证码。
     */
    @NotBlank(message = "验证码不能为空")
    @Pattern(regexp = "\\d{6}", message = "验证码必须为6位数字")
    private String code;

    /**
     * 获取登录邮箱。
     *
     * @param 无
     * @return 登录邮箱
     */
    public String getEmail() {
        return email;
    }

    /**
     * 设置登录邮箱。
     *
     * @param email 登录邮箱
     * @return 无
     */
    public void setEmail(String email) {
        this.email = email;
    }

    /**
     * 获取验证码。
     *
     * @param 无
     * @return 验证码
     */
    public String getCode() {
        return code;
    }

    /**
     * 设置验证码。
     *
     * @param code 验证码
     * @return 无
     */
    public void setCode(String code) {
        this.code = code;
    }
}
