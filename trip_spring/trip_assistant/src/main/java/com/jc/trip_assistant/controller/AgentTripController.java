package com.jc.trip_assistant.controller;

import com.jc.trip_assistant.common.Result;
import com.jc.trip_assistant.common.UserHolder;
import com.jc.trip_assistant.dto.TripPlanQueryResponse;
import com.jc.trip_assistant.entity.TripPlan;
import com.jc.trip_assistant.entity.TripRequest;
import com.jc.trip_assistant.service.AgentTripService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * Agent行程控制器，仅负责请求接收和服务返回透传。
 */
@RestController
@RequestMapping("/api/agent")
public class AgentTripController {

    /**
     * Agent行程服务。
     */
    private final AgentTripService agentTripService;

    /**
     * 构造函数，注入Agent行程服务。
     *
     * @param agentTripService Agent行程服务
     * @return 无
     */
    public AgentTripController(AgentTripService agentTripService) {
        this.agentTripService = agentTripService;
    }

    /**
     * 提交行程规划请求。
     *
     * @param request 行程请求参数
     * @return 请求唯一ID
     */
    @PostMapping("/trip/submit")
    public Result<String> submitTripRequest(@Valid @RequestBody TripRequest request) {
        // Controller只做参数接收和透传，不加入额外业务逻辑。
        Long userId = UserHolder.getUser().getUserId();
        return agentTripService.submitTripRequest(userId, request);
    }

    /**
     * 查询某次行程请求结果。
     *
     * @param requestId 请求唯一ID
     * @return 行程查询结果
     */
    @GetMapping("/trip/query")
    public Result<TripPlanQueryResponse> queryTripPlan(@RequestParam("requestId") String requestId) {
        // Controller只做参数接收和透传，不加入额外业务逻辑。
        Long userId = UserHolder.getUser().getUserId();
        return agentTripService.queryTripPlan(userId, requestId);
    }

    /**
     * 分页查询当前用户历史行程计划列表。
     *
     * @param page 页码，从1开始
     * @param size 每页条数
     * @return TripPlan列表
     */
    @GetMapping("/trip/plans")
    public Result<List<TripPlan>> listCurrentUserTripPlans(@RequestParam(value = "page", defaultValue = "1") Integer page,
                                                           @RequestParam(value = "size", defaultValue = "10") Integer size) {
        // Controller只做参数接收和透传，不加入额外业务逻辑。
        Long userId = UserHolder.getUser().getUserId();
        return agentTripService.listCurrentUserTripPlans(userId, page, size);
    }
}
