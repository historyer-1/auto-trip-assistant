package com.jc.trip_assistant;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Spring Boot 启动类。
 */
@SpringBootApplication
@MapperScan("com.jc.trip_assistant.dao")
public class TripAssistantApplication {

    /**
     * 应用启动入口。
     *
     * @param args 启动参数
     * @return 无
     */
    public static void main(String[] args) {
        // 启动Spring Boot应用上下文。
        SpringApplication.run(TripAssistantApplication.class, args);
    }

}
