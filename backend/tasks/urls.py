from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, ProjectTaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'project-tasks', ProjectTaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]