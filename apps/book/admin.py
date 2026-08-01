from django.contrib import admin
from .models import BookTask, BookSubTask, BookCategory, Book, BookAuthor


class BookSubTaskInline(admin.TabularInline):
    model = BookSubTask
    extra = 1


class BookInline(admin.TabularInline):
    model = Book
    extra = 1


@admin.register(BookAuthor)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio')
    search_fields = ('name',)
    inlines = [BookInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'status')
    list_filter = ('status', 'published_date')
    search_fields = ('title', 'author__name')


@admin.register(BookCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(BookTask)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'category', 'status', 'created_at')
    list_filter = ('category', 'status', 'created_at')
    search_fields = ('title',)
    inlines = (BookSubTaskInline,)

    def short_title(self, obj):
        if obj.title and len(obj.title) > 10:
            return obj.title[:10] + '***'
        return obj.title or ""

    short_title.short_description = 'Title'


@admin.register(BookSubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'created_at')
    list_filter = ('status', 'task')
    search_fields = ('title',)
    actions = ['make_done']

    @admin.action(description='Mark selected subtasks as Done')
    def make_done(self, request, queryset):
        updated_count = queryset.update(status='done')
        self.message_user(request, f"{updated_count} subtasks were successfully marked as Done.")