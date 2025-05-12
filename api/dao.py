from contextlib import contextmanager
from datetime import datetime
from psycopg2.extensions import cursor
from django.db import transaction, connection
from typing import List, Optional
from src.task import Task, TaskRepository

class BaseDAO:
    def __init__(self):
        self.cursor = None

    @contextmanager
    def get_cursor(self) -> cursor:
        """Context manager for database cursor"""
        try:
            self.cursor = connection.cursor()
            yield self.cursor
        finally:
            if self.cursor:
                self.cursor.close()

    def execute(self, query: str, params: Optional[list] = None) -> cursor:
        """Execute a query and return the cursor"""
        with self.get_cursor() as cursor:
            cursor.execute(query, params or [])
            return cursor

class TaskDAO(BaseDAO, TaskRepository):

    def add(self, task: Task):
        return

    def get(self, task_id: int) -> Optional[Task]:
        with transaction.atomic():
            with self.get_cursor() as cursor:
                cursor.execute("""
                    SELECT id, location, source_language, target_language, start_time
                    FROM tasks
                    WHERE id = %s
                """, [task_id])
                row = cursor.fetchone()
                if row:
                    taskDTO = {
                        'id': row[0],
                        'location': row[1],
                        'source_language': row[2],
                        'target_language': row[3],
                        'start_time': row[4]
                    }
                    return Task(**taskDTO)
        return None

    def find_by_attributes(self, location: str, source_language: str, target_language: str) -> List[Task]:
        return []

    def find_by_location_time_range(self, location: str, start_time: datetime, end_time: datetime) -> List[Task]:
        return []
