from django.contrib import admin
from django.db import models

class Task(models.Model):
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    source_language = models.CharField(max_length=10)
    target_language = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tasks'  # Specify the desired table name

    def __str__(self):
        return f"Task {self.id} at {self.location}"

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'source_language', 'target_language', 'start_time')
