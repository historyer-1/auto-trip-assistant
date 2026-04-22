package com.jc.trip_assistant.config;

import org.apache.kafka.clients.admin.NewTopic;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.config.TopicBuilder;
import org.springframework.kafka.core.ConsumerFactory;
import org.springframework.kafka.listener.ContainerProperties;
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
        // 创建4分区Topic，配合4路消费者并发消费。
        return TopicBuilder.name(topicName).partitions(4).replicas(1).build();
    }

    /**
     * 创建Agent任务线程池。
     *
     * @param 无
     * @return 线程池执行器
     */
    @Bean("tripTaskExecutor")
    public Executor tripTaskExecutor() {
        // 使用固定规模线程池，和Kafka并发数保持一致。
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(4);
        executor.setMaxPoolSize(4);
        executor.setQueueCapacity(200);
        executor.setThreadNamePrefix("trip-task-");
        executor.initialize();
        return executor;
    }

    /**
     * 创建Kafka监听容器工厂，开启4路并发并使用手动立即确认。
     *
     * @param consumerFactory Kafka消费者工厂
     * @param listenerConcurrency 消费并发数
     * @return 监听容器工厂
     */
    @Bean("tripKafkaListenerContainerFactory")
    public ConcurrentKafkaListenerContainerFactory<String, String> tripKafkaListenerContainerFactory(
            ConsumerFactory<String, String> consumerFactory,
            @Value("${trip.kafka.listener-concurrency:4}") int listenerConcurrency) {
        ConcurrentKafkaListenerContainerFactory<String, String> factory = new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(consumerFactory);
        factory.setConcurrency(listenerConcurrency);
        factory.getContainerProperties().setAckMode(ContainerProperties.AckMode.MANUAL_IMMEDIATE);
        return factory;
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
