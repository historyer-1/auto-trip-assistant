package com.jc.trip_assistant.config;

import org.apache.kafka.clients.admin.NewTopic;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.kafka.config.TopicBuilder;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import org.springframework.web.client.RestTemplate;

import java.util.concurrent.Executor;

/**
 * Agent行程异步处理配置，包含Kafka Topic、线程池和HTTP客户端。
 */
@Configuration
@EnableKafka
public class AgentTripAsyncConfig {

    /**
     * 创建行程请求Topic。
     *
     * @param topicName Topic名称
     * @return Topic对象
     */
    @Bean
    public NewTopic tripAgentRequestTopic(@Value("${trip.kafka.topic}") String topicName) {
        // 创建单分区Topic，当前场景足够使用，后续可按吞吐扩容分区数。
        return TopicBuilder.name(topicName).partitions(1).replicas(1).build();
    }

    /**
     * 创建Agent任务线程池。
     *
     * @param 无
     * @return 线程池执行器
     */
    @Bean("tripTaskExecutor")
    public Executor tripTaskExecutor() {
        // 使用固定规模线程池处理耗时HTTP调用，避免阻塞Kafka监听线程。
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(4);
        executor.setMaxPoolSize(8);
        executor.setQueueCapacity(200);
        executor.setThreadNamePrefix("trip-task-");
        executor.initialize();
        return executor;
    }

    /**
     * 创建RestTemplate客户端。
     *
     * @param 无
     * @return RestTemplate实例
     */
    @Bean
    public RestTemplate restTemplate() {
        // 统一使用Spring内置HTTP客户端调用Agent服务。
        return new RestTemplate();
    }
}
