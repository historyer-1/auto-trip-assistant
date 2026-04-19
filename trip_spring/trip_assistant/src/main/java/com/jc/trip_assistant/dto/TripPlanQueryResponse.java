package com.jc.trip_assistant.dto;

import com.jc.trip_assistant.entity.TripPlan;

/**
 * 查询行程计划的响应实体。
 */
public class TripPlanQueryResponse {

    /**
     * 请求唯一ID。
     */
    private String requestId;

    /**
     * 处理状态。
     */
    private String status;

    /**
     * 失败原因。
     */
    private String errorMessage;

    /**
     * 行程计划结果。
     */
    private TripPlan tripPlan;

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
     * 获取行程计划结果。
     *
     * @param 无
     * @return 行程计划结果
     */
    public TripPlan getTripPlan() {
        return tripPlan;
    }

    /**
     * 设置行程计划结果。
     *
     * @param tripPlan 行程计划结果
     * @return 无
     */
    public void setTripPlan(TripPlan tripPlan) {
        this.tripPlan = tripPlan;
    }
}
