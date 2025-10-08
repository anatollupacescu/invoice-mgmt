from datetime import datetime

class Task:
    def __init__(self, location: str, language: str):
        self.location = location
        self.language = language

class Invoice:
    def __init__(self, task: Task, start_time: datetime, end_time: datetime, signature: str):
        self.task = task
        self.start_time = start_time
        self.end_time = end_time
        self.signature = signature

    @property
    def duration(self):
        return self.end_time - self.start_time

    @property
    def is_valid(self):
        return (
            self.signature is not ""
            and datetime.now() <= self.start_time
        )
