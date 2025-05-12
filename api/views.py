from typing_extensions import Optional
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from api.dao import TaskDAO
from .models import task_to_model
from typing import Dict,Any

class TaskAPIView(APIView):
    def __init__(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)
        self.task_dao = TaskDAO()

    def get(self, request: Request, task_id: Optional[int] = None) -> Response:
        if task_id is None:
            return Response("task id not provided", status=status.HTTP_410_GONE)
        try:
            task = self.task_dao.get(task_id)
            if task:
                # Convert Task to TaskModel
                task_model = task_to_model(task)

                # and then to JSON
                return Response(task_model.model_dump(), status=status.HTTP_200_OK)
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
