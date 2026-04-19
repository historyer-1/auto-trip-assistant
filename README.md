# Trip Assistant

Trip Assistant 是一个旅行规划系统，当前后端由 Spring Boot 提供认证、行程提交、异步生成与结果查询能力。

系统核心链路：

1. 用户登录后提交行程请求。
2. 后端将请求写入 Kafka。
3. 消费端调用 Python Agent 生成行程。
4. 结果写回 MySQL，前端可按请求ID查询或按分页查询历史行程。

## 1. 项目结构

- `trip_spring/trip_assistant/`：Java 后端子项目
- `python_agent/`：Python 行程规划子项目
- `trip_spring/trip_assistant/src/main/java`：Spring Boot 业务代码（Controller/Service/DAO）
- `trip_spring/trip_assistant/src/main/resources/application.yaml`：运行配置
- `trip_spring/trip_assistant/src/main/resources/sql/*.sql`：数据库初始化脚本
- `trip_spring/trip_assistant/API.md`：后端接口文档（给前端）
- `python_agent/FastapiPan.py`：Python Agent 服务入口
- `python_agent/agentService/`：Agent 编排、工具和数据模型
- `python_agent/requirements.txt`：Python 依赖清单

## 2. 运行环境要求

### 2.1 基础软件版本建议

- JDK 21
- Maven 3.9+
- MySQL 8.0+
- Redis 7+
- Kafka 3.x

### 2.2 默认端口

- Spring Boot：`8080`
- MySQL：`3306`
- Redis：`6379`
- Kafka：`9092`
- Python Agent 服务：`8000`

## 3. 依赖服务部署

下面给出本地开发最小化部署方式。

### 3.1 MySQL

1. 启动 MySQL，确保可通过 `127.0.0.1:3306` 访问。
2. 创建数据库（可选，项目已配置自动建库）：


3. 确保 `application.yaml` 中数据库账号密码可用。

### 3.2 Redis

1. 启动 Redis，监听 `6379`，推介使用docker部署。
2. 使用默认配置即可满足当前登录态与验证码缓存。

### 3.3 Kafka

1. 启动 Kafka（确保 `127.0.0.1:9092` 可访问），推介使用docker部署。
2. 当前配置使用主题：`trip-agent-request`。
3. 可手工创建主题（可选）：

```bash
kafka-topics --create --topic trip-agent-request --bootstrap-server 127.0.0.1:9092 --partitions 1 --replication-factor 1
```

### 3.4 Python Agent 服务

1. Python Agent 子项目负责接收后端提交的行程请求，并调用本地工具生成结构化行程结果。
2. 入口文件是 `python_agent/FastapiPan.py`，提供健康检查接口 `/health` 和行程接口 `POST /agent/query`。
3. 安装依赖后在 `python_agent` 目录启动服务，默认监听 `8000` 端口。
4. 如果地址或端口变化，请同步修改 Java 项目 `application.yaml` 中 `trip.agent.server-url`。
5. Agent 采用“总编排 Agent + 多个领域 Agent”的方式拆分职责：景点、天气、酒店、餐饮分别并发检索，再由规划 Agent 汇总成最终行程。
6. 工具层直接接入高德地图接口，结合本地 adcode 映射、参数校验和超时控制，保证检索结果真实可用且稳定。
7. 规划阶段通过 Pydantic 模型、字段归一化和 JSON 修复兜底来约束模型输出，减少大模型格式漂移对接口和数据库的影响。

Python Agent 启动示例：

```powershell
Set-Location "你的项目位置\python_agent"
pip install -r requirements.txt
uvicorn FastapiPan:app --host 0.0.0.0 --port 8000 --reload
```

启动成功后可访问：

- 健康检查：`http://localhost:8000/health`
- 行程接口：`http://localhost:8000/agent/query`

## 4. 配置说明

配置文件位置：`src/main/resources/application.yaml`

重点配置项：

- `spring.datasource.*`：MySQL连接
- `spring.data.redis.*`：Redis连接
- `spring.kafka.*`：Kafka连接与序列化
- `trip.kafka.topic`：行程请求Topic
- `trip.agent.server-url`：Python Agent HTTP地址
- `spring.mail.*`：验证码邮件发送配置
- `jwt.secret`、`jwt.expire-minutes`：JWT配置

Python 子项目重点依赖：

- `fastapi`：HTTP 服务框架
- `uvicorn[standard]`：ASGI 服务器
- `pydantic`：请求与响应模型
- `langchain` / `langchain-openai`：Agent 编排
- `mcp`：工具接入能力

### 4.1 本地必须补齐的敏感配置文件

以下文件因为包含本地环境敏感信息或密钥，没有提交到仓库，但项目运行时必须存在：

- `trip_spring/trip_assistant/src/main/resources/application.yaml`：Spring Boot 主配置文件，包含数据库、Redis、Kafka、邮件和 Agent 地址等运行参数。
- `python_agent/agentService/entity/api_keys.py`：Python Agent 的高德地图等接口密钥配置。


## 5. 启动步骤

在 Windows PowerShell 中执行：

```powershell
Set-Location "你的项目位置\trip_spring\trip_assistant"
mvn spring-boot:run
```

启动成功后默认访问：

- 登录页：`http://localhost:8080/login`

## 6. 数据库初始化

项目不再在启动时自动执行 SQL 脚本，需要手动执行数据库初始化文件。

建议执行顺序如下：

1. `trip_spring/trip_assistant/src/main/resources/sql/schema.sql` 初始化用户表。
2. `trip_spring/trip_assistant/src/main/resources/sql/trip_plan_schema.sql` 初始化行程计划表。
3. `trip_spring/trip_assistant/src/main/resources/sql/add_trip_plan_user_id_index.sql` 如需单独补索引，可手动执行。

## 7. 接口说明

详细 API 文档见：`API.md`

重点接口：

1. `POST /api/auth/send-code` 发送验证码
2. `POST /api/auth/login` 登录
3. `POST /api/agent/trip/submit` 提交行程请求
4. `GET /api/agent/trip/query` 查询单次行程结果
5. `GET /api/agent/trip/plans` 分页查询当前用户历史行程

## 8. 代码检查与测试

```powershell
Set-Location "你的项目位置\trip_spring\trip_assistant"
mvn test
```

如果本地 MySQL、Redis、Kafka 或 Python Agent 未启动，部分测试或运行过程可能失败，请先确认依赖服务状态。

## 9. 常见问题

1. 启动报数据库连接失败：检查 MySQL 地址、账号密码、端口。
2. 登录接口报 Redis 连接失败：检查 Redis 服务和 `6379` 端口。
3. 提交行程后一直 `PENDING`：检查 Kafka 与 Python Agent 是否可用。
4. 邮件发送失败：检查 `spring.mail.username/password` 是否为有效 SMTP 凭据。
5. Python Agent 启动失败：先确认已安装 `python_agent/requirements.txt` 里的依赖，再检查 `FastapiPan.py` 是否在 `python_agent` 目录下启动。

