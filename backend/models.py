from typing import List, Optional
from pydantic import BaseModel

class GenerateRequest(BaseModel):
    prompt: str
    tech_stack: Optional[str] = "AI decides"

class TaskItem(BaseModel):
    title: str
    description: str
    technical_hint: str

class ProjectPlan(BaseModel):
    project_name: str
    suggested_stack: List[str]
    tasks: List[TaskItem]

class GenerateResponse(BaseModel):
    result: ProjectPlan 
    status: str 

class ExplainRequest(BaseModel):
    task_title: str
    task_description: str
    tech_stack: str 
    project_context: str 

class ExplainResponse(BaseModel):
    explanation: str
    code_snippet: str 
    related_docs: List[str] 
