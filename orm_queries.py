import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


from apps.myapp.models import Task as TaskMy, SubTask as SubTaskMy
from apps.book.models import Task as TaskBook, SubTask as SubTaskBook, Category


def create_records():

    print("--- Creating records (get_or_create) ---")
    today = timezone.now()
    cat, _ = Category.objects.get_or_create(name="Study")

    # Myapp Task

    t_my, created = TaskMy.objects.get_or_create(
        title="Prepare presentation",
        defaults={
            "description": "Prepare materials and slides",
            "status": "New",
            "deadline": today + timedelta(days=3)
        })

    # Subtasks

    SubTaskMy.objects.get_or_create(title="Gather information", task=t_my,
                                    defaults={"status": "New",
                                              "deadline": today + timedelta
                                              (days=2)})
    SubTaskMy.objects.get_or_create(title="Create slides", task=t_my,
                                    defaults={"status": "New",
                                              "deadline": today + timedelta
                                              (days=1)})

    # Book Task

    t_book, created = TaskBook.objects.get_or_create(
        title="Prepare presentation",
        category=cat,
        defaults={
            "description": "Prepare materials and slides",
            "status": "New",
            "deadline": today + timedelta(days=3)
        })

    # Subtasks

    SubTaskBook.objects.get_or_create(title="Gather information", task=t_book,
                                      defaults={"status": "New",
                                                "deadline": today + timedelta
                                                (days=2)})

    SubTaskBook.objects.get_or_create(title="Create slides", task=t_book,
                                      defaults={"status": "New",
                                                "deadline": today + timedelta
                                                (days=1)})

    print("Records are ready (no duplicates created).")

    # 1. CREATE:

def read_records():

    print("\n--- Reading records ---")
    print("New Tasks count:",
          TaskMy.objects.filter(status="New").count() +
          TaskBook.objects.filter(status="New").count())


def update_records():

    print("\n--- Updating records ---")
    TaskMy.objects.filter(title="Prepare presentation").update(status="In progress")
    TaskBook.objects.filter(title="Prepare presentation").update(status="In progress")
    print("Status updated to 'In progress'")


def delete_records():

    print("\n--- Deleting records ---")
    TaskMy.objects.filter(title="Prepare presentation").delete()
    TaskBook.objects.filter(title="Prepare presentation").delete()
    print("Records deleted.")


if __name__ == '__main__':
    create_records()
    read_records()
    update_records()
    delete_records()