# Trip Assistant 接口文档

## 1. 访问方式

- 协议：`HTTP/1.1`
- 基础地址：`http://localhost:8080`
- 内容类型：`application/json`（页面路由除外）
- 会话：基于 Cookie（`JSESSIONID`）维护登录态
- 统一返回：所有业务接口使用 `Result<T>` 包装

## 2. 统一返回对象 `Result<T>`

### 2.1 Java 定义（约定）

```java
/**
 * 统一返回结果包装类
 * @param <T> data 字段的类型
 */
public class Result<T> {
    private int code;          // 业务码，0 表示成功
    private String message;    // 业务提示信息
    private T data;            // 业务数据（可为任意类型）

    // 成功响应
    public static <T> Result<T> success() { ... }
    public static <T> Result<T> success(T data) { ... }
    public static <T> Result<T> success(String message, T data) { ... }

    // 失败响应
    public static <T> Result<T> fail(int code, String message) { ... }
    public static <T> Result<T> fail(String message) { ... }

    // Getter / Setter / toString() 方法
    public int getCode() { ... }
    public String getMessage() { ... }
    public T getData() { ... }
}
```

### 2.2 字段说明

| 字段 | 类型 | 必有 | 说明 |
|---|---|---|---|
| code | int | 是 | 业务码，`0` 表示成功 |
| message | string | 是 | 业务提示信息 |
| data | object/array/null | 是 | 业务数据 |

### 2.3 常用业务码

| code | 说明 |
|---|---|
| 0 | 成功 |
| 400 | 参数错误/校验失败 |
| 401 | 未登录或登录失效 |
| 404 | 资源不存在 |
| 500 | 服务内部错误 |

### 2.4 响应示例

**成功响应** (code = 0)：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "city": "北京",
    "startDate": "2025-11-03",
    "endDate": "2025-11-05"
  }
}
```

**失败响应** (code ≠ 0)：

```json
{
  "code": 401,
  "message": "请先登录",
  "data": null
}
```

### 2.5 前端处理 Result 的标准模式

```javascript
// 调用 API 获取 Result 对象
const result = await fetch('/api/trip/overview').then(r => r.json());

// 标准处理流程
if (result.code !== 0) {
    // 处理失败情况
    console.error('错误消息：' + result.message);
    return;
}

// 使用 result.data 获取业务数据
const data = result.data;
console.log('目的地：' + data.city);
```

前端约束（当前实现）：

- 所有业务接口统一按 `Result<T>` 解析，必须包含 `code` 字段。
- 当 `code !== 0` 时，前端直接展示 `message` 并中断后续渲染。
- 当响应不是合法 JSON，或缺少 `code` 字段时，前端按失败处理（`code=500`）。

## 3. 页面路由

> 这三个路由用于返回页面（HTML），不是业务 JSON 接口。  
> 若返回 `Result` JSON，会导致页面无法渲染（例如出现 Whitelabel/模板解析异常）。

| 页面 | 方法 | 路径 | 正确返回（让前端可渲染） | 说明 |
|---|---|---|---|---|
| 登录页 | GET | `/login` | 返回模板 `login`（即 `templates/login.html`） | 页面依赖 `#email`、`#code`、`#sendCodeBtn`、`#loginBtn`，并加载 `/js/app.js` |
| 行程看板 | GET | `/trip/dashboard` | 返回模板 `dashboard`（即 `templates/dashboard.html`） | 页面依赖 `#overviewBox`、`#budgetBox`、`#mapBox`、`#dailyBox`、`#weatherBox`，并加载 `/js/app.js` |
| 首页 | GET | `/` | 建议 `redirect:/login`（或按登录态重定向到 `/trip/dashboard`） | 用作入口路由，避免直接返回空内容 |

### 3.1 推荐控制器返回方式

```java
@Controller
public class LoginController {

    @GetMapping("/")
    public String index() {
        return "redirect:/login";
    }

    @GetMapping("/login")
    public String login() {
        return "login";
    }

    @GetMapping("/trip/dashboard")
    public String dashboard() {
        return "dashboard";
    }
}
```

### 3.2 页面路由响应约束

- `Content-Type` 应为 `text/html`。
- 模板文件位置：`src/main/resources/templates/`。
- `/trip/dashboard` 的登录态由前端脚本通过 `/api/auth/me` 校验，未登录时前端会跳转到 `/login`。

## 4. 认证接口

### 4.1 发送邮箱验证码

- 方法：`POST`
- 路径：`/api/auth/send-code`

请求参数：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| email | string | 是 | 邮箱地址 |

请求示例：

```json
{
  "email": "tester@example.com"
}
```

### 4.2 验证码登录

- 方法：`POST`
- 路径：`/api/auth/login`

请求参数：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| email | string | 是 | 邮箱地址 |
| code | string | 是 | 6 位验证码 |

### 4.3 查询当前登录用户

- 方法：`GET`
- 路径：`/api/auth/me`
- 参数：无

### 4.4 退出登录

- 方法：`POST`
- 路径：`/api/auth/logout`
- 参数：无

## 5. 行程接口（需登录）

### 5.1 行程概览

- 方法：`GET`
- 路径：`/api/trip/overview`
- 参数：无

`data` 字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| city | string | 城市 |
| startDate | string | 开始日期（`yyyy-MM-dd`） |
| endDate | string | 结束日期（`yyyy-MM-dd`） |
| suggestion | string | 出行建议 |

### 5.2 预算明细

- 方法：`GET`
- 路径：`/api/trip/budget`
- 参数：无

| 字段 | 类型 | 说明 |
|---|---|---|
| ticketCost | int | 门票费用 |
| hotelCost | int | 住宿费用 |
| foodCost | int | 餐饮费用 |
| transportCost | int | 交通费用 |
| totalCost | int | 合计费用 |

### 5.3 景点地图点位

- 方法：`GET`
- 路径：`/api/trip/map-points`
- 参数：无

`data`（数组）字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| id | int | 点位序号 |
| name | string | 景点名称 |
| x | int | 横向百分比坐标 |
| y | int | 纵向百分比坐标 |

### 5.4 每日行程

- 方法：`GET`
- 路径：`/api/trip/daily-plans`
- 参数：无

`data`（数组）字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| dayIndex | int | 天序号 |
| date | string | 日期 |
| description | string | 日程描述 |
| transport | string | 交通方式 |
| hotel | string | 住宿偏好 |
| spots | array | 景点列表 |
| hotelSuggestion | object | 住宿推荐 |
| meals | array | 餐饮安排 |

### 5.5 天气信息

- 方法：`GET`
- 路径：`/api/trip/weather`
- 参数：无

`data`（数组）字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| date | string | 日期（如 `11-03`） |
| condition | string | 天气情况 |
| temp | string | 温度区间 |
| tip | string | 出行提示 |

## 6. 接口实现检查清单

> 以下清单帮助后端开发者确保所有接口都已正确实现

### 6.1 认证接口

- [ ] `/api/auth/send-code` (POST)
  - 请求体：`{ email: "string" }`
  - 响应：`Result<{ email: string }>`
  - 业务逻辑：验证邮箱格式，发送验证码（实际项目中可集成邮件服务）

- [ ] `/api/auth/login` (POST)
  - 请求体：`{ email: "string", code: "string" }`
  - 响应：`Result<{ email: string }>`
  - 业务逻辑：验证邮箱和验证码，创建会话

- [ ] `/api/auth/me` (GET)
  - 响应：`Result<{ email: string }>`
  - 业务逻辑：返回当前登录用户信息（需要会话检查）

- [ ] `/api/auth/logout` (POST)
  - 响应：`Result<null>`
  - 业务逻辑：清理会话

### 6.2 行程接口（需登录）

- [ ] `/api/trip/overview` (GET)
  - 响应：`Result<{ city, startDate, endDate, suggestion }>`
  
- [ ] `/api/trip/budget` (GET)
  - 响应：`Result<{ ticketCost, hotelCost, foodCost, transportCost, totalCost }>`
  
- [ ] `/api/trip/map-points` (GET)
  - 响应：`Result<Array<{ id, name, x, y }>>`
  
- [ ] `/api/trip/daily-plans` (GET)
  - 响应：`Result<Array<{ dayIndex, date, description, transport, hotel, spots[], hotelSuggestion, meals[] }>>`
  
- [ ] `/api/trip/weather` (GET)
  - 响应：`Result<Array<{ date, condition, temp, tip }>>`

### 6.3 会话管理说明

- **会话维护**：使用 Cookie（`JSESSIONID`）维护登录态
- **登录检查**：所有行程接口应在处理前调用 `HttpSession.getAttribute()` 检查用户登录态
- **未登录处理**：返回 `Result.fail(401, "请先登录")`

## 7. 前端 Mock 模式说明（仅前端开发）

当前前端支持 Mock 接口，默认关闭（默认走真实后端接口）：

- 启用：`http://localhost:8080/login?mock=1`
- 关闭：`http://localhost:8080/login?mock=0`
- 默认验证码：`123456`

该模式仅用于页面联调和样式演示；关闭 Mock 后，前端会直接调用本文档中定义的后端接口，并按 `Result<T>` 结构解析。

