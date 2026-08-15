from django.urls import path
from apps.book.views.book_viewset_views import (
    BookAuthorListCreateAPIView,
    BookAuthorDetailAPIView,
    BookTaskListCreateAPIView,
    BookTaskDetailAPIView,
    BookSubTaskListCreateAPIView,
    BookSubTaskDetailAPIView,

)
from apps.book.views.category_views import BookCategoryListCreateAPIView

urlpatterns = [
    path('book-authors/', BookAuthorListCreateAPIView.as_view(), name='book-author-list'),
    path('book-authors/<uuid:pk>/', BookAuthorDetailAPIView.as_view(), name='book-author-detail'),

    path('book-tasks/', BookTaskListCreateAPIView.as_view(), name='book-task-list'),
    path('book-tasks/<int:pk>/', BookTaskDetailAPIView.as_view(), name='book-task-detail'),

    path('book-subtasks/', BookSubTaskListCreateAPIView.as_view(), name='book-subtask-list'),
    path('book-subtasks/<int:pk>/', BookSubTaskDetailAPIView.as_view(), name='book-subtask-detail'),

    path('categories/', BookCategoryListCreateAPIView.as_view(), name='category-list-create'),
]