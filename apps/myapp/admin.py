from django.contrib import admin
from .models import Task, SubTask, Category


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'status', 'deadline', 'created_at')
    filter_horizontal = ('categories',)
    list_filter = ('status', 'deadline')
    search_fields = ('title',)
    inlines = (SubTaskInline,)

    def short_title(self, obj):
        if len(obj.title) > 10:
            return obj.title[:10] + '...'
        return obj.title

    short_title.short_description = 'Title'


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline')
    list_filter = ('status', 'deadline')
    search_fields = ('title',)
    actions = ['make_done']

    @admin.action(description='Mark selected subtasks as Done')
    def make_done(self, request, queryset):
        updated_count = queryset.update(status='Done')
        self.message_user(request, f"{updated_count} subtasks were successfully marked as Done.")