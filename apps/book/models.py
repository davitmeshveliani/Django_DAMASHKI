from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Task(TimeStampedModel):
    title = models.CharField(max_length=100, blank=True, default="", verbose_name="Task Title")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tasks')
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default="New", blank=True, null=True)
    deadline = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.title

class SubTask(TimeStampedModel):
    task = models.ForeignKey(Task, on_delete=models.SET_NULL,null=True,blank=True, related_name='subtasks')
    title = models.CharField(max_length=100, blank=True, default="", verbose_name="Task Title")
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default="New", blank=True, null=True)
    deadline = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        verbose_name_plural = 'SubTasks'

    def __str__(self):
        return self.title