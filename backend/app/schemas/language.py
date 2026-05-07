from pydantic import BaseModel


class LanguageOption(BaseModel):
    code: str
    label: str
    native_label: str


class LanguageListData(BaseModel):
    items: list[LanguageOption]
