package com.jc.trip_assistant.common;

import com.jc.trip_assistant.dto.UserDTO;

/**
 * 当前登录用户持有器，使用ThreadLocal保存请求上下文中的用户信息。
 */
public class UserHolder {

    /**
     * 保存当前请求对应的用户信息。
     */
    private static final ThreadLocal<UserDTO> USER_THREAD_LOCAL = new ThreadLocal<>();

    /**
     * 设置当前登录用户。
     *
     * @param userDTO 当前登录用户信息
     * @return 无
     */
    public static void setUser(UserDTO userDTO) {
        // 将用户信息绑定到当前线程，供后续业务链路读取。
        USER_THREAD_LOCAL.set(userDTO);
    }

    /**
     * 获取当前登录用户。
     *
     * @param 无
     * @return 当前登录用户信息，若不存在则返回null
     */
    public static UserDTO getUser() {
        // 从当前线程读取用户信息，避免在控制器中重复解析token。
        return USER_THREAD_LOCAL.get();
    }

    /**
     * 清理当前线程中的用户信息。
     *
     * @param 无
     * @return 无
     */
    public static void removeUser() {
        // 请求结束后清理ThreadLocal，避免线程复用导致数据串扰。
        USER_THREAD_LOCAL.remove();
    }
}
