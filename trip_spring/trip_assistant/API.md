# Trip Assistant 接口文档

## 1. 访问方式

- 协议：`HTTP/1.1`
- 基础地址：`http://localhost:8080`
- 内容类型：`application/json`（页面路由除外）
- 统一返回：所有业务接口使用 `Result<T>` 包装
- 认证方式：`JWT Bearer Token`

## 2. 统一返回对象 `Result<T>`

### 2.1 字段说明

| 字段 | 类型 | 必有 | 说明 |
|---|---|---|---|
| code | int | 是 | 业务码，`0` 表示成功 |
| message | string | 是 | 业务提示信息 |
| data | object/array/null | 是 | 业务数据 |

### 2.2 常用业务码

| code | 说明 |
|---|---|
| 0 | 成功 |
| 400 | 参数错误/校验失败 |
| 401 | 未登录或登录失效 |
| 404 | 资源不存在 |
| 500 | 服务内部错误 |

## 3. 页面路由

> 页面路由返回 HTML 模板，不返回业务 JSON。

| 页面 | 方法 | 路径 | 返回 | 说明 |
|---|---|---|---|---|
| 首页 | GET | `/` | `redirect:/login` | 统一入口 |
| 登录页 | GET | `/login` | `login` 模板 | 登录页面 |
| 行程看板 | GET | `/trip/dashboard` | `dashboard` 模板 | 看板页面 |

## 4. 认证与登录接口

### 4.1 发送邮箱验证码

- 方法：`POST`
- 路径：`/api/auth/send-code`
- 认证：不需要 token

请求体：

```json
{
  "email": "tester@example.com"
}
```

说明：
- 验证码通过邮件发送。
- 验证码会输出到后端日志，便于开发调试。
- Redis 存储键：`auth:code:{email}`。
- 过期时间：`3 分钟`。

### 4.2 邮箱验证码登录

- 方法：`POST`
- 路径：`/api/auth/login`
- 认证：不需要 token

请求体：

```json
{
  "email": "tester@example.com",
  "code": "123456"
}
```

响应体 `data`：

| 字段 | 类型 | 说明 |
|---|---|---|
| token | string | JWT令牌 |
| userId | long | 用户ID |
| email | string | 用户邮箱 |
| nickname | string | 用户昵称 |

说明：
- 先校验 Redis 中的邮箱验证码。
- 用户存在则直接登录，不存在则自动创建用户后登录。
- JWT 会写入 Redis：`auth:token:{token}`。
- 过期时间：`30 分钟`。

### 4.3 查询当前用户

- 方法：`GET`
- 路径：`/api/auth/me`
- 认证：需要 token

请求头：

```text
Authorization: Bearer <token>
```

### 4.4 退出登录

- 方法：`POST`
- 路径：`/api/auth/logout`
- 认证：需要 token

请求头：

```text
Authorization: Bearer <token>
```

说明：
- 退出时删除 Redis 中的 token，令牌立即失效。

## 5. 业务接口鉴权规则

- 除 `/api/auth/send-code` 与 `/api/auth/login` 外，其余 `/api/**` 接口都必须携带 JWT。
- 拦截器：`LoginInterceptor`。
- 放行条件：
  - 请求头存在 `Authorization: Bearer <token>`。
  - JWT 解析成功且未过期。
  - Redis 中存在对应 `auth:token:{token}` 会话键。
- 不满足条件时，统一返回：`Result.fail(401, "...")`。

## 6. 前端对 token 的处理约定

- 登录成功后将 `data.token` 保存到本地存储。
- 请求 `/api/**` 时（除发送验证码与登录），自动添加请求头：

```text
Authorization: Bearer <token>
```

- 收到 `401` 后清理本地 token 并跳转登录页。
- 退出登录时调用 `/api/auth/logout`，并清理本地 token。

## 7. 数据库与表结构

数据库配置见 `application.yaml`，用户表结构如下：

```sql
CREATE TABLE IF NOT EXISTS t_user (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '用户主键ID',
    email VARCHAR(128) NOT NULL UNIQUE COMMENT '登录邮箱，唯一',
    nickname VARCHAR(64) NOT NULL COMMENT '用户昵称',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';
```

初始化脚本位置：`src/main/resources/sql/schema.sql`

## 8. 接口实现检查清单

- [x] `/api/auth/send-code` (POST)：邮箱校验 + 邮件发送 + Redis验证码缓存
- [x] `/api/auth/login` (POST)：验证码校验 + 用户查询/新增 + JWT签发 + Redis登录态缓存
- [x] `/api/auth/me` (GET)：基于 token 返回当前用户
- [x] `/api/auth/logout` (POST)：清理 token 登录态
- [x] 登录拦截器：除登录接口外，全部要求 Bearer Token
- [x] 前端：除登录外统一携带 token
