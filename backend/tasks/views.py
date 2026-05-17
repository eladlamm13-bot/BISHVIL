from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Task, ProjectTask
from .serializers import TaskSerializer, ProjectTaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # מאפשר לפרונטאנד לבקש רק משימות של אזור ספציפי באמצעות: /api/tasks/?region=1
        region_id = self.request.query_params.get('region')
        if region_id:
            queryset = queryset.filter(region_id=region_id)
        return queryset

class ProjectTaskViewSet(viewsets.ModelViewSet):
    queryset = ProjectTask.objects.all()
    serializer_class = ProjectTaskSerializer
    permission_classes = [IsAuthenticated]
    