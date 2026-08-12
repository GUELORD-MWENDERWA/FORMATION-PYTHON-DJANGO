from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),

    path('produits/', views.produits_liste, name='produits_liste'),
    path('produits/ajouter/', views.produits_form, name='produits_form'),
    path('produits/<int:pk>/modifier/', views.produits_form, name='produits_edit'),
    path('produits/<int:pk>/supprimer/', views.produits_delete, name='produits_delete'),

    path('stock/', views.stock_liste, name='stock_liste'),

    path('ventes/', views.ventes_liste, name='ventes_liste'),
    path('ventes/nouvelle/', views.ventes_form, name='ventes_form'),

    path('clients/', views.clients_liste, name='clients_liste'),
    path('clients/ajouter/', views.clients_form, name='clients_form'),
    path('clients/<int:pk>/modifier/', views.clients_form, name='clients_edit'),
    path('clients/<int:pk>/supprimer/', views.clients_delete, name='clients_delete'),

    path('fournisseurs/', views.fournisseurs_liste, name='fournisseurs_liste'),
    path('fournisseurs/ajouter/', views.fournisseurs_form, name='fournisseurs_form'),
    path('fournisseurs/<int:pk>/modifier/', views.fournisseurs_form, name='fournisseurs_edit'),
    path('fournisseurs/<int:pk>/supprimer/', views.fournisseurs_delete, name='fournisseurs_delete'),

    path('factures/', views.factures_liste, name='factures_liste'),
    path('factures/<int:pk>/', views.factures_detail, name='factures_detail'),

    path('statistiques/', views.statistiques, name='statistiques'),
    path('notifications/', views.notifications, name='notifications'),
    path('parametres/', views.parametres, name='parametres'),

    path('connexion/', views.login, name='login'),
    path('deconnexion/', views.logout_view, name='logout'),
]
