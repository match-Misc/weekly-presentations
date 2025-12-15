from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            password = os.environ.get('ADMIN_PASSWORD')
            if not password:
                self.stdout.write(self.style.ERROR('ADMIN_PASSWORD environment variable not set'))
                return
            User.objects.create_superuser('admin', 'admin@example.com', password)
            self.stdout.write(self.style.SUCCESS('Successfully created admin user'))