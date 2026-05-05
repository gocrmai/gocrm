"""
Management command to create superuser for GOPOS CRM.
"""

from django.core.management.base import BaseCommand
from apps.users.models import User


class Command(BaseCommand):
    help = 'Create superuser for GOPOS CRM'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='gopos', help='Username')
        parser.add_argument('--email', default='info@gopos.hk', help='Email')
        parser.add_argument('--password', default='goposadmin123', help='Password')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists.')
            )
            # Update email and set password
            user = User.objects.get(username=username)
            user.email = email
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.role = User.Role.ADMIN
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'User "{username}" updated successfully.')
            )
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                chinese_name='系統管理員',
                role=User.Role.ADMIN,
                is_staff=True,
                is_superuser=True,
            )
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" created successfully.')
            )

        self.stdout.write(f'Login credentials:')
        self.stdout.write(f'  Username: {username}')
        self.stdout.write(f'  Email: {email}')
        self.stdout.write(f'  Password: {password}')
        self.stdout.write(f'\nPlease change the password after first login!')