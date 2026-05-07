from pydantic import BaseModel


class HistoryItem(BaseModel):
    id: str
    question: str
    summary: str
    mock: bool = True


class HistoryListData(BaseModel):
    items: list[HistoryItem]
