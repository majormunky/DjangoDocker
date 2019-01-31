from django.core.management.base import BaseCommand
from core import models
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        if models.CoreUser.objects.count() == 0:
            for user in settings.ADMINS:
                user_parts = user[0].split(" ")

                email = user[1]
                password = 'admin'
                admin = models.CoreUser.objects.create_superuser(
                    first_name=user_parts[0], 
                    last_name=user_parts[1], 
                    email=email, 
                    password=password
                )
                admin.is_active = True
                admin.is_admin = True
                admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
