package com.jc.trip_assistant.service;

import com.jc.trip_assistant.common.Result;
import com.jc.trip_assistant.dto.TripPlanQueryResponse;
import com.jc.trip_assistant.entity.TripPlan;
import com.jc.trip_assistant.entity.TripRequest;

import java.util.List;

/**
 * Agent行程业务服务接口。
 */
public interface AgentTripService {

    /**
     * 提交用户行程请求到消息队列。
     *
     * @param userId 用户ID
     * @param request 行程请求参数
     * @return 请求唯一ID
     */
    Result<String> submitTripRequest(Long userId, TripRequest request);

    /**
     * 查询用户某次请求的行程结果。
     *
     * @param userId 用户ID
     * @param requestId 请求唯一ID
     * @return 行程查询结果
     */
    Result<TripPlanQueryResponse> queryTripPlan(Long userId, String requestId);

    /**
     * 分页查询当前用户的历史行程计划。
     *
     * @param userId 用户ID
     * @param page 页码，从1开始
     * @param size 每页条数
     * @return TripPlan列表
     */
    Result<List<TripPlan>> listCurrentUserTripPlans(Long userId, Integer page, Integer size);
}
