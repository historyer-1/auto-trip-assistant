package com.jc.trip_assistant.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;

/**
 * 发送验证码请求参数对象。
 */
public class SendCodeRequest {

    /**
     * 登录邮箱。
     */
    @NotBlank(message = "邮箱不能为空")
    @Email(message = "邮箱格式不正确")
    private String email;

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
}
