from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Sadece sahibi düzenleyebilir, diğerleri sadece okuyabilir
    """
    def has_object_permission(self, request, view, obj):
        # Okuma izni herkese açık
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Yazma izni sadece objenin sahibine
        return obj.user == request.user


class IsOwner(permissions.BasePermission):
    """
    Sadece sahibi erişebilir
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsEventOwnerOrParticipant(permissions.BasePermission):
    """
    Etkinlik sahibi veya katılımcısı erişebilir
    """
    def has_object_permission(self, request, view, obj):
        # Sahibi her zaman erişebilir
        if obj.user == request.user:
            return True
        
        # Katılımcısı sadece okuma yapabilir
        if request.method in permissions.SAFE_METHODS:
            return obj.participants.filter(user=request.user).exists()
        
        return False
