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
    name = models.CharField(max_length=100, verbose_name="Название категории")

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название задачи")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    categories = models.ManyToManyField(Category, related_name='tasks', verbose_name="Категории")
    status = models.CharField(choices=STATUS_CHOICES, max_length=100, default='New', verbose_name='Статус')
    deadline = models.DateTimeField(null=True, blank=True, verbose_name="Дедлайн")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        unique_together = ('title', 'created_at')
        verbose_name = 'Задача'
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.title

class SubTask(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название подзадачи")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks', verbose_name="Основная задача")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New', verbose_name="Статус")
    deadline = models.DateTimeField(null=True, blank=True, verbose_name="Дедлайн")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Подзадача"
        verbose_name_plural = "Подзадачи"

    def __str__(self):
        return self.title