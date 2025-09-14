from django.urls import path
from .views import (
    CategoryListCreateView, CategoryDetailView,
    TodoListCreateView, TodoDetailView,
    toggle_todo, add_todo_comment,
    todo_statistics, upcoming_todos
)

app_name = 'todos'

urlpatterns = [
    # Kategori endpoints
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    
    # Todo endpoints
    path('', TodoListCreateView.as_view(), name='todo-list-create'),
    path('<int:pk>/', TodoDetailView.as_view(), name='todo-detail'),
    path('<int:pk>/toggle/', toggle_todo, name='todo-toggle'),
    path('<int:pk>/comments/', add_todo_comment, name='todo-add-comment'),
    
    # İstatistik ve özel endpoints
    path('statistics/', todo_statistics, name='todo-statistics'),
    path('upcoming/', upcoming_todos, name='upcoming-todos'),
]
