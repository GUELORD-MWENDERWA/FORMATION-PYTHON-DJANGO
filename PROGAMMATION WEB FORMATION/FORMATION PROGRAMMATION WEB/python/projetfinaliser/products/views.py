from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.db.models import Count, Max, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ClientForm, FournisseurForm, LigneVenteFormSet, ProduitForm, VenteForm
from .models import Client, Fournisseur, Produit, Vente


def est_gerant(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def gerant_required(view_func):
    """Autorise uniquement les comptes gerants (is_staff) ; redirige vers la
    connexion s'il n'y a personne, renvoie une erreur 403 sinon."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if not est_gerant(request.user):
            messages.error(request, "Cette page est reservee aux gerants.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def home(request):
    return render(request, 'home.html')


# ---------------------------------------------------------------------
# Produits
# ---------------------------------------------------------------------

@login_required
def produits_liste(request):
    produits = Produit.objects.select_related('categorie').annotate(
        total_ventes=Sum('lignes_vente__quantite')
    )
    return render(request, 'produits/liste.html', {'produits': produits})


@login_required
def produits_form(request, pk=None):
    produit = get_object_or_404(Produit, pk=pk) if pk else None
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            messages.success(request, "Produit enregistre.")
            return redirect('produits_liste')
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'produits/form.html', {'form': form, 'produit': produit})


@login_required
@permission_required('products.delete_produit', raise_exception=True)
@require_POST
def produits_delete(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    produit.delete()
    messages.success(request, "Produit supprime.")
    return redirect('produits_liste')


# ---------------------------------------------------------------------
# Stock (vue d'ensemble basee sur les memes produits)
# ---------------------------------------------------------------------

@login_required
def stock_liste(request):
    produits = Produit.objects.all()
    return render(request, 'stock/liste.html', {'produits': produits})


# ---------------------------------------------------------------------
# Clients
# ---------------------------------------------------------------------

@login_required
def clients_liste(request):
    clients = Client.objects.annotate(
        nb_achats=Count('ventes'),
        dernier_achat=Max('ventes__date'),
    )
    return render(request, 'clients/liste.html', {'clients': clients})


@login_required
def clients_form(request, pk=None):
    client = get_object_or_404(Client, pk=pk) if pk else None
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Client enregistre.")
            return redirect('clients_liste')
    else:
        form = ClientForm(instance=client)
    return render(request, 'clients/form.html', {'form': form, 'client': client})


@login_required
@permission_required('products.delete_client', raise_exception=True)
@require_POST
def clients_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.delete()
    messages.success(request, "Client supprime.")
    return redirect('clients_liste')


# ---------------------------------------------------------------------
# Fournisseurs (reserve aux gerants : relation fournisseur = decision
# de gestion, pas une operation de vente au quotidien)
# ---------------------------------------------------------------------

@gerant_required
def fournisseurs_liste(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'fournisseurs/liste.html', {'fournisseurs': fournisseurs})


@gerant_required
def fournisseurs_form(request, pk=None):
    fournisseur = get_object_or_404(Fournisseur, pk=pk) if pk else None
    if request.method == 'POST':
        form = FournisseurForm(request.POST, instance=fournisseur)
        if form.is_valid():
            form.save()
            messages.success(request, "Fournisseur enregistre.")
            return redirect('fournisseurs_liste')
    else:
        form = FournisseurForm(instance=fournisseur)
    return render(request, 'fournisseurs/form.html', {'form': form, 'fournisseur': fournisseur})


@gerant_required
@require_POST
def fournisseurs_delete(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    fournisseur.delete()
    messages.success(request, "Fournisseur supprime.")
    return redirect('fournisseurs_liste')


# ---------------------------------------------------------------------
# Ventes / Factures (une facture = la vente correspondante)
# ---------------------------------------------------------------------

@login_required
def ventes_liste(request):
    ventes = Vente.objects.select_related('client').prefetch_related('lignes')
    return render(request, 'ventes/liste.html', {'ventes': ventes})


@login_required
def ventes_form(request):
    produits_catalogue = Produit.objects.filter(actif=True)
    vente = Vente()
    if request.method == 'POST':
        vente_form = VenteForm(request.POST, instance=vente)
        formset = LigneVenteFormSet(request.POST, instance=vente)
        if vente_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                vente = vente_form.save()
                lignes = formset.save(commit=False)
                for ligne in lignes:
                    ligne.prix_unitaire = ligne.produit.prix
                    ligne.save()
                    produit = ligne.produit
                    produit.stock -= ligne.quantite
                    produit.save(update_fields=['stock'])
            messages.success(request, "Vente enregistree.")
            return redirect('factures_detail', pk=vente.pk)
    else:
        vente_form = VenteForm(instance=vente)
        formset = LigneVenteFormSet(instance=vente)
    return render(request, 'ventes/form.html', {
        'vente_form': vente_form,
        'formset': formset,
        'produits_catalogue': produits_catalogue,
    })


@login_required
def factures_liste(request):
    ventes = Vente.objects.select_related('client').prefetch_related('lignes')
    return render(request, 'factures/liste.html', {'ventes': ventes})


@login_required
def factures_detail(request, pk):
    vente = get_object_or_404(
        Vente.objects.select_related('client').prefetch_related('lignes__produit'),
        pk=pk,
    )
    return render(request, 'factures/detail.html', {'vente': vente})


# ---------------------------------------------------------------------
# Pages pas encore branchees a la base de donnees (hors perimetre de
# cette premiere passe backend, voir docs/ pour la suite)
# ---------------------------------------------------------------------

@login_required
def statistiques(request):
    return render(request, 'statistiques/index.html')


@login_required
def notifications(request):
    return render(request, 'notifications/liste.html')


@gerant_required
def parametres(request):
    return render(request, 'parametres/index.html')


# ---------------------------------------------------------------------
# Authentification
# ---------------------------------------------------------------------

def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'auth/login.html')


def logout_view(request):
    auth_logout(request)
    messages.success(request, "Vous etes deconnecte.")
    return redirect('login')
