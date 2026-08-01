from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CommonStatus(models.TextChoices):
    NEW = 'new', 'New'
    IN_PROGRESS = 'in_progress', 'In Progress'
    DONE = 'done', 'Done'
    PUBLISHED = 'published', 'Published'
    ARCHIVED = 'archived', 'Archived'


class BookAuthor(TimeStampedModel):
    name = models.CharField(max_length=100, verbose_name="Author Name")
    bio = models.TextField(blank=True, null=True, verbose_name="Biography")

    class Meta:
        db_table = 'book_manager_author'
        verbose_name = 'Book Author'
        verbose_name_plural = 'Book Authors'

    def __str__(self):
        return self.name


class BookCategory(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")

    class Meta:
        db_table = 'book_manager_category'
        verbose_name = 'Book Category'
        verbose_name_plural = 'Book Categories'

    def __str__(self):
        return self.name


class Book(TimeStampedModel):
    objects = models.Manager()
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name="Book")
    author = models.ForeignKey(BookAuthor, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='books', verbose_name="Author")
    category = models.ForeignKey(BookCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='books', verbose_name="Category")
    published_date = models.DateField(null=True, blank=True, verbose_name="Дата публикации")

    status = models.CharField(
        max_length=20,
        choices=CommonStatus.choices,
        default=CommonStatus.PUBLISHED,
        verbose_name="Status"
    )

    class Meta:
        db_table = 'book_manager_book'
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['-published_date']

    def __str__(self):
        return self.title or "Untitled Book"


class BookTask(TimeStampedModel):
    title = models.CharField(max_length=100, blank=True, default="", verbose_name="Task Title")
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE, related_name='book_tasks')
    description = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=CommonStatus.choices,
        default=CommonStatus.NEW,
        verbose_name="Status"
    )
    deadline = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'book_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Book Task'
        verbose_name_plural = 'Book Tasks'

    def __str__(self):
        return self.title


class BookSubTask(TimeStampedModel):
    task = models.ForeignKey(BookTask, on_delete=models.SET_NULL, null=True, blank=True, related_name='book_subtasks')
    title = models.CharField(max_length=100, blank=True, default="", verbose_name="Task Title")
    description = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=CommonStatus.choices,
        default=CommonStatus.NEW,
        verbose_name="Status"
    )
    deadline = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'book_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'Book SubTask'
        verbose_name_plural = 'Book SubTasks'

    def __str__(self):
        return self.title