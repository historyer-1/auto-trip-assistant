package com.jc.trip_assistant.dto;

/**
 * 登录响应对象，返回JWT与基础用户信息。
 */
public class LoginResponse {

    /**
     * JWT令牌。
     */
    private String token;

    /**
     * 用户主键ID。
     */
    private Long userId;

    /**
     * 用户邮箱。
     */
    private String email;

    /**
     * 用户昵称。
     */
    private String nickname;

    /**
     * 获取JWT令牌。
     *
     * @param 无
     * @return JWT令牌
     */
    public String getToken() {
        return token;
    }

    /**
     * 设置JWT令牌。
     *
     * @param token JWT令牌
     * @return 无
     */
    public void setToken(String token) {
        this.token = token;
    }

    /**
     * 获取用户主键ID。
     *
     * @param 无
     * @return 用户主键ID
     */
    public Long getUserId() {
        return userId;
    }

    /**
     * 设置用户主键ID。
     *
     * @param userId 用户主键ID
     * @return 无
     */
    public void setUserId(Long userId) {
        this.userId = userId;
    }

    /**
     * 获取用户邮箱。
     *
     * @param 无
     * @return 用户邮箱
     */
    public String getEmail() {
        return email;
    }

    /**
     * 设置用户邮箱。
     *
     * @param email 用户邮箱
     * @return 无
     */
    public void setEmail(String email) {
        this.email = email;
    }

    /**
     * 获取用户昵称。
     *
     * @param 无
     * @return 用户昵称
     */
    public String getNickname() {
        return nickname;
    }

    /**
     * 设置用户昵称。
     *
     * @param nickname 用户昵称
     * @return 无
     */
    public void setNickname(String nickname) {
        this.nickname = nickname;
    }
}
