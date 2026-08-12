from django.apps import AppConfig


# Configuration de l'application "products". Generee automatiquement
# par `python manage.py startapp products` et referencee dans
# INSTALLED_APPS (GestionPharmacie/settings.py) via 'products' : c'est
# ce qui indique a Django de charger cette app (ses modeles, ses
# templates dans products/templates/, ses fichiers statiques dans
# products/static/, etc.) au demarrage du projet.
class ProductsConfig(AppConfig):
    name = 'products'
