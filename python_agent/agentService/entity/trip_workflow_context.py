"""旅行编排共享上下文：在多个智能体之间传递关键结果。"""

from __future__ import annotations

from pydantic import BaseModel, Field

from agentService.entity.BasicClass import TripRequest


class TripWorkflowContext(BaseModel):
    """共享上下文数据。

    说明：
    - 四个搜索智能体输出统一保存为字符串；
    - 字符串中包含工具输出和模型输出，供规划智能体直接消费。
    """

    request: TripRequest = Field(..., description="用户原始旅行请求")
    attraction_response: str = Field(default="", description="景点搜索原始输出")
    weather_response: str = Field(default="", description="天气搜索原始输出")
    hotel_response: str = Field(default="", description="酒店搜索原始输出")
    meals_response: str = Field(default="", description="餐饮搜索原始输出")


    def save_search_results(
        self,
        attraction_result: str,
        weather_result: str,
        hotel_result: str,
        meals_result: str,
    ) -> None:
        """写入四个搜索智能体的结果。

        参数:
            attraction_result: 景点搜索原始输出。
            weather_result: 天气搜索原始输出。
            hotel_result: 酒店搜索原始输出。
            meals_result: 餐饮搜索原始输出。

        返回值:
            None
        """
        self.attraction_response = attraction_result
        self.weather_response = weather_result
        self.hotel_response = hotel_result
        self.meals_response = meals_result
