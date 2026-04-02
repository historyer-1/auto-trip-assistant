package com.jc.trip_assistant.config;

import com.jc.trip_assistant.common.Result;
import org.springframework.validation.BindException;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.List;

/**
 * 全局异常处理器，统一封装接口异常响应。
 */
@RestControllerAdvice
public class GlobalExceptionHandler {

    /**
     * 处理请求体参数校验异常。
     *
     * @param ex 参数校验异常对象
     * @return 统一错误响应
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public Result<Object> handleMethodArgumentNotValidException(MethodArgumentNotValidException ex) {
        // 提取首个字段错误信息，返回给前端做用户提示。
        List<FieldError> fieldErrors = ex.getBindingResult().getFieldErrors();
        String message = fieldErrors.isEmpty() ? "参数校验失败" : fieldErrors.get(0).getDefaultMessage();
        return Result.fail(400, message);
    }

    /**
     * 处理查询参数和表单参数校验异常。
     *
     * @param ex 参数绑定异常对象
     * @return 统一错误响应
     */
    @ExceptionHandler(BindException.class)
    public Result<Object> handleBindException(BindException ex) {
        // 提取首个字段错误信息，保证前端得到明确提示。
        List<FieldError> fieldErrors = ex.getBindingResult().getFieldErrors();
        String message = fieldErrors.isEmpty() ? "参数校验失败" : fieldErrors.get(0).getDefaultMessage();
        return Result.fail(400, message);
    }

    /**
     * 处理业务参数异常。
     *
     * @param ex 非法参数异常对象
     * @return 统一错误响应
     */
    @ExceptionHandler(IllegalArgumentException.class)
    public Result<Object> handleIllegalArgumentException(IllegalArgumentException ex) {
        // 将业务参数异常返回为400状态语义的业务码。
        return Result.fail(400, ex.getMessage());
    }

    /**
     * 处理业务状态异常。
     *
     * @param ex 非法状态异常对象
     * @return 统一错误响应
     */
    @ExceptionHandler(IllegalStateException.class)
    public Result<Object> handleIllegalStateException(IllegalStateException ex) {
        // 将业务状态异常返回为500业务码，提示稍后重试。
        return Result.fail(500, ex.getMessage());
    }
}
