from datetime import datetime
from typing import Dict, List, Optional
from abc import ABC, abstractmethod

class Task:
    """
    The Task object
    """
    def __init__(self, task_id: Optional[int], location: str, source_language: str, target_language: str, start_time: datetime):
        self.id = task_id
        self.location = location
        self.source_language = source_language
        self.target_language = target_language
        self.start_time = start_time

class TaskRepository(ABC):
    @abstractmethod
    def add(self, task: Task):
        pass
    @abstractmethod
    def get(self, task_id: int) -> Optional[Task]:
        pass
    @abstractmethod
    def find_by_attributes(self, location: str, source_language: str, target_language: str) -> List[Task]:
        pass
    @abstractmethod
    def find_by_location_time_range(self, location: str, start_time: datetime, end_time: datetime) -> List[Task]:
        pass

class InMemTaskRepository:
    def __init__(self):
        self.tasks: Dict[int, Task] = {}

    def add(self, task: Task):
        if task.id is None:
            task.id = len(self.tasks)

        self.tasks[task.id] = task

    def get(self, task_id: int) -> Optional[Task]:
        return self.tasks.get(task_id)

    def find_by_attributes(self, location: str, source_language: str, target_language: str) -> List[Task]:
        return [
            task for task in self.tasks.values()
            if task.location.lower() == location.lower() and
                task.source_language.lower() == source_language.lower() and
                task.target_language.lower() == target_language.lower()
        ]

    def find_by_location_time_range(self, location: str, start_time: datetime, end_time: datetime) -> List[Task]:
        return [
            task for task in self.tasks.values()
            if task.location.lower() == location.lower() and
                task.start_time >= start_time and task.start_time <= end_time
        ]
