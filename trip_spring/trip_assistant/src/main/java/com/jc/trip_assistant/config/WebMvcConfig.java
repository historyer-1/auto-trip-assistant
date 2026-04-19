package com.jc.trip_assistant.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * WebMvc配置类，注册登录拦截器并定义拦截规则。
 */
@Configuration
public class WebMvcConfig implements WebMvcConfigurer {

    /**
     * 登录拦截器。
     */
    private final LoginInterceptor loginInterceptor;

    /**
     * 构造函数，注入登录拦截器。
     *
     * @param loginInterceptor 登录拦截器
     * @return 无
     */
    public WebMvcConfig(LoginInterceptor loginInterceptor) {
        this.loginInterceptor = loginInterceptor;
    }

    /**
     * 注册拦截器并配置路径白名单。
     *
     * @param registry 拦截器注册器
     * @return 无
     */
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(loginInterceptor)
                .addPathPatterns("/api/**")
                .excludePathPatterns("/api/auth/send-code", "/api/auth/login");
    }
}
