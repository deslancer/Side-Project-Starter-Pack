from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Backend API", version="1.0.0")

# Создаем роутер для API с префиксом
api_router = APIRouter(prefix="/api", tags=["API"])


class GenerateRequest(BaseModel):
    prompt: Optional[str] = None


class GenerateResponse(BaseModel):
    result: str
    status: str


@api_router.get("/")
async def root():
    return {"message": "FastAPI server is running"}


@api_router.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """
    Generate endpoint - processes the input and returns a result
    """
    # Basic implementation - can be extended later
    result = f"Generated response for: {request.prompt or 'empty prompt'}"
    
    return GenerateResponse(
        result=result,
        status="success"
    )


# Подключаем роутер к приложению
app.include_router(api_router)

