package com.jc.trip_assistant.entity;

import java.time.LocalDateTime;

/**
 * 用户实体类，对应数据库中的t_user表。
 */
public class User {

    /**
     * 用户主键ID。
     */
    private Long id;

    /**
     * 用户登录邮箱。
     */
    private String email;

    /**
     * 用户昵称。
     */
    private String nickname;

    /**
     * 用户创建时间。
     */
    private LocalDateTime createTime;

    /**
     * 用户更新时间。
     */
    private LocalDateTime updateTime;

    /**
     * 获取用户主键ID。
     *
     * @param 无
     * @return 用户主键ID
     */
    public Long getId() {
        return id;
    }

    /**
     * 设置用户主键ID。
     *
     * @param id 用户主键ID
     * @return 无
     */
    public void setId(Long id) {
        this.id = id;
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

    /**
     * 获取用户创建时间。
     *
     * @param 无
     * @return 用户创建时间
     */
    public LocalDateTime getCreateTime() {
        return createTime;
    }

    /**
     * 设置用户创建时间。
     *
     * @param createTime 用户创建时间
     * @return 无
     */
    public void setCreateTime(LocalDateTime createTime) {
        this.createTime = createTime;
    }

    /**
     * 获取用户更新时间。
     *
     * @param 无
     * @return 用户更新时间
     */
    public LocalDateTime getUpdateTime() {
        return updateTime;
    }

    /**
     * 设置用户更新时间。
     *
     * @param updateTime 用户更新时间
     * @return 无
     */
    public void setUpdateTime(LocalDateTime updateTime) {
        this.updateTime = updateTime;
    }
}
