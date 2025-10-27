from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator


class CustomUser(AbstractUser):
    """Кастомная модель пользователя"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('active', 'Активен'),
        ('suspended', 'Заблокирован'),
        ('expired', 'Срок истёк'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    access_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Доступ до'
    )
    is_super_admin = models.BooleanField(
        default=False,
        verbose_name='Супер администратор'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата регистрации'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_status_display()})"
    
    def is_access_expired(self):
        """Проверка истёк ли срок доступа"""
        if self.access_until:
            return timezone.now() > self.access_until
        return False
    
    def can_access(self):
        """Может ли пользователь получить доступ"""
        if self.is_super_admin:
            return True
        if self.status == 'suspended':
            return False
        if self.status == 'pending':
            return False
        if self.is_access_expired():
            return False
        return True


class Room(models.Model):
    """Модель комнаты"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название комнаты'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_rooms',
        verbose_name='Создал'
    )
    
    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_total_beds(self):
        """Общее количество мест в комнате"""
        return self.beds.count()
    
    def get_free_beds(self):
        """Количество свободных мест"""
        return self.beds.filter(is_occupied=False).count()
    
    def get_occupied_beds(self):
        """Количество занятых мест"""
        return self.beds.filter(is_occupied=True).count()


class Bed(models.Model):
    """Модель кровати"""
    BED_TYPE_CHOICES = [
        ('single', 'Одиночная'),
        ('double', 'Двухъярусная'),
    ]
    
    SIDE_CHOICES = [
        ('left', 'Левая сторона'),
        ('right', 'Правая сторона'),
        ('center', 'Центр'),
    ]
    
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='beds',
        verbose_name='Комната'
    )
    bed_type = models.CharField(
        max_length=10,
        choices=BED_TYPE_CHOICES,
        default='single',
        verbose_name='Тип кровати'
    )
    side = models.CharField(
        max_length=10,
        choices=SIDE_CHOICES,
        default='center',
        verbose_name='Сторона'
    )
    bed_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Номер кровати'
    )
    is_occupied = models.BooleanField(
        default=False,
        verbose_name='Занято'
    )
    position = models.IntegerField(
        default=0,
        verbose_name='Позиция'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    class Meta:
        verbose_name = 'Кровать'
        verbose_name_plural = 'Кровати'
        ordering = ['room', 'position']
        unique_together = ['room', 'bed_number']
    
    def __str__(self):
        return f"{self.room.name} - {self.bed_number or 'без номера'}"


class Resident(models.Model):
    """Модель жильца"""
    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Оплачено'),
        ('unpaid', 'Не оплачено'),
        ('partial', 'Частично оплачено'),
    ]
    
    name = models.CharField(
        max_length=200,
        verbose_name='ФИО'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='residents',
        verbose_name='Комната'
    )
    bed = models.ForeignKey(
        Bed,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='residents',
        verbose_name='Кровать'
    )
    bed_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Номер кровати'
    )
    check_in_date = models.DateField(
        verbose_name='Дата заселения'
    )
    check_out_date = models.DateField(
        verbose_name='Дата выселения'
    )
    payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Сумма оплаты'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='unpaid',
        verbose_name='Статус оплаты'
    )
    passport_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Номер паспорта'
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Телефон'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Примечания'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_residents',
        verbose_name='Создал'
    )
    
    class Meta:
        verbose_name = 'Жилец'
        verbose_name_plural = 'Жильцы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.room.name}"
    
    def is_current(self):
        """Является ли жилец текущим"""
        today = timezone.now().date()
        return self.check_in_date <= today <= self.check_out_date


class SystemSettings(models.Model):
    """Системные настройки"""
    key = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Ключ'
    )
    value = models.TextField(
        verbose_name='Значение'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Настройка системы'
        verbose_name_plural = 'Настройки системы'
    
    def __str__(self):
        return f"{self.key}: {self.value}"


class AuditLog(models.Model):
    """Журнал действий"""
    ACTION_CHOICES = [
        ('login', 'Вход в систему'),
        ('logout', 'Выход из системы'),
        ('user_create', 'Создание пользователя'),
        ('user_update', 'Изменение пользователя'),
        ('user_delete', 'Удаление пользователя'),
        ('user_approve', 'Одобрение пользователя'),
        ('user_suspend', 'Блокировка пользователя'),
        ('user_unsuspend', 'Разблокировка пользователя'),
        ('room_create', 'Создание комнаты'),
        ('room_update', 'Изменение комнаты'),
        ('room_delete', 'Удаление комнаты'),
        ('resident_create', 'Создание жильца'),
        ('resident_update', 'Изменение жильца'),
        ('resident_delete', 'Удаление жильца'),
    ]
    
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs',
        verbose_name='Пользователь'
    )
    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES,
        verbose_name='Действие'
    )
    details = models.TextField(
        blank=True,
        verbose_name='Детали'
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='IP адрес'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время'
    )
    
    class Meta:
        verbose_name = 'Запись аудита'
        verbose_name_plural = 'Журнал аудита'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user} - {self.get_action_display()} - {self.timestamp}"
