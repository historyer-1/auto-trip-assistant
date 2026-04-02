package com.jc.trip_assistant.common;

/**
 * 统一返回结果包装类
 * 所有业务接口均返回此类型，便于前端统一处理
 * @param <T> data 字段的类型
 */
public class Result<T> {
    private int code;
    private String message;
    private T data;

    public Result() {
    }

    public Result(int code, String message, T data) {
        this.code = code;
        this.message = message;
        this.data = data;
    }

    /**
     * 成功响应（无数据）
     */
    public static <T> Result<T> success() {
        return new Result<>(0, "success", null);
    }

    /**
     * 成功响应（返回数据）
     */
    public static <T> Result<T> success(T data) {
        return new Result<>(0, "success", data);
    }
    public static <T> Result<T> success(String message) {
        return new Result<>(0, message, null);
    }

    /**
     * 成功响应（自定义消息和数据）
     */
    public static <T> Result<T> success(String message, T data) {
        return new Result<>(0, message, data);
    }

    /**
     * 失败响应
     */
    public static <T> Result<T> fail(int code, String message) {
        return new Result<>(code, message, null);
    }

    /**
     * 失败响应（常用业务码）
     */
    public static <T> Result<T> fail(String message) {
        return new Result<>(500, message, null);
    }

    // Getter 和 Setter 方法，支持 Thymeleaf 和序列化访问
    public int getCode() {
        return code;
    }

    public void setCode(int code) {
        this.code = code;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public T getData() {
        return data;
    }

    public void setData(T data) {
        this.data = data;
    }

    @Override
    public String toString() {
        return "Result{" +
                "code=" + code +
                ", message='" + message + '\'' +
                ", data=" + data +
                '}';
    }
}