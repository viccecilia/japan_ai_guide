from pydantic import BaseModel, Field


class SpotSearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=200)
    language: str = Field(default="zh-CN", max_length=20)


class SpotItem(BaseModel):
    id: str
    name: str
    city: str
    category: str
    summary: str
    mock: bool = True


class SpotSearchData(BaseModel):
    query: str
    items: list[SpotItem]
