from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from models import GenerateRequest, GenerateResponse, ProjectPlan, ExplainRequest, ExplainResponse
from prompts import SYSTEM_PROMPT, SYSTEM_PROMPT_EXPLAIN

load_dotenv()

app = FastAPI(title="Backend API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api_router = APIRouter(prefix="/api", tags=["API"])
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



@api_router.get("/")
async def root():
    return {"message": "FastAPI server is running"}


@api_router.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """
    Generates a project plan based on the user's idea using OpenAI.
    """
    try:
        user_content = f"Idea: {request.prompt}. Preferred Stack: {request.tech_stack}"

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content}
            ],
            response_format={"type": "json_object"}, 
            temperature=0.7
        )

        content = response.choices[0].message.content

        data = json.loads(content)
        
        project_plan = ProjectPlan(**data)

        return GenerateResponse(
            result=project_plan,
            status="success"
        )

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="AI response parsing failed")
    except Exception as e:
        print(f"OpenAI Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/explain", response_model=ExplainResponse)
async def explain_task(request: ExplainRequest):
    """
    Detailed explanation for a specific task with code examples.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT_EXPLAIN},
                {"role": "user", "content": f"Explain task: {request.task_title}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )

        content = response.choices[0].message.content
        data = json.loads(content)

        return ExplainResponse(**data)

    except Exception as e:
        print(f"Explain Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to explain task")


app.include_router(api_router)

