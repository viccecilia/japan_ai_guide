from app.schemas.history import HistoryItem, HistoryListData


def list_mock_history() -> HistoryListData:
    return HistoryListData(
        items=[
            HistoryItem(
                id="hist_001",
                question="清水寺",
                summary="景点介绍、历史背景、附近推荐",
            ),
            HistoryItem(
                id="hist_002",
                question="大阪一日游",
                summary="美食、路线、夜景建议",
            ),
            HistoryItem(
                id="hist_003",
                question="神社和寺庙区别",
                summary="文化解释与参拜礼仪",
            ),
        ]
    )
