# AI 执行计划与进度记录（progress1）

## 目标
将项目重构为“长连接复用 + 预创建 Agent + FastAPI 生命周期管理”架构。

## 执行计划
1. 新建 McpConnector，仅负责 MCP 长连接、Session 初始化、Tools 加载。
2. 重构 AttractionSearchAgent：启动阶段注入 tools 并预创建 LangChain Agent。
3. 重构 FastAPI：使用 lifespan 在启动时创建 connector 与 agent，挂载到 app.state。
4. 路由层改为轻量调用 app.state.agent.ainvoke()，加入超时与异常兜底。
5. 补充依赖、启动说明与架构验证清单。

## 进度日志
- [x] 完成第 1 项：新增 McpConnector（agentService/mcp_connector.py），支持 connect/close 与工具预加载。
- [x] 完成第 2 项：重构 AttractionSearchAgent（agentService/attraction_search_agent.py），去除请求内连接创建逻辑，改为复用预创建工具 Agent。
- [x] 完成提示词拆分：在 agentService/prompts/attraction_prompt.py 中补齐 Planner/Tool/Summary 提示词常量。
- [x] 完成第 3 项：改造 FastAPI 生命周期（fastapi/FastapiPan.py），启动阶段创建 connector 与 agent，并挂载至 app.state。
- [x] 完成第 4 项：路由层改为极简调用 app.state.agent.ainvoke()，并加入超时控制与异常兜底。
- [x] 完成补充项：更新 requirements.txt，加入 LangChain 现代 API 与 MCP 适配依赖。
- [x] 完成修正项：main.py 调试入口改为复用 McpConnector 与 agent.ainvoke()，避免旧 run 接口残留。
- [x] 第 5 项完成：在交付说明中补充架构验证清单、启动与请求链路说明，并指出现有设计中的可优化点。
- [x] 响应新增需求：将 agentService/attraction_search_agent.py 精简为单阶段自动工具调用流程，删除 planner/summary 分段链路与统一输出兜底函数。
- [x] 响应新增需求：将提示词收敛为单一 AGENT_SYSTEM_PROMPT，由提示词约束“先调用 MCP 工具再总结输出”。
