from django.urls import path
from . import views

# Fichier d'URLs de l'application "products". Inclus depuis
# GestionPharmacie/urls.py via include('products.urls').
#
# Chaque path() associe :
#   1. un motif d'URL (ex. 'produits/'),
#   2. une vue a appeler dans views.py (ex. views.produits_liste),
#   3. un nom (name=...) qui permet de generer le lien sans jamais
#      ecrire l'URL en dur, ni dans les vues (reverse('produits_liste'))
#      ni dans les templates ({% url 'produits_liste' %}, voir
#      products/templates/partials/sidebar.html). Si l'URL change un
#      jour, seul le path() ci-dessous doit etre modifie.
#
# <int:pk> (voir 'factures/<int:pk>/') capture un nombre entier dans
# l'URL et le transmet a la vue comme argument pk (ex: /factures/12/
# appelle factures_detail(request, pk=12)).
urlpatterns = [
    path('', views.home, name='home'),

    path('produits/', views.produits_liste, name='produits_liste'),
    path('produits/ajouter/', views.produits_form, name='produits_form'),

    path('stock/', views.stock_liste, name='stock_liste'),

    path('ventes/', views.ventes_liste, name='ventes_liste'),
    path('ventes/nouvelle/', views.ventes_form, name='ventes_form'),

    path('clients/', views.clients_liste, name='clients_liste'),
    path('clients/ajouter/', views.clients_form, name='clients_form'),

    path('fournisseurs/', views.fournisseurs_liste, name='fournisseurs_liste'),
    path('fournisseurs/ajouter/', views.fournisseurs_form, name='fournisseurs_form'),

    path('factures/', views.factures_liste, name='factures_liste'),
    path('factures/<int:pk>/', views.factures_detail, name='factures_detail'),

    path('statistiques/', views.statistiques, name='statistiques'),
    path('notifications/', views.notifications, name='notifications'),
    path('parametres/', views.parametres, name='parametres'),

    path('connexion/', views.login, name='login'),
]
