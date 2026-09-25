import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Cree un superutilisateur par defaut s'il n'en existe aucun. "
        "Identifiants configurables via DJANGO_SUPERUSER_USERNAME, "
        "DJANGO_SUPERUSER_EMAIL et DJANGO_SUPERUSER_PASSWORD."
    )

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin123")

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.WARNING(
                    "Un superutilisateur existe deja, aucune action effectuee."
                )
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"L'utilisateur '{username}' existe deja, aucune action effectuee."
                )
            )
            return

        User.objects.create_superuser(
            username=username, email=email, password=password
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Superutilisateur '{username}' cree avec succes."
            )
        )
