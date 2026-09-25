from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .forms import FournisseurForm, ProduitForm, ClientForm, VenteForm, LigneVenteFormSet
from django.views.decorators.http import require_POST
from django.contrib.auth import  authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Produit,Fournisseur, Client, Vente
from django.db.models import Count, Max, Sum, F


# Vues de simple affichage pour le moment : chaque vue ne fait
# qu'afficher son template (aucune donnee de la base pour l'instant,
# ca viendra avec l'integration Django).

@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def produits_liste(request):
    produits = Produit.objects.select_related('categorie').annotate(
       total_ventes = Sum('Lignes_vente__quantite')
    )
    return render(request, 'produits/liste.html', {'produits': produits})


@login_required
def produits_form(request,pk=None):
    produit = get_object_or_404(Produit,pk=pk) if pk else None
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            messages.success(request, "Produit enregisté.")
            return redirect('produits_liste')

    else:
        form = ProduitForm(instance=produit)

    return render(request, 'produits/form.html', {'form': form, 'produit':produit})

@login_required
@permission_required('products.delete_produit', raise_exception=True)
@require_POST
def produits_delete(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    produit.delete()
    messages.success(request, "Produit supprimer.")
    return redirect('produits_liste')
   
   

@login_required
def stock_liste(request):
    produit = Produit.objects.all()
    return render(request, 'stock/liste.html', {'produits': produit})


@login_required
def ventes_liste(request):
    ventes =  Vente.objects.select_related('client').prefetch_related('lignes')
    return render(request, 'ventes/liste.html', {'ventes': ventes})


@login_required
def ventes_form(request):
    produits_catalogue = Produit.objects.filter(actif=True)
    if request.method == 'POST':
        vente_form = VenteForm(request.POST)
        formset = LigneVenteFormSet(request.POST, instance=vente_form.instance)
        if vente_form.is_valid() and formset.is_valid():
            vente = vente_form.save()
            formset.save()
            for ligne in vente.lignes.select_related('produit'):
                Produit.objects.filter(pk=ligne.produit_id).update(
                    stock=F('stock') - ligne.quantite
                )
            messages.success(request, "Vente enregistrée.")
            return redirect('factures_detail', pk=vente.pk)
    else:
        vente_form = VenteForm()
        formset = LigneVenteFormSet(instance=Vente())
    return render(request, 'ventes/form.html', {
        'vente_form': vente_form,
        'formset': formset,
        'produits_catalogue': produits_catalogue,
    })

@login_required
def clients_liste(request):
    clients = Client.objects.annotate(
        nb_achats = Count('ventes'),
        dernier_achat = Max('ventes__date')
    )
    return render(request, 'clients/liste.html', {'clients': clients})

@login_required 
def clients_form(request,pk=None):
    client = get_object_or_404(Client, pk=pk) if pk else None
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Client enregisté.")
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
    messages.success(request, "Client supprimer.")
    return redirect('clients_liste')

@login_required
def fournisseurs_liste(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'fournisseurs/liste.html', {'fournisseurs': fournisseurs})

@login_required
def fournisseurs_form(request, pk=None):
    fournisseurs = get_object_or_404(Fournisseur, pk=pk) if pk else None
    if request.method == 'POST':
        form = FournisseurForm(request.POST, instance=fournisseurs)
        if form.is_valid():
            form.save()
            messages.success(request, "Fournisseur enregisté.")
            return redirect('fournisseurs_liste')
    else:
        form = FournisseurForm(instance=fournisseurs)
    return render(request, 'fournisseurs/form.html',{'form': form, 'fournisseur': fournisseurs})

@login_required
@permission_required('products.delete_fournisseur', raise_exception=True)
@require_POST
def fournisseurs_delete(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)
    fournisseur.delete()
    messages.success(request, "Fournisseur supprimer.")
    return redirect('fournisseurs_liste')

@login_required
def factures_liste(request):
     ventes = Vente.objects.select_related('client').prefetch_related('lignes')
     return render(request, 'factures/liste.html', {'ventes':ventes})


@login_required
def factures_detail(request, pk):
    vente = get_object_or_404(
        Vente.objects.select_related('client').prefetch_related('lignes__produit'),pk=pk,
    )
    return render(request, 'factures/detail.html', {'vente':vente})


@login_required
def statistiques(request):
    return render(request, 'statistiques/index.html')


@login_required
def notifications(request):
    return render(request, 'notifications/liste.html')


@login_required
def parametres(request):
    return render(request, 'parametres/index.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    next_url = request.POST.get('next') or request.GET.get('next', '')

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if next_url and url_has_allowed_host_and_scheme(
                next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
            ):
                return redirect(next_url)
            return redirect('home')
        messages.error(request, "Mot d'utilisateur ou mot de passe incorect.")

    return render(request, 'auth/login.html', {'next': next_url})

def logout_view(request):
    auth_logout(request)
    messages.success(request, "Vous etes deconnecte.")
    return redirect('login')
