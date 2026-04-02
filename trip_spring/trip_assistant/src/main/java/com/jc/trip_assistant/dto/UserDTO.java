package com.jc.trip_assistant.dto;

/**
 * 当前登录用户的数据传输对象，仅保存非敏感信息。
 */
public class UserDTO {

    /**
     * 用户主键ID。
     */
    private Long userId;

    /**
     * 用户登录邮箱。
     */
    private String email;

    /**
     * 用户昵称。
     */
    private String nickname;

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
     * 获取用户登录邮箱。
     *
     * @param 无
     * @return 用户登录邮箱
     */
    public String getEmail() {
        return email;
    }

    /**
     * 设置用户登录邮箱。
     *
     * @param email 用户登录邮箱
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
