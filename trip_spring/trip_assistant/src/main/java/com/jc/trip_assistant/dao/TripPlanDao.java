package com.jc.trip_assistant.dao;

import com.jc.trip_assistant.entity.TripPlanRecord;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.List;

/**
 * 行程计划DAO，负责t_trip_plan表访问。
 */
@Mapper
public interface TripPlanDao {

    /**
     * 新增一条行程请求记录。
     *
     * @param record 行程请求记录
     * @return 受影响行数
     */
    @Insert("""
            INSERT INTO t_trip_plan(user_id, request_id, request_json, status, retry_count)
            VALUES(#{userId}, #{requestId}, #{requestJson}, #{status}, #{retryCount})
            """)
    int insertPending(TripPlanRecord record);

    /**
     * 更新消费结果。
     *
     * @param requestId 请求唯一ID
     * @param status 处理状态
     * @param planJson 行程结果JSON
     * @param errorMessage 失败原因
     * @return 受影响行数
     */
    @Update("""
            UPDATE t_trip_plan
            SET status = #{status},
                plan_json = #{planJson},
                error_message = #{errorMessage},
                retry_count = #{retryCount}
            WHERE request_id = #{requestId}
            """)
    int updateResult(@Param("requestId") String requestId,
                     @Param("status") String status,
                     @Param("planJson") String planJson,
                     @Param("errorMessage") String errorMessage,
                     @Param("retryCount") int retryCount);

    /**
     * 按用户和请求ID查询记录。
     *
     * @param userId 用户ID
     * @param requestId 请求唯一ID
     * @return 行程请求记录
     */
    @Select("""
            SELECT id, user_id, request_id, request_json, plan_json, status, retry_count, error_message, create_time, update_time
            FROM t_trip_plan
            WHERE user_id = #{userId} AND request_id = #{requestId}
            LIMIT 1
            """)
    TripPlanRecord findByUserIdAndRequestId(@Param("userId") Long userId,
                                            @Param("requestId") String requestId);

    /**
     * 分页查询用户成功生成的行程结果JSON。
     *
     * @param userId 用户ID
     * @param offset 偏移量
     * @param size 每页条数
     * @return 行程结果JSON列表
     */
    @Select("""
            SELECT plan_json
            FROM t_trip_plan
            WHERE user_id = #{userId}
                    AND status = 'SUCCESS'
                    AND plan_json IS NOT NULL
            ORDER BY update_time DESC, id DESC
            LIMIT #{size} OFFSET #{offset}
            """)
    List<String> findSuccessPlanJsonListByUserId(@Param("userId") Long userId,
                                                 @Param("offset") int offset,
                                                 @Param("size") int size);
}
