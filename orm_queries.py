import os
import django
from datetime import timedelta
from django.utils import timezone


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.myapp.models import Task, SubTask


def run_homework():
    # 1. CREATE:
    today = timezone.now()
    task = Task.objects.create(
        title="Prepare presentation",
        description="Prepare materials and slides for the presentation",
        status="New",
        deadline=today + timedelta(days=3)
    )

    SubTask.objects.create(
        task=task,
        title="Gather information",
        description="Find necessary information for the presentation",
        status="New",
        deadline=today + timedelta(days=2)
    )

    SubTask.objects.create(
        task=task,
        title="Create slides",
        description="Create presentation slides",
        status="New",
        deadline=today + timedelta(days=1)
    )
    print("1. Records Created")

    # 2. READ:
    print("--- New Tasks ---")
    print(list(Task.objects.filter(status="New")))

    print("--- Expired 'Done' Subtasks ---")
    print(list(SubTask.objects.filter(status="Done", deadline__lt=timezone.now())))

    # 3. UPDATE:
    # Task - change status
    task = Task.objects.get(title="Prepare presentation")
    task.status = "In progress"
    task.save()

    # SubTask - by 2 days
    sub1 = SubTask.objects.get(title="Gather information")
    sub1.deadline = sub1.deadline - timedelta(days=2)
    sub1.save()

    # SubTask - description

    sub2 = SubTask.objects.get(title="Create slides")
    sub2.description = "Create and format presentation slides"
    sub2.save()
    print("3. Updates Applied")

    # 4. DELETE:
    Task.objects.get(title="Prepare presentation").delete()
    print("4. Task Deleted")


if __name__ == '__main__':
    run_homework()