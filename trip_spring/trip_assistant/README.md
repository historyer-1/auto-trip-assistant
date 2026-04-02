# Trip Assistant (Spring Boot MVC)

单体 Spring Boot + Thymeleaf 项目，当前已完成前端页面：

- 橙黄色简约主题（无渐变）
- 邮箱验证码登录页
- 行程看板（概览、预算、地图、每日行程、天气）
- 默认支持前端 Mock 数据演示

## 启动项目

```powershell
Set-Location "D:\project\agent\helloagents\auto_trip_assistant\trip_spring\trip_assistant"
mvn spring-boot:run
```

## 访问前端页面

```text
http://localhost:8080/login?mock=1
```

登录演示信息：

- 邮箱：任意合法邮箱
- 验证码：`123456`

> 如果你后续已接入真实后端接口，可改用 `http://localhost:8080/login?mock=0` 关闭前端 Mock。

## 运行测试

```powershell
Set-Location "D:\project\agent\helloagents\auto_trip_assistant\trip_spring\trip_assistant"
mvn test
```

## 接口文档

详细接口定义见 `API.md`。

