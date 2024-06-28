# management/commands/create_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from cal.models import MaterialGroup, CreateCode, ColorCode

class Command(BaseCommand):
    help = 'Create user groups and assign permissions'

    def handle(self, *args, **kwargs):
        # Create groups
        admin_group, created = Group.objects.get_or_create(name='Admin')
        user_group, created = Group.objects.get_or_create(name='User')

        # Assign permissions to admin group
        admin_permissions = Permission.objects.all()
        admin_group.permissions.set(admin_permissions)

        # Assign limited permissions to user group
        user_permissions = Permission.objects.filter(
            content_type__app_label='cal',
            content_type__model__in=['indexview', 'aboutview', 'contactview']
        )
        user_group.permissions.set(user_permissions)

        self.stdout.write(self.style.SUCCESS('Successfully created groups and assigned permissions.'))
