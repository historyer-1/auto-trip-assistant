package com.jc.trip_assistant.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.stereotype.Component;

import java.io.Serializable;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Component
public class Mail implements Serializable {
    private String recipient;//邮件接收目的地址
    private String subject;//邮件主题
    private String content;//邮件内容
}
