-- 给 t_trip_plan 表增加重试次数字段，配合PENDING重试机制使用。
USE trip_assistant;

ALTER TABLE t_trip_plan
    ADD COLUMN retry_count INT NOT NULL DEFAULT 0 COMMENT '重试次数' AFTER plan_json;
