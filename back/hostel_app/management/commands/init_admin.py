from django.core.management.base import BaseCommand
from django.conf import settings
from hostel_app.models import CustomUser


class Command(BaseCommand):
    help = 'Создаёт супер администратора с заданными логином и паролем'

    def handle(self, *args, **options):
        username = settings.ADMIN_USERNAME
        password = settings.ADMIN_PASSWORD
        
        # Проверяем, существует ли уже такой пользователь
        if CustomUser.objects.filter(username=username).exists():
            user = CustomUser.objects.get(username=username)
            user.set_password(password)
            user.is_super_admin = True
            user.is_staff = True
            user.is_superuser = True
            user.status = 'active'
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Супер администратор "{username}" обновлён')
            )
        else:
            user = CustomUser.objects.create_superuser(
                username=username,
                password=password,
                email='admin@hostel.local'
            )
            user.is_super_admin = True
            user.status = 'active'
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Супер администратор "{username}" создан')
            )
        
        self.stdout.write(self.style.SUCCESS(f'Логин: {username}'))
        self.stdout.write(self.style.SUCCESS(f'Пароль: {password}'))
