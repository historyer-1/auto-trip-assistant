"""旅行编排共享上下文：在多个智能体之间传递关键结果。"""

from __future__ import annotations

from pydantic import BaseModel, Field

from entity.BasicClass import TripRequest


class TripWorkflowContext(BaseModel):
    """共享上下文数据。

    说明：
    - 仅保存流程编排所需的最小信息；
    - 使用简单字段避免复杂状态管理。
    """

    request: TripRequest = Field(..., description="用户原始旅行请求")
    attraction_result: str = Field(default="", description="景点搜索结果")
    weather_result: str = Field(default="", description="天气搜索结果")
    hotel_result: str = Field(default="", description="酒店搜索结果")

    def save_search_results(
        self,
        attraction_result: str,
        weather_result: str,
        hotel_result: str,
    ) -> None:
        """写入三个搜索智能体的结果。

        参数:
            attraction_result: 景点搜索文本结果。
            weather_result: 天气搜索文本结果。
            hotel_result: 酒店搜索文本结果。

        返回值:
            None
        """
        self.attraction_result = attraction_result
        self.weather_result = weather_result
        self.hotel_result = hotel_result
