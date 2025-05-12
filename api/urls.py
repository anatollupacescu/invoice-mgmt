from django.urls import path
from . import views

urlpatterns = [
    path('task/', views.TaskAPIView.as_view(), name='all_tasks'),
    path('task/<int:task_id>/', views.TaskAPIView.as_view(), name='hello_with_task_id'),
]
