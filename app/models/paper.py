from pydantic import BaseModel, Field, ConfigDict

# 声明输入、输出格式及输入约束

class PaperSearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=200)
    limit: int = Field(default=5, ge=1, le=20)

class PaperItem(BaseModel):
    id: int
    title: str

class PaperSearchResponse(BaseModel):
    query: str
    papers: list[PaperItem]

class PaperCreate(BaseModel):
    # 给 Pydantic 模型设置规则：处理字符串字段时，自动去掉首尾的空白字符。
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)
    url: str = Field(min_length=1, max_length=2048)
    source: str = Field(min_length=1, max_length=50, default="manual")

class PaperUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)

class PaperResponse(BaseModel):
    id: int
    title: str
    url: str
    created_at: str
    source: str
    