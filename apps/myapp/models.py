from django.db import models
from django.utils import timezone

STATUS_CHOICES = [
    ('New', 'New'),
    ('In progress', 'In progress'),
    ('Pending', 'Pending'),
    ('Blocked', 'Blocked'),
    ('Done', 'Done'),
]

class Category(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Category Name")

    class Meta:
        app_label = 'myapp'
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Task(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=255, verbose_name="Task Title")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    categories = models.ManyToManyField(Category, related_name='tasks', verbose_name="Categories")
    status = models.CharField(choices=STATUS_CHOICES, max_length=100, default='New', verbose_name='Status')
    deadline = models.DateTimeField(null=True, blank=True, verbose_name="Deadline")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        app_label = 'myapp'
        unique_together = ('title', 'created_at')
        verbose_name = 'Task'
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.title

class SubTask(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=255, verbose_name="Subtask Title")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks', verbose_name="Main Task")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New', verbose_name="Status")
    deadline = models.DateTimeField(null=True, blank=True, verbose_name="Deadline")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        app_label = 'myapp'
        verbose_name = "Subtask"
        verbose_name_plural = "Subtasks"

    def __str__(self):
        return self.title