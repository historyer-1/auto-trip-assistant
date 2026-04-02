package com.jc.trip_assistant.util;


import com.jc.trip_assistant.entity.Mail;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class MailUtil {
    @Value("${spring.mail.username}")
    private String sender;//邮件发送源地址
    @Autowired
    private JavaMailSender javaMailSender;

    /**
     * 发送文本邮件
     *
     * @param mail
     */
    public boolean sendSimpleMail(Mail mail) {
        try {
            SimpleMailMessage mailMessage = new SimpleMailMessage();
            mailMessage.setFrom(sender); //邮件发送者
            mailMessage.setTo(mail.getRecipient()); // 邮件发给的人
            mailMessage.setSubject(mail.getSubject());  // 邮件主题
            mailMessage.setText(mail.getContent());  // 邮件内容
            //mailMessage.copyTo(copyTo);

            //javaMailSender.send(mailMessage);
            log.info("邮件发送成功 收件人：{}", mail.getRecipient());
            return true;
        } catch (Exception e) {
            log.error("邮件发送失败 {}", e.getMessage());
            return false;
        }
    }
}
