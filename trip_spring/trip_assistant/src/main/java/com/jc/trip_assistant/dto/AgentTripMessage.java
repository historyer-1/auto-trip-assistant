package com.jc.trip_assistant.dto;

import com.jc.trip_assistant.entity.TripRequest;

/**
 * Kafka中传输的行程任务消息实体。
 */
public class AgentTripMessage {

    /**
     * 用户ID。
     */
    private Long userId;

    /**
     * 请求唯一ID。
     */
    private String requestId;

    /**
     * 行程请求体。
     */
    private TripRequest tripRequest;

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
     * 获取行程请求体。
     *
     * @param 无
     * @return 行程请求体
     */
    public TripRequest getTripRequest() {
        return tripRequest;
    }

    /**
     * 设置行程请求体。
     *
     * @param tripRequest 行程请求体
     * @return 无
     */
    public void setTripRequest(TripRequest tripRequest) {
        this.tripRequest = tripRequest;
    }
}
