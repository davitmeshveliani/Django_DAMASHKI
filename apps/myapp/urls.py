from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.myapp.views import CategoryViewSet, TaskViewSet, SubTaskViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'subtasks', SubTaskViewSet, basename='subtask')

urlpatterns = [
    path('', include(router.urls)),
]