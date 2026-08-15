from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .models import ActiveManager
from .views import CategoryViewSet, TaskViewSet, SubtaskViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tasks',TaskViewSet, basename='task')
router.register(r'subtasks',SubtaskViewSet, basename='subtask')


urlpatterns = [
    path('', include(router.urls)),
]