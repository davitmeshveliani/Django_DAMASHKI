from django.urls import path
from apps.myapp.views.task_views import TaskListCreateView, TaskDetailView
from apps.myapp.views.category_views import CategoryListCreateView, CategoryDetailView
from apps.myapp.views.stats_views import TaskStatsView
from apps.myapp.views.subtask_views import SubTaskListCreateView, SubTaskDetailUpdateDeleteView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),

    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
]