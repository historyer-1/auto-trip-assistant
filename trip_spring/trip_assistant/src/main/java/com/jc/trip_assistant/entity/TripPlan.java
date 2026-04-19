package com.jc.trip_assistant.entity;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

/**
 * Agent返回的行程结果实体，对应Python端TripPlan。
 */
public class TripPlan {

    /**
     * 目的地城市。
     */
    private String city;

    /**
     * 开始日期。
     */
    @JsonProperty("start_date")
    private String startDate;

    /**
     * 结束日期。
     */
    @JsonProperty("end_date")
    private String endDate;

    /**
     * 每日行程列表，保持通用结构以便直接承接Agent返回。
     */
    private List<Object> days;

    /**
     * 天气信息列表，保持通用结构以便直接承接Agent返回。
     */
    @JsonProperty("weather_info")
    private List<Object> weatherInfo;

    /**
     * 总体建议。
     */
    @JsonProperty("overall_suggestions")
    private String overallSuggestions;

    /**
     * 预算信息，保持通用结构以便兼容后续扩展字段。
     */
    private Object budget;

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
     * 获取每日行程列表。
     *
     * @param 无
     * @return 每日行程列表
     */
    public List<Object> getDays() {
        return days;
    }

    /**
     * 设置每日行程列表。
     *
     * @param days 每日行程列表
     * @return 无
     */
    public void setDays(List<Object> days) {
        this.days = days;
    }

    /**
     * 获取天气信息列表。
     *
     * @param 无
     * @return 天气信息列表
     */
    public List<Object> getWeatherInfo() {
        return weatherInfo;
    }

    /**
     * 设置天气信息列表。
     *
     * @param weatherInfo 天气信息列表
     * @return 无
     */
    public void setWeatherInfo(List<Object> weatherInfo) {
        this.weatherInfo = weatherInfo;
    }

    /**
     * 获取总体建议。
     *
     * @param 无
     * @return 总体建议
     */
    public String getOverallSuggestions() {
        return overallSuggestions;
    }

    /**
     * 设置总体建议。
     *
     * @param overallSuggestions 总体建议
     * @return 无
     */
    public void setOverallSuggestions(String overallSuggestions) {
        this.overallSuggestions = overallSuggestions;
    }

    /**
     * 获取预算信息。
     *
     * @param 无
     * @return 预算信息
     */
    public Object getBudget() {
        return budget;
    }

    /**
     * 设置预算信息。
     *
     * @param budget 预算信息
     * @return 无
     */
    public void setBudget(Object budget) {
        this.budget = budget;
    }
}
