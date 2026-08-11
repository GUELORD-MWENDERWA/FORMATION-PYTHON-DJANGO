from django.urls import path
from . import views


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
