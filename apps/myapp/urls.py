from django.urls import path
from apps.myapp.views.task_views import TaskListCreateView, TaskDetailView
#from apps.myapp.views.stats_views import TaskStatsView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
#    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
]