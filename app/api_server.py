from fastapi import FastAPI
from app.api.papers import router as papers_router

# 创建主应用，保留健康检查，注册论文路由
app = FastAPI()

app.include_router(papers_router)

@app.get("/health")
async def health():
    return {
        "status": "ok"
    }

@app.get("/")
async def root():
    return {
        "message": "my Agent API"
    }
