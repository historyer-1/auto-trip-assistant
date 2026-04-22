package com.jc.trip_assistant.service.impl;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.jc.trip_assistant.common.Result;
import com.jc.trip_assistant.dao.TripPlanDao;
import com.jc.trip_assistant.dto.AgentTripMessage;
import com.jc.trip_assistant.dto.TripPlanQueryResponse;
import com.jc.trip_assistant.entity.TripPlan;
import com.jc.trip_assistant.entity.TripPlanRecord;
import com.jc.trip_assistant.entity.TripRequest;
import com.jc.trip_assistant.service.AgentTripService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

/**
 * Agent行程服务实现，负责请求入队、消费处理、调用Agent并落库。
 */
@Service
@Slf4j
public class AgentTripServiceImpl implements AgentTripService {

    /**
     * 处理中状态。
     */
    private static final String STATUS_PENDING = "PENDING";

    /**
     * 成功状态。
     */
    private static final String STATUS_SUCCESS = "SUCCESS";

    /**
     * 失败状态。
     */
    private static final String STATUS_FAILED = "FAILED";

    /**
     * 行程结果DAO。
     */
    private final TripPlanDao tripPlanDao;

    /**
     * Kafka消息发送模板。
     */
    private final KafkaTemplate<String, String> kafkaTemplate;

    /**
     * JSON工具。
     */
    private final ObjectMapper objectMapper;

    /**
     * HTTP客户端。
     */
    private final RestTemplate restTemplate;

    /**
     * Kafka主题。
     */
    private final String tripTopic;

    /**
     * Agent服务地址。
     */
    private final String agentServerUrl;

    /**
     * 构造函数，注入依赖。
     *
     * @param tripPlanDao 行程结果DAO
     * @param kafkaTemplate Kafka消息发送模板
     * @param objectMapper JSON工具
     * @param restTemplate HTTP客户端
     * @param tripTopic Kafka主题
     * @param agentServerUrl Agent服务地址
     * @return 无
     */
    public AgentTripServiceImpl(TripPlanDao tripPlanDao,
                                KafkaTemplate<String, String> kafkaTemplate,
                                ObjectMapper objectMapper,
                                RestTemplate restTemplate,
                                @Value("${trip.kafka.topic}") String tripTopic,
                                @Value("${trip.agent.server-url}") String agentServerUrl) {
        this.tripPlanDao = tripPlanDao;
        this.kafkaTemplate = kafkaTemplate;
        this.objectMapper = objectMapper;
        this.restTemplate = restTemplate;
        this.tripTopic = tripTopic;
        this.agentServerUrl = agentServerUrl;
    }

    /**
     * 提交用户行程请求到消息队列。
     *
     * @param userId 用户ID
     * @param request 行程请求参数
     * @return 请求唯一ID
     */
    @Override
    public Result<String> submitTripRequest(Long userId, TripRequest request) {

        String requestId = UUID.randomUUID().toString().replace("-", "");
        try {
            // 先落库PENDING记录，保证请求轨迹可查。
            TripPlanRecord record = new TripPlanRecord();
            record.setUserId(userId);
            record.setRequestId(requestId);
            record.setRequestJson(objectMapper.writeValueAsString(request));
            record.setStatus(STATUS_PENDING);
            record.setRetryCount(0);
            tripPlanDao.insertPending(record);

            // 组装Kafka消息并发送到Topic。
            AgentTripMessage message = new AgentTripMessage();
            message.setUserId(userId);
            message.setRequestId(requestId);
            message.setTripRequest(request);
            kafkaTemplate.send(tripTopic, requestId, objectMapper.writeValueAsString(message));
            return Result.success("请求已进入队列，请稍后查询", requestId);
        } catch (Exception ex) {
            log.error("提交行程请求失败，userId={}, requestId={}", userId, requestId, ex);
            tripPlanDao.updateResult(requestId, STATUS_FAILED, null, "请求入队失败：" + ex.getMessage(), 0);
            return Result.fail(500, "提交请求失败：" + ex.getMessage());
        }
    }

    /**
     * 查询用户某次请求的行程结果。
     *
     * @param userId 用户ID
     * @param requestId 请求唯一ID
     * @return 行程查询结果
     */
    @Override
    public Result<TripPlanQueryResponse> queryTripPlan(Long userId, String requestId) {
        TripPlanRecord record = tripPlanDao.findByUserIdAndRequestId(userId, requestId);
        if (record == null) {
            return Result.fail(404, "未找到对应的行程记录");
        }

        // 封装统一响应，成功时解析TripPlan，失败和处理中返回状态及错误原因。
        TripPlanQueryResponse response = new TripPlanQueryResponse();
        response.setRequestId(record.getRequestId());
        response.setStatus(record.getStatus());
        response.setErrorMessage(record.getErrorMessage());

        if (STATUS_SUCCESS.equals(record.getStatus())
                && record.getPlanJson() != null
                && !record.getPlanJson().isBlank()) {
            try {
                response.setTripPlan(objectMapper.readValue(record.getPlanJson(), TripPlan.class));
            } catch (JsonProcessingException ex) {
                log.error("解析TripPlan失败，requestId={}", requestId, ex);
                return Result.fail(500, "行程结果解析失败：" + ex.getMessage());
            }
        }

        return Result.success(response);
    }

    /**
     * 分页查询当前用户的历史行程计划。
     *
     * @param userId 用户ID
     * @param page 页码，从1开始
     * @param size 每页条数
     * @return TripPlan列表
     */
    @Override
    public Result<List<TripPlan>> listCurrentUserTripPlans(Long userId, Integer page, Integer size) {
        // 参数校验：页码与每页条数必须为正数，且每页条数限制在100以内。
        if (page == null || page < 1) {
            return Result.fail(400, "page必须大于等于1");
        }
        if (size == null || size < 1 || size > 100) {
            return Result.fail(400, "size必须在1到100之间");
        }

        // 计算分页偏移量，并按用户维度查询成功的行程结果JSON。
        int offset = (page - 1) * size;
        List<String> planJsonList = tripPlanDao.findSuccessPlanJsonListByUserId(userId, offset, size);

        // 将数据库中的plan_json逐条反序列化为TripPlan对象列表。
        List<TripPlan> tripPlanList = new ArrayList<>();
        for (String planJson : planJsonList) {
            try {
                tripPlanList.add(objectMapper.readValue(planJson, TripPlan.class));
            } catch (JsonProcessingException ex) {
                log.error("解析TripPlan列表项失败，userId={}, page={}, size={}", userId, page, size, ex);
                return Result.fail(500, "历史行程解析失败：" + ex.getOriginalMessage());
            }
        }
        return Result.success(tripPlanList);
    }

    /**
     * Kafka消费者入口，接收消息后同步完成Agent调用和状态确认。
     *
     * @param payload Kafka消息内容
     * @return 无
     */
    @KafkaListener(topics = "${trip.kafka.topic}",
            concurrency = "${trip.kafka.listener-concurrency:4}",
            containerFactory = "tripKafkaListenerContainerFactory")
    public void consumeTripMessage(String payload, Acknowledgment acknowledgment) {
        try {
            processTripMessage(payload);
        } catch (Exception ex) {
            log.error("消费行程消息失败，payload={}", payload, ex);
        } finally {
            acknowledgment.acknowledge();
        }
    }

    /**
     * 处理Kafka消息并调用Agent服务。
     *
     * @param payload Kafka消息内容
     * @return 无
     */
    private void processTripMessage(String payload) {
        String requestId = "";
        try {
            // 反序列化消息并提取基础信息。
            AgentTripMessage message = objectMapper.readValue(payload, AgentTripMessage.class);
            requestId = message.getRequestId();
            TripPlanRecord record = tripPlanDao.findByUserIdAndRequestId(message.getUserId(), requestId);
            if (record == null) {
                log.error("未找到对应的行程记录，userId={}, requestId={}", message.getUserId(), requestId);
                return;
            }

            int retryCount = record.getRetryCount() == null ? 0 : record.getRetryCount();
            TripProcessingResult processingResult = callAgentWithRetry(message, requestId, retryCount);
            if (processingResult == null) {
                return;
            }

            // 处理成功后更新数据库状态与结果。
            tripPlanDao.updateResult(requestId, STATUS_SUCCESS, processingResult.planJson(), null, processingResult.retryCount());
        } catch (Exception ex) {
            log.error("消费行程消息失败，requestId={}", requestId, ex);
            if (!requestId.isBlank()) {
                tripPlanDao.updateResult(requestId, STATUS_FAILED, null, "消费失败：" + ex.getMessage(), 1);
            }
        }
    }

    /**
     * 调用Agent服务，首次失败时将记录标记为PENDING并重试一次。
     *
     * @param message Kafka消息
     * @param requestId 请求唯一ID
     * @param retryCount 当前已重试次数
     * @return 行程结果JSON
     */
    private TripProcessingResult callAgentWithRetry(AgentTripMessage message, String requestId, int retryCount) {
        int attempt = Math.min(retryCount, 1);
        while (attempt <= 1) {
            try {
                String planJson = restTemplate.postForObject(agentServerUrl, message.getTripRequest(), String.class);
                if (planJson == null || planJson.isBlank()) {
                    throw new IllegalStateException("Agent返回为空");
                }
                return new TripProcessingResult(planJson, attempt);
            } catch (Exception ex) {
                if (attempt == 0) {
                    tripPlanDao.updateResult(requestId, STATUS_PENDING, null, "首次消费失败，准备重试：" + ex.getMessage(), 1);
                    attempt = 1;
                    continue;
                }
                tripPlanDao.updateResult(requestId, STATUS_FAILED, null, "消费失败：" + ex.getMessage(), 1);
                return null;
            }
        }
        return null;
    }

    /**
     * Kafka消息处理结果。
     *
     * @param planJson 行程结果JSON
     * @param retryCount 最终使用的重试次数
     */
    private record TripProcessingResult(String planJson, int retryCount) {
    }
}
