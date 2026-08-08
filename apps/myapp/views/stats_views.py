from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.myapp.models import Task

class TaskStatsView(APIView):
    def get(self, request):
        total_tasks = Task.objects.count()
        data = {
            "total_tasks": total_tasks,
        }
        return Response(data, status=status.HTTP_200_OK)


# ==========================================
# ავტომატური ჯენერიკები / ViewSet (დაკომენტარებული)
# ==========================================
# from rest_framework.decorators import action
# from django.db.models import Count, Q
# from django.utils import timezone
#
# class TaskStatsViewSet(viewsets.ViewSet):
#     @action(detail=False, methods=['get'])
#     def stats(self, request):
#         now = timezone.now()
#         stats_data = Task.objects.aggregate(
#             total_tasks=Count('id'),
#             overdue_tasks=Count('id', filter=Q(deadline__lt=now) & ~Q(status='Done')),
#         )
#         return Response(stats_data, status=status.HTTP_200_OK)