from app.schemas.language import LanguageListData, LanguageOption


def list_supported_languages() -> LanguageListData:
    return LanguageListData(
        items=[
            LanguageOption(code="zh-CN", label="Chinese", native_label="中文"),
            LanguageOption(code="en", label="English", native_label="English"),
            LanguageOption(code="ja", label="Japanese", native_label="日本語"),
            LanguageOption(code="ko", label="Korean", native_label="한국어"),
            LanguageOption(code="th", label="Thai", native_label="ไทย"),
        ]
    )
