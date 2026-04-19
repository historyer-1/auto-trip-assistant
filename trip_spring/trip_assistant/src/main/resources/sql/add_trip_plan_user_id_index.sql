-- 给 t_trip_plan 表的 user_id 字段添加索引，提升按用户查询旅行计划的速度。
USE trip_assistant;

ALTER TABLE t_trip_plan
    ADD INDEX idx_user_id (user_id);
