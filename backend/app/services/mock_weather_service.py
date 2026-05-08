from app.schemas.travel_context import WeatherContext


def get_mock_weather_context(query: str) -> WeatherContext:
    text = query.lower()
    if any(token in text for token in ["下雨", "雨天", "rain", "rainy"]):
        return WeatherContext(condition="rainy", summary="今天可能下雨，建议减少连续户外步行。", outdoor_pressure="high")
    if any(token in text for token in ["很热", "高温", "炎热", "hot"]):
        return WeatherContext(condition="hot", summary="天气偏热，建议减少长时间步行并增加室内休息。", outdoor_pressure="high")
    if any(token in text for token in ["人多", "拥挤", "crowded"]):
        return WeatherContext(condition="crowded", summary="热门区域可能拥挤，建议避开连续热门点。", outdoor_pressure="medium")
    return WeatherContext(condition="sunny", summary="天气稳定，适合按原计划出行。", outdoor_pressure="normal")
