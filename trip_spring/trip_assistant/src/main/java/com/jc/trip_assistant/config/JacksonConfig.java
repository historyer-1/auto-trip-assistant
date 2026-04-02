package com.jc.trip_assistant.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Jackson配置类，独立提供ObjectMapper Bean供JSON序列化使用。
 */
@Configuration
public class JacksonConfig {

    /**
     * 提供JSON序列化器，供登录拦截器统一返回Result对象。
     *
     * @param 无
     * @return ObjectMapper实例
     */
    @Bean
    public ObjectMapper objectMapper() {
        // 使用Jackson默认实现构建序列化器，避免手写JSON字符串。
        return new ObjectMapper();
    }
}
