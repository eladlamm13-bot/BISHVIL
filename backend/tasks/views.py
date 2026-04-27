from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Task, ProjectTask
from .serializers import TaskSerializer, ProjectTaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

class ProjectTaskViewSet(viewsets.ModelViewSet):
    queryset = ProjectTask.objects.all()
    serializer_class = ProjectTaskSerializer
    permission_classes = [IsAuthenticated]
    