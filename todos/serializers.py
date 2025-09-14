from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Todo, TodoAttachment, TodoComment

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """
    Kategori serializer'ı
    """
    todo_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'color', 'todo_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_todo_count(self, obj):
        """
        Kategoriye ait todo sayısını getir
        """
        return obj.todos.count()


class TodoAttachmentSerializer(serializers.ModelSerializer):
    """
    Todo eki serializer'ı
    """
    class Meta:
        model = TodoAttachment
        fields = ('id', 'filename', 'file', 'file_size', 'uploaded_at')
        read_only_fields = ('id', 'filename', 'file_size', 'uploaded_at')


class TodoCommentSerializer(serializers.ModelSerializer):
    """
    Todo yorumu serializer'ı
    """
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = TodoComment
        fields = ('id', 'user', 'user_name', 'user_username', 'comment', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')


class TodoCreateSerializer(serializers.ModelSerializer):
    """
    Todo oluşturma için basit serializer
    """
    class Meta:
        model = Todo
        fields = (
            'id', 'title', 'description', 'priority', 'due_date', 
            'is_important', 'is_completed', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'is_completed', 'created_at', 'updated_at')

    def create(self, validated_data):
        """
        Todo oluştururken kullanıcıyı otomatik ata
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class TodoListSerializer(serializers.ModelSerializer):
    """
    Todo listesi için basit serializer
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    days_until_due = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()

    class Meta:
        model = Todo
        fields = (
            'id', 'title', 'description', 'category', 'category_name', 'category_color',
            'is_completed', 'priority', 'due_date', 'is_important', 'is_starred',
            'days_until_due', 'is_overdue', 'created_at', 'updated_at'
        )


class TodoDetailSerializer(serializers.ModelSerializer):
    """
    Todo detayı için kapsamlı serializer
    """
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False)
    attachments = TodoAttachmentSerializer(many=True, read_only=True)
    comments = TodoCommentSerializer(many=True, read_only=True)
    days_until_due = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        fields = (
            'id', 'title', 'description', 'category', 'category_id',
            'is_completed', 'priority', 'due_date', 'completed_at',
            'is_important', 'is_starred', 'estimated_duration', 'actual_duration',
            'days_until_due', 'is_overdue', 'duration',
            'attachments', 'comments', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'completed_at', 'created_at', 'updated_at')

    def get_duration(self, obj):
        """
        Todo'nun süresini hesapla
        """
        if obj.actual_duration:
            return str(obj.actual_duration)
        elif obj.estimated_duration:
            return str(obj.estimated_duration)
        return None

    def create(self, validated_data):
        """
        Todo oluştururken kullanıcıyı otomatik ata
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class TodoCommentCreateSerializer(serializers.ModelSerializer):
    """
    Todo yorumu oluşturma serializer'ı
    """
    class Meta:
        model = TodoComment
        fields = ('id', 'comment', 'created_at')
        read_only_fields = ('id', 'created_at')

    def create(self, validated_data):
        """
        Yorum oluştururken kullanıcıyı otomatik ata
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
