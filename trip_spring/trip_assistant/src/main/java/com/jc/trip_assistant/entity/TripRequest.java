package com.jc.trip_assistant.entity;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;

/**
 * 用户发起行程规划时的请求实体，对应Python端TripRequest。
 */
public class TripRequest {

    /**
     * 目的地城市。
     */
    @NotBlank(message = "city不能为空")
    private String city;

    /**
     * 开始日期。
     */
    @JsonProperty("start_date")
    @NotBlank(message = "startDate不能为空")
    private String startDate;

    /**
     * 结束日期。
     */
    @JsonProperty("end_date")
    @NotBlank(message = "endDate不能为空")
    private String endDate;

    /**
     * 旅行偏好。
     */
    private String preference;

    /**
     * 住宿偏好。
     */
    private String accommodation;

    /**
     * 交通偏好。
     */
    private String transportation;

    /**
     * 预算。
     */
    @Min(value = 0, message = "budget不能小于0")
    private Integer budget;

    /**
     * 用户补充输入。
     */
    @JsonProperty("user_input")
    private String userInput;

    /**
     * 获取目的地城市。
     *
     * @param 无
     * @return 目的地城市
     */
    public String getCity() {
        return city;
    }

    /**
     * 设置目的地城市。
     *
     * @param city 目的地城市
     * @return 无
     */
    public void setCity(String city) {
        this.city = city;
    }

    /**
     * 获取开始日期。
     *
     * @param 无
     * @return 开始日期
     */
    public String getStartDate() {
        return startDate;
    }

    /**
     * 设置开始日期。
     *
     * @param startDate 开始日期
     * @return 无
     */
    public void setStartDate(String startDate) {
        this.startDate = startDate;
    }

    /**
     * 获取结束日期。
     *
     * @param 无
     * @return 结束日期
     */
    public String getEndDate() {
        return endDate;
    }

    /**
     * 设置结束日期。
     *
     * @param endDate 结束日期
     * @return 无
     */
    public void setEndDate(String endDate) {
        this.endDate = endDate;
    }

    /**
     * 获取旅行偏好。
     *
     * @param 无
     * @return 旅行偏好
     */
    public String getPreference() {
        return preference;
    }

    /**
     * 设置旅行偏好。
     *
     * @param preference 旅行偏好
     * @return 无
     */
    public void setPreference(String preference) {
        this.preference = preference;
    }

    /**
     * 获取住宿偏好。
     *
     * @param 无
     * @return 住宿偏好
     */
    public String getAccommodation() {
        return accommodation;
    }

    /**
     * 设置住宿偏好。
     *
     * @param accommodation 住宿偏好
     * @return 无
     */
    public void setAccommodation(String accommodation) {
        this.accommodation = accommodation;
    }

    /**
     * 获取交通偏好。
     *
     * @param 无
     * @return 交通偏好
     */
    public String getTransportation() {
        return transportation;
    }

    /**
     * 设置交通偏好。
     *
     * @param transportation 交通偏好
     * @return 无
     */
    public void setTransportation(String transportation) {
        this.transportation = transportation;
    }

    /**
     * 获取预算。
     *
     * @param 无
     * @return 预算
     */
    public Integer getBudget() {
        return budget;
    }

    /**
     * 设置预算。
     *
     * @param budget 预算
     * @return 无
     */
    public void setBudget(Integer budget) {
        this.budget = budget;
    }

    /**
     * 获取用户补充输入。
     *
     * @param 无
     * @return 用户补充输入
     */
    public String getUserInput() {
        return userInput;
    }

    /**
     * 设置用户补充输入。
     *
     * @param userInput 用户补充输入
     * @return 无
     */
    public void setUserInput(String userInput) {
        this.userInput = userInput;
    }
}
