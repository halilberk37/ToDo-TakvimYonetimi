from django.shortcuts import render
from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import Category, Todo, TodoComment
from .serializers import (
    CategorySerializer, TodoListSerializer, TodoDetailSerializer, 
    TodoCreateSerializer, TodoCommentCreateSerializer
)
from .permissions import IsOwnerOrReadOnly, IsOwner


class CategoryListCreateView(generics.ListCreateAPIView):
    """
    Kategori listesi ve oluşturma
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Kategori detayı, güncelleme ve silme
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class TodoListCreateView(generics.ListCreateAPIView):
    """
    Todo listesi ve oluşturma
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_completed', 'priority', 'is_important', 'category']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'created_at', 'due_date', 'priority']
    ordering = ['-created_at']

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TodoCreateSerializer
        return TodoListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Todo detayı, güncelleme ve silme
    """
    serializer_class = TodoDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_todo(request, pk):
    """
    Todo tamamlama durumunu değiştir
    """
    try:
        todo = Todo.objects.get(pk=pk, user=request.user)
        todo.is_completed = not todo.is_completed
        if todo.is_completed:
            todo.completed_at = timezone.now()
        else:
            todo.completed_at = None
        todo.save()
        
        serializer = TodoDetailSerializer(todo)
        return Response(serializer.data)
    except Todo.DoesNotExist:
        return Response(
            {'error': 'Todo bulunamadı'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_todo_comment(request, pk):
    """
    Todo'ya yorum ekle
    """
    try:
        todo = Todo.objects.get(pk=pk, user=request.user)
        serializer = TodoCommentCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user, todo=todo)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Todo.DoesNotExist:
        return Response(
            {'error': 'Todo bulunamadı'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def todo_statistics(request):
    """
    Todo istatistikleri
    """
    user_todos = Todo.objects.filter(user=request.user)
    
    stats = {
        'total_todos': user_todos.count(),
        'completed_todos': user_todos.filter(is_completed=True).count(),
        'pending_todos': user_todos.filter(is_completed=False).count(),
        'high_priority_todos': user_todos.filter(priority='high').count(),
        'overdue_todos': user_todos.filter(
            due_date__lt=timezone.now().date(),
            is_completed=False
        ).count(),
    }
    
    return Response(stats)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def upcoming_todos(request):
    """
    Yaklaşan todo'lar
    """
    now = timezone.now()
    upcoming_date = now + timedelta(days=7)
    
    todos = Todo.objects.filter(
        user=request.user,
        due_date__range=[now.date(), upcoming_date.date()],
        is_completed=False
    ).order_by('due_date')
    
    serializer = TodoListSerializer(todos, many=True)
    return Response(serializer.data)
