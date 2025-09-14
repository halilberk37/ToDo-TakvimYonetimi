from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Kullanıcı kayıt serializer'ı
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'password_confirm', 'phone_number', 'birth_date', 'bio')
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        """
        Şifre doğrulama
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Şifreler eşleşmiyor.")
        return attrs

    def create(self, validated_data):
        """
        Yeni kullanıcı oluşturma
        """
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Kullanıcı giriş serializer'ı
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        """
        Kullanıcı doğrulama
        """
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Geçersiz e-posta veya şifre.')
            if not user.is_active:
                raise serializers.ValidationError('Hesap aktif değil.')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('E-posta ve şifre gereklidir.')


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Kullanıcı profil serializer'ı
    """
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'full_name', 
                 'phone_number', 'birth_date', 'profile_picture', 'bio', 'is_verified', 
                 'created_at', 'updated_at')
        read_only_fields = ('id', 'email', 'is_verified', 'created_at', 'updated_at')


class ChangePasswordSerializer(serializers.Serializer):
    """
    Şifre değiştirme serializer'ı
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        """
        Şifre doğrulama
        """
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Yeni şifreler eşleşmiyor.")
        return attrs

    def validate_old_password(self, value):
        """
        Eski şifre doğrulama
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Eski şifre yanlış.")
        return value
