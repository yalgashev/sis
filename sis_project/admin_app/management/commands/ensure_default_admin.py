import os

from django.core.management.base import BaseCommand

from admin_app.models import Admin


class Command(BaseCommand):
    """Ensure a default admin record exists for the legacy admin portal."""

    help = "Creates or updates the default admin_app Admin record from environment variables."

    def handle(self, *args, **options):
        username = os.environ.get("ADMIN_PORTAL_USERNAME", "admin")
        password = os.environ.get("ADMIN_PORTAL_PASSWORD", "admin12345")
        email = os.environ.get("ADMIN_PORTAL_EMAIL", "admin@sis.local")
        first_name = os.environ.get("ADMIN_PORTAL_FIRST_NAME", "System")
        last_name = os.environ.get("ADMIN_PORTAL_LAST_NAME", "Administrator")
        is_super_admin = os.environ.get("ADMIN_PORTAL_SUPER", "1") == "1"

        admin, created = Admin.objects.get_or_create(
            username=username,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "password": password,
                "email": email,
                "is_active": True,
                "is_super_admin": is_super_admin,
            },
        )

        if not created:
            updated_fields = []
            if admin.password != password:
                admin.password = password
                updated_fields.append("password")
            if admin.email != email:
                admin.email = email
                updated_fields.append("email")
            if admin.first_name != first_name:
                admin.first_name = first_name
                updated_fields.append("first_name")
            if admin.last_name != last_name:
                admin.last_name = last_name
                updated_fields.append("last_name")
            if admin.is_super_admin != is_super_admin:
                admin.is_super_admin = is_super_admin
                updated_fields.append("is_super_admin")
            if not admin.is_active:
                admin.is_active = True
                updated_fields.append("is_active")

            if updated_fields:
                admin.save(update_fields=updated_fields)
                self.stdout.write(
                    self.style.WARNING(
                        f"Updated admin '{admin.username}' fields: {', '.join(updated_fields)}"
                    )
                )
            else:
                self.stdout.write(
                    f"Admin '{admin.username}' already up to date."
                )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Created default admin '{admin.username}' for admin portal."
                )
            )
