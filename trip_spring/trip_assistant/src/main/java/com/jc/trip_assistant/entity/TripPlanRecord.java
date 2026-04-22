package com.jc.trip_assistant.entity;

import java.time.LocalDateTime;

/**
 * 行程计划数据库实体，对应t_trip_plan表。
 */
public class TripPlanRecord {

    /**
     * 主键ID。
     */
    private Long id;

    /**
     * 用户ID。
     */
    private Long userId;

    /**
     * 请求唯一ID。
     */
    private String requestId;

    /**
     * 原始请求JSON。
     */
    private String requestJson;

    /**
     * 生成结果JSON。
     */
    private String planJson;

    /**
     * 处理状态。
     */
    private String status;

    /**
     * 重试次数。
     */
    private Integer retryCount;

    /**
     * 失败原因。
     */
    private String errorMessage;

    /**
     * 创建时间。
     */
    private LocalDateTime createTime;

    /**
     * 更新时间。
     */
    private LocalDateTime updateTime;

    /**
     * 获取主键ID。
     *
     * @param 无
     * @return 主键ID
     */
    public Long getId() {
        return id;
    }

    /**
     * 设置主键ID。
     *
     * @param id 主键ID
     * @return 无
     */
    public void setId(Long id) {
        this.id = id;
    }

    /**
     * 获取用户ID。
     *
     * @param 无
     * @return 用户ID
     */
    public Long getUserId() {
        return userId;
    }

    /**
     * 设置用户ID。
     *
     * @param userId 用户ID
     * @return 无
     */
    public void setUserId(Long userId) {
        this.userId = userId;
    }

    /**
     * 获取请求唯一ID。
     *
     * @param 无
     * @return 请求唯一ID
     */
    public String getRequestId() {
        return requestId;
    }

    /**
     * 设置请求唯一ID。
     *
     * @param requestId 请求唯一ID
     * @return 无
     */
    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }

    /**
     * 获取原始请求JSON。
     *
     * @param 无
     * @return 原始请求JSON
     */
    public String getRequestJson() {
        return requestJson;
    }

    /**
     * 设置原始请求JSON。
     *
     * @param requestJson 原始请求JSON
     * @return 无
     */
    public void setRequestJson(String requestJson) {
        this.requestJson = requestJson;
    }

    /**
     * 获取生成结果JSON。
     *
     * @param 无
     * @return 生成结果JSON
     */
    public String getPlanJson() {
        return planJson;
    }

    /**
     * 设置生成结果JSON。
     *
     * @param planJson 生成结果JSON
     * @return 无
     */
    public void setPlanJson(String planJson) {
        this.planJson = planJson;
    }

    /**
     * 获取处理状态。
     *
     * @param 无
     * @return 处理状态
     */
    public String getStatus() {
        return status;
    }

    /**
     * 设置处理状态。
     *
     * @param status 处理状态
     * @return 无
     */
    public void setStatus(String status) {
        this.status = status;
    }

    /**
     * 获取重试次数。
     *
     * @param 无
     * @return 重试次数
     */
    public Integer getRetryCount() {
        return retryCount;
    }

    /**
     * 设置重试次数。
     *
     * @param retryCount 重试次数
     * @return 无
     */
    public void setRetryCount(Integer retryCount) {
        this.retryCount = retryCount;
    }

    /**
     * 获取失败原因。
     *
     * @param 无
     * @return 失败原因
     */
    public String getErrorMessage() {
        return errorMessage;
    }

    /**
     * 设置失败原因。
     *
     * @param errorMessage 失败原因
     * @return 无
     */
    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }

    /**
     * 获取创建时间。
     *
     * @param 无
     * @return 创建时间
     */
    public LocalDateTime getCreateTime() {
        return createTime;
    }

    /**
     * 设置创建时间。
     *
     * @param createTime 创建时间
     * @return 无
     */
    public void setCreateTime(LocalDateTime createTime) {
        this.createTime = createTime;
    }

    /**
     * 获取更新时间。
     *
     * @param 无
     * @return 更新时间
     */
    public LocalDateTime getUpdateTime() {
        return updateTime;
    }

    /**
     * 设置更新时间。
     *
     * @param updateTime 更新时间
     * @return 无
     */
    public void setUpdateTime(LocalDateTime updateTime) {
        this.updateTime = updateTime;
    }
}
