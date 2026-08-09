from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Count, Q
from apps.myapp.models import Task




class TaskStatsView(APIView):

    def get(self, request):
        now = timezone.now()
        stats_data = Task.objects.aggregate(
            total_tasks=Count('id'),
            overdue_tasks=Count(
                'id', filter=Q(deadline__lt=now) & ~Q(status='Done') ),)

        status_counts_queryset = (
            Task.objects.values('status')
            .annotate(count=Count('id'))
            .order_by('status'))

        status_counts = {
            item['status']: item['count']
            for item in status_counts_queryset
            if item['status']}

        data = {
            'total_tasks': stats_data['total_tasks'],
            'status_counts': status_counts,
            'overdue_tasks': stats_data['overdue_tasks'],
        }
        return Response(data, status=status.HTTP_200_OK)


