from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser if none exists'

    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@oraculo.com',
                password='admin123'
            )
            self.stdout.write(
                self.style.SUCCESS('Superuser created: admin/admin123')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Superuser already exists')
            )