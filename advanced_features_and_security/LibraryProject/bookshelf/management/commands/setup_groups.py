from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

class Command(BaseCommand):
    help = 'Creates default permission groups for library system'
    
    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Book)

        # Permission definitions
        perms = {
            "can_view": "Can view book",
            "can_create": "Can create book",
            "can_edit": "Can edit book",
            "can_delete": "Can delete book"
        }

        # Group definitions with their permissions
        groups = {
            "Viewers": ["can_view"],
            "Editors": ["can_view", "can_create", "can_edit"],
            "Admins": ["can_view", "can_create", "can_edit", "can_delete"]
        }

        # Create permissions
        for codename, name in perms.items():
            Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=content_type
            )

        # Create groups and assign permissions
        for group_name, perm_codenames in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f"Created group: {group_name}")
            
            for codename in perm_codenames:
                try:
                    perm = Permission.objects.get(codename=codename)
                    group.permissions.add(perm)
                    self.stdout.write(f"Added permission '{codename}' to group '{group_name}'")
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(
                        f"Permission '{codename}' not found. Skipping for group '{group_name}'"
                    ))

        self.stdout.write(self.style.SUCCESS('Successfully created groups and permissions'))

