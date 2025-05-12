from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict, Callable, Any
from src.task import Task

class TaskModel(BaseModel):
    """
    JSON serializable Task model
    """
    id: Optional[int]
    location: str
    source_language: str
    target_language: str
    start_time: datetime

    class Config:
        # Specify the type for json_encoders
        json_encoders: Dict[type, Callable[[Any], str]] = {
            datetime: lambda v: v.isoformat()
        }

def task_to_model(task: Task) -> TaskModel:
    """Convert Task object to TaskModel"""
    return TaskModel(
        id=task.id,
        location=task.location,
        source_language=task.source_language,
        target_language=task.target_language,
        start_time=task.start_time
    )

def model_to_task(model: TaskModel) -> Task:
    """Convert TaskModel to Task object"""
    return Task(
        id=model.id,
        location=model.location,
        source_language=model.source_language,
        target_language=model.target_language,
        start_time=model.start_time
    )
