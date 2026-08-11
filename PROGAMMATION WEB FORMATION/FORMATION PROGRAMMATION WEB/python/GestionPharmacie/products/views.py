from django.shortcuts import render

# Vues de simple affichage pour le moment : chaque vue ne fait
# qu'afficher son template (aucune donnee de la base pour l'instant,
# ca viendra avec l'integration Django).

def home(request):
    return render(request, 'home.html')


def produits_liste(request):
    return render(request, 'produits/liste.html')


def produits_form(request):
    return render(request, 'produits/form.html')


def stock_liste(request):
    return render(request, 'stock/liste.html')


def ventes_liste(request):
    return render(request, 'ventes/liste.html')


def ventes_form(request):
    return render(request, 'ventes/form.html')


def clients_liste(request):
    return render(request, 'clients/liste.html')


def clients_form(request):
    return render(request, 'clients/form.html')


def fournisseurs_liste(request):
    return render(request, 'fournisseurs/liste.html')


def fournisseurs_form(request):
    return render(request, 'fournisseurs/form.html')


def factures_liste(request):
    return render(request, 'factures/liste.html')


def factures_detail(request, pk):
    return render(request, 'factures/detail.html')


def statistiques(request):
    return render(request, 'statistiques/index.html')


def notifications(request):
    return render(request, 'notifications/liste.html')


def parametres(request):
    return render(request, 'parametres/index.html')


def login(request):
    return render(request, 'auth/login.html')
