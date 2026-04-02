package com.jc.trip_assistant.dao;

import com.jc.trip_assistant.entity.User;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Options;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

/**
 * 用户DAO接口，负责用户表的数据库访问。
 */
@Mapper
public interface UserDao {

    /**
     * 根据邮箱查询用户。
     *
     * @param email 用户登录邮箱
     * @return 查询到的用户对象，未查询到返回null
     */
    @Select("SELECT id, email, nickname, create_time, update_time FROM t_user WHERE email = #{email} LIMIT 1")
    User findByEmail(@Param("email") String email);

    /**
     * 根据用户ID查询用户。
     *
     * @param id 用户主键ID
     * @return 查询到的用户对象，未查询到返回null
     */
    @Select("SELECT id, email, nickname, create_time, update_time FROM t_user WHERE id = #{id} LIMIT 1")
    User findById(@Param("id") Long id);

    /**
     * 新增用户记录。
     *
     * @param user 用户信息对象
     * @return 受影响行数
     */
    @Insert("INSERT INTO t_user(email, nickname) VALUES(#{email}, #{nickname})")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(User user);
}
