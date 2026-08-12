"""
URL configuration for GestionPharmacie project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# Fichier d'URLs racine du PROJET (a distinguer de products/urls.py,
# qui est le fichier d'URLs de l'APPLICATION "products"). Django lit
# ce fichier en premier pour chaque requete, car ROOT_URLCONF pointe
# vers "GestionPharmacie.urls" dans settings.py.
urlpatterns = [
    # /admin/... -> interface d'administration Django, fournie
    # automatiquement par 'django.contrib.admin' (deja dans
    # INSTALLED_APPS). Vide tant qu'aucun modele n'est enregistre
    # dans products/admin.py.
    path('admin/', admin.site.urls),

    # '' -> delegue TOUTES les autres URLs (/, /produits/, /stock/...)
    # au fichier products/urls.py via include(). Ca permet de garder
    # les routes de chaque application dans son propre dossier plutot
    # que de tout entasser ici.
    path('', include('products.urls')),
]
