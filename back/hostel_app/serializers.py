from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import CustomUser, Room, Bed, Resident, AuditLog


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""
    password = serializers.CharField(write_only=True, required=False)
    is_access_expired = serializers.SerializerMethodField()
    can_access = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'password',
            'status', 'access_until', 'is_super_admin', 'is_staff',
            'created_at', 'updated_at', 'is_access_expired', 'can_access'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_is_access_expired(self, obj):
        return obj.is_access_expired()
    
    def get_can_access(self, obj):
        return obj.can_access()
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации"""
    password = serializers.CharField(write_only=True, required=True, min_length=3)
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'password_confirm', 'email', 'first_name', 'last_name']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            status='pending'
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Сериализатор входа"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            
            if not user:
                raise serializers.ValidationError("Неверный логин или пароль")
            
            # Проверка доступа
            if not user.can_access() and not user.is_super_admin:
                if user.status == 'pending':
                    raise serializers.ValidationError("Ваша учётная запись ожидает подтверждения администратора")
                elif user.status == 'suspended':
                    raise serializers.ValidationError("Ваша учётная запись заблокирована")
                elif user.is_access_expired():
                    raise serializers.ValidationError("Срок доступа к вашей учётной записи истёк")
                else:
                    raise serializers.ValidationError("Доступ запрещён")
            
            data['user'] = user
        else:
            raise serializers.ValidationError("Необходимо указать логин и пароль")
        
        return data


class BedSerializer(serializers.ModelSerializer):
    """Сериализатор кровати"""
    room_name = serializers.CharField(source='room.name', read_only=True)
    
    class Meta:
        model = Bed
        fields = [
            'id', 'room', 'room_name', 'bed_type', 'side', 
            'bed_number', 'is_occupied', 'position', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class RoomSerializer(serializers.ModelSerializer):
    """Сериализатор комнаты"""
    beds = BedSerializer(many=True, read_only=True)
    total_beds = serializers.SerializerMethodField()
    free_beds = serializers.SerializerMethodField()
    occupied_beds = serializers.SerializerMethodField()
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Room
        fields = [
            'id', 'name', 'description', 'beds', 'total_beds', 
            'free_beds', 'occupied_beds', 'created_by', 
            'created_by_username', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_total_beds(self, obj):
        return obj.get_total_beds()
    
    def get_free_beds(self, obj):
        return obj.get_free_beds()
    
    def get_occupied_beds(self, obj):
        return obj.get_occupied_beds()


class ResidentSerializer(serializers.ModelSerializer):
    """Сериализатор жильца"""
    room_name = serializers.CharField(source='room.name', read_only=True)
    bed_side = serializers.CharField(source='bed.side', read_only=True, allow_null=True)
    is_current = serializers.SerializerMethodField()
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Resident
        fields = [
            'id', 'name', 'room', 'room_name', 'bed', 'bed_number', 
            'bed_side', 'check_in_date', 'check_out_date', 'payment_amount',
            'payment_status', 'passport_number', 'phone_number', 'notes',
            'is_current', 'created_by', 'created_by_username',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_is_current(self, obj):
        return obj.is_current()


class AuditLogSerializer(serializers.ModelSerializer):
    """Сериализатор журнала аудита"""
    username = serializers.CharField(source='user.username', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'username', 'action', 'action_display',
            'details', 'ip_address', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']


class AdminStatsSerializer(serializers.Serializer):
    """Сериализатор статистики для админа"""
    total_users = serializers.IntegerField()
    pending_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    suspended_users = serializers.IntegerField()
    total_rooms = serializers.IntegerField()
    total_beds = serializers.IntegerField()
    occupied_beds = serializers.IntegerField()
    free_beds = serializers.IntegerField()
    total_residents = serializers.IntegerField()
    current_residents = serializers.IntegerField()
