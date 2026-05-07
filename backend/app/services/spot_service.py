from app.schemas.spot import SpotItem, SpotSearchData


def search_mock_spots(query: str) -> SpotSearchData:
    return SpotSearchData(
        query=query,
        items=[
            SpotItem(
                id="spot_kiyomizu",
                name="清水寺",
                city="京都",
                category="寺院文化",
                summary="京都代表性寺院，适合半日路线和历史文化讲解。",
            ),
            SpotItem(
                id="spot_yasaka",
                name="八坂神社",
                city="京都",
                category="神社文化",
                summary="祇园附近的重要神社，可与清水寺串联游览。",
            ),
            SpotItem(
                id="spot_dotonbori",
                name="道顿堀",
                city="大阪",
                category="美食街区",
                summary="大阪夜景和街头美食的高频推荐区域。",
            ),
        ],
    )
