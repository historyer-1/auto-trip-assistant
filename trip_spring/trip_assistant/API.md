# Trip Assistant 后端 API 文档

本文档面向前端开发，描述当前后端已提供接口。所有接口统一返回结构：

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

- `code=0` 表示成功
- `code!=0` 表示失败

## 1. 认证模块

### 1.1 发送邮箱验证码
- 路径：`POST /api/auth/send-code`
- 鉴权：否
- 请求体：

```json
{
  "email": "user@example.com"
}
```

- 关键字段说明：
- `email`：邮箱，必填

- 成功响应示例：

```json
{
  "code": 0,
  "message": "邮件发送成功",
  "data": null
}
```

### 1.2 邮箱验证码登录
- 路径：`POST /api/auth/login`
- 鉴权：否
- 请求体：

```json
{
  "email": "user@example.com",
  "code": "123456"
}
```

- 关键字段说明：
- `email`：邮箱，必填
- `code`：6位数字验证码，必填

- 成功响应示例：

```json
{
  "code": 0,
  "message": "登录成功",
  "data": {
    "token": "<JWT_TOKEN>",
    "userId": 1,
    "email": "user@example.com",
    "nickname": "用户abc123"
  }
}
```

### 1.3 查询当前登录用户
- 路径：`GET /api/auth/me`
- 鉴权：是
- 请求头：
- `Authorization: <JWT_TOKEN>`

- 成功响应示例：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "userId": 1,
    "email": "user@example.com",
    "nickname": "用户abc123"
  }
}
```

### 1.4 退出登录
- 路径：`POST /api/auth/logout`
- 鉴权：是
- 请求头：
- `Authorization: <JWT_TOKEN>`

- 成功响应示例：

```json
{
  "code": 0,
  "message": "退出登录成功",
  "data": null
}
```

## 2. 行程模块

### 2.1 提交行程规划请求
- 路径：`POST /api/agent/trip/submit`
- 鉴权：是
- 请求头：
- `Authorization: <JWT_TOKEN>`

- 请求体：

```json
{
  "city": "杭州",
  "start_date": "2026-05-01",
  "end_date": "2026-05-03",
  "preference": "自然风景",
  "accommodation": "舒适型酒店",
  "transportation": "地铁+步行",
  "budget": 3000,
  "user_input": "希望安排轻松节奏"
}
```

- 关键字段说明：
- `city`：目的地城市，必填
- `start_date`：开始日期，必填
- `end_date`：结束日期，必填
- `budget`：预算，非负整数
- 其余字段均为可选偏好补充

- 成功响应示例：

```json
{
  "code": 0,
  "message": "请求已进入队列，请稍后查询",
  "data": "c9d8d6f8f4f14c8ea31f5f5948debe85"
}
```

- `data` 即 `requestId`。

### 2.2 按 requestId 查询单次行程结果
- 路径：`GET /api/agent/trip/query?requestId={requestId}`
- 鉴权：是
- 请求头：
- `Authorization: <JWT_TOKEN>`

- 请求参数：
- `requestId`：提交接口返回的请求唯一ID

- 成功响应示例：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "requestId": "c9d8d6f8f4f14c8ea31f5f5948debe85",
    "status": "SUCCESS",
    "errorMessage": null,
    "tripPlan": {
      "city": "杭州",
      "start_date": "2026-05-01",
      "end_date": "2026-05-03",
      "days": [],
      "weather_info": [],
      "overall_suggestions": "...",
      "budget": {}
    }
  }
}
```

- `status` 可能值：`PENDING`、`SUCCESS`、`FAILED`

### 2.3 分页查询当前用户历史行程计划列表
- 路径：`GET /api/agent/trip/plans?page={page}&size={size}`
- 鉴权：是
- 请求头：
- `Authorization: <JWT_TOKEN>`

- 请求参数：
- `page`：页码，从 1 开始，默认 1
- `size`：每页条数，默认 10，范围 1~100

- 返回说明：
- 返回当前登录用户的历史 `TripPlan` 列表（仅成功生成的行程）
- 按更新时间倒序返回

- 成功响应示例：

```json
{
  "code": 0,
  "message": "success",
  "data": [
    {
      "city": "杭州",
      "start_date": "2026-05-01",
      "end_date": "2026-05-03",
      "days": [],
      "weather_info": [],
      "overall_suggestions": "...",
      "budget": {}
    }
  ]
}
```

## 3. 前端对接建议

- 登录成功后，将 `token` 保存到本地，并在后续鉴权接口请求头携带：`Authorization: <JWT_TOKEN>`。
- 提交行程后先拿到 `requestId`，可轮询 `/api/agent/trip/query` 获取状态；同时可通过 `/api/agent/trip/plans` 分页展示历史行程。
