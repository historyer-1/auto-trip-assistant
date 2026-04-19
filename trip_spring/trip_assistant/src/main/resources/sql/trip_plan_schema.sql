-- 创建行程计划结果表：用于保存不同用户发起Agent请求后的生成结果。
USE trip_assistant;

CREATE TABLE IF NOT EXISTS t_trip_plan (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    user_id BIGINT NOT NULL COMMENT '用户ID',
    request_id VARCHAR(64) NOT NULL COMMENT '请求唯一ID',
    request_json LONGTEXT NOT NULL COMMENT '原始请求JSON',
    plan_json LONGTEXT NULL COMMENT '行程结果JSON',
    status VARCHAR(32) NOT NULL DEFAULT 'PENDING' COMMENT '处理状态：PENDING/SUCCESS/FAILED',
    error_message VARCHAR(512) NULL COMMENT '失败原因',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY uk_request_id (request_id),
    KEY idx_user_id (user_id),
    KEY idx_user_id_status_update_time (user_id, status, update_time, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户行程计划结果表';
