from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

VENDEUR_CODENAMES = [
    'view_produit', 'add_produit', 'change_produit',
    'view_categorie',
    'view_client', 'add_client', 'change_client',
    'view_vente', 'add_vente', 'change_vente',
    'view_lignevente', 'add_lignevente', 'change_lignevente',
]

DEMO_USERS = [
    # username, password, is_staff, groupe
    ('gerant', 'pharmacie123', True, 'Gerant'),
    ('vendeur', 'pharmacie123', False, 'Vendeur'),
]


class Command(BaseCommand):
    help = (
        "Cree les groupes 'Gerant' et 'Vendeur' avec leurs permissions, "
        "ainsi que deux comptes de demonstration (gerant / vendeur, "
        "mot de passe pharmacie123). A lancer une fois, apres migrate."
    )

    def handle(self, *args, **options):
        vendeur, _ = Group.objects.get_or_create(name='Vendeur')
        vendeur.permissions.set(
            Permission.objects.filter(
                content_type__app_label='products',
                codename__in=VENDEUR_CODENAMES,
            )
        )

        gerant, _ = Group.objects.get_or_create(name='Gerant')
        gerant.permissions.set(
            Permission.objects.filter(content_type__app_label='products')
        )

        self.stdout.write(self.style.SUCCESS(
            "Groupes 'Gerant' et 'Vendeur' crees/mis a jour."
        ))

        User = get_user_model()
        groupes = {'Gerant': gerant, 'Vendeur': vendeur}
        for username, password, is_staff, groupe_nom in DEMO_USERS:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'is_staff': is_staff},
            )
            if created:
                user.set_password(password)
                user.is_staff = is_staff
                user.save()
            user.groups.add(groupes[groupe_nom])
            statut = "cree" if created else "deja present"
            self.stdout.write(f"Utilisateur '{username}' {statut} (groupe {groupe_nom}).")

        self.stdout.write(self.style.SUCCESS(
            "Termine. Connectez-vous avec gerant/pharmacie123 ou vendeur/pharmacie123."
        ))
