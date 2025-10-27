from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout
from django.utils import timezone
from django.conf import settings
from django.db.models import Q, Count
from .models import CustomUser, Room, Bed, Resident, AuditLog
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    RoomSerializer, BedSerializer, ResidentSerializer,
    AuditLogSerializer, AdminStatsSerializer
)


def get_client_ip(request):
    """Получить IP адрес клиента"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def create_audit_log(user, action, details='', request=None):
    """Создать запись в журнале аудита"""
    ip_address = get_client_ip(request) if request else None
    AuditLog.objects.create(
        user=user,
        action=action,
        details=details,
        ip_address=ip_address
    )


class IsSuperAdmin(permissions.BasePermission):
    """Проверка является ли пользователь супер админом"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_super_admin


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """Регистрация нового пользователя"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        create_audit_log(user, 'user_create', f'Новый пользователь: {user.username}', request)
        return Response({
            'message': 'Регистрация успешна. Ожидайте подтверждения администратора.',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Вход в систему"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Создаём JWT токены
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        # Логируем вход
        create_audit_log(user, 'login', f'Успешный вход', request)
        
        return Response({
            'message': 'Вход выполнен успешно',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Выход из системы"""
    create_audit_log(request.user, 'logout', 'Выход из системы', request)
    return Response({'message': 'Выход выполнен успешно'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """Получить текущего пользователя"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsSuperAdmin])
def admin_stats_view(request):
    """Получить статистику для админа"""
    # Статистика пользователей
    users = CustomUser.objects.all()
    total_users = users.count()
    pending_users = users.filter(status='pending').count()
    active_users = users.filter(status='active').count()
    suspended_users = users.filter(status='suspended').count()
    
    # Статистика комнат и кроватей
    rooms = Room.objects.all()
    total_rooms = rooms.count()
    beds = Bed.objects.all()
    total_beds = beds.count()
    occupied_beds = beds.filter(is_occupied=True).count()
    free_beds = total_beds - occupied_beds
    
    # Статистика жильцов
    residents = Resident.objects.all()
    total_residents = residents.count()
    today = timezone.now().date()
    current_residents = residents.filter(
        check_in_date__lte=today,
        check_out_date__gte=today
    ).count()
    
    data = {
        'total_users': total_users,
        'pending_users': pending_users,
        'active_users': active_users,
        'suspended_users': suspended_users,
        'total_rooms': total_rooms,
        'total_beds': total_beds,
        'occupied_beds': occupied_beds,
        'free_beds': free_beds,
        'total_residents': total_residents,
        'current_residents': current_residents,
    }
    
    serializer = AdminStatsSerializer(data)
    return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для управления пользователями"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    
    def get_queryset(self):
        queryset = CustomUser.objects.all()
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset.order_by('-created_at')
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        create_audit_log(
            request.user,
            'user_create',
            f"Создан пользователь: {response.data.get('username')}",
            request
        )
        return response
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        create_audit_log(
            request.user,
            'user_update',
            f"Обновлён пользователь ID: {kwargs.get('pk')}",
            request
        )
        return response
    
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        create_audit_log(
            request.user,
            'user_delete',
            f"Удалён пользователь: {user.username}",
            request
        )
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Одобрить пользователя"""
        user = self.get_object()
        user.status = 'active'
        user.save()
        create_audit_log(
            request.user,
            'user_approve',
            f"Одобрен пользователь: {user.username}",
            request
        )
        return Response({'message': 'Пользователь одобрен'})
    
    @action(detail=True, methods=['post'])
    def suspend(self, request, pk=None):
        """Заблокировать пользователя"""
        user = self.get_object()
        user.status = 'suspended'
        user.save()
        create_audit_log(
            request.user,
            'user_suspend',
            f"Заблокирован пользователь: {user.username}",
            request
        )
        return Response({'message': 'Пользователь заблокирован'})
    
    @action(detail=True, methods=['post'])
    def unsuspend(self, request, pk=None):
        """Разблокировать пользователя"""
        user = self.get_object()
        user.status = 'active'
        user.save()
        create_audit_log(
            request.user,
            'user_unsuspend',
            f"Разблокирован пользователь: {user.username}",
            request
        )
        return Response({'message': 'Пользователь разблокирован'})
    
    @action(detail=True, methods=['post'])
    def set_access_period(self, request, pk=None):
        """Установить срок доступа"""
        user = self.get_object()
        access_until = request.data.get('access_until')
        if access_until:
            user.access_until = access_until
            user.save()
            create_audit_log(
                request.user,
                'user_update',
                f"Установлен срок доступа для {user.username} до {access_until}",
                request
            )
            return Response({'message': 'Срок доступа установлен'})
        return Response({'error': 'access_until обязателен'}, status=status.HTTP_400_BAD_REQUEST)


class RoomViewSet(viewsets.ModelViewSet):
    """ViewSet для управления комнатами"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        create_audit_log(
            self.request.user,
            'room_create',
            f"Создана комната: {serializer.instance.name}",
            self.request
        )
    
    def perform_update(self, serializer):
        serializer.save()
        create_audit_log(
            self.request.user,
            'room_update',
            f"Обновлена комната: {serializer.instance.name}",
            self.request
        )
    
    def perform_destroy(self, instance):
        room_name = instance.name
        instance.delete()
        create_audit_log(
            self.request.user,
            'room_delete',
            f"Удалена комната: {room_name}",
            self.request
        )


class BedViewSet(viewsets.ModelViewSet):
    """ViewSet для управления кроватями"""
    queryset = Bed.objects.all()
    serializer_class = BedSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Bed.objects.all()
        room_id = self.request.query_params.get('room', None)
        if room_id:
            queryset = queryset.filter(room_id=room_id)
        return queryset.order_by('position')


class ResidentViewSet(viewsets.ModelViewSet):
    """ViewSet для управления жильцами"""
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Resident.objects.all()
        room_id = self.request.query_params.get('room', None)
        if room_id:
            queryset = queryset.filter(room_id=room_id)
        
        current_only = self.request.query_params.get('current', None)
        if current_only:
            today = timezone.now().date()
            queryset = queryset.filter(
                check_in_date__lte=today,
                check_out_date__gte=today
            )
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        create_audit_log(
            self.request.user,
            'resident_create',
            f"Создан жилец: {serializer.instance.name}",
            self.request
        )
    
    def perform_update(self, serializer):
        serializer.save()
        create_audit_log(
            self.request.user,
            'resident_update',
            f"Обновлён жилец: {serializer.instance.name}",
            self.request
        )
    
    def perform_destroy(self, instance):
        resident_name = instance.name
        instance.delete()
        create_audit_log(
            self.request.user,
            'resident_delete',
            f"Удалён жилец: {resident_name}",
            self.request
        )


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для просмотра журнала аудита"""
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    
    def get_queryset(self):
        queryset = AuditLog.objects.all()
        user_id = self.request.query_params.get('user', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        action = self.request.query_params.get('action', None)
        if action:
            queryset = queryset.filter(action=action)
        
        return queryset.order_by('-timestamp')
