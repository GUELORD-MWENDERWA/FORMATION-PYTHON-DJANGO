# 06 — Ventes : formulaires imbriques (formsets)

Fichiers concernes : [`products/forms.py`](../products/forms.py)
(`VenteForm`, `LigneVenteForm`, `LigneVenteFormSet`),
[`products/views.py`](../products/views.py) (`ventes_form`),
[`ventes/form.html`](../products/templates/ventes/form.html)

## Objectif du module

Le module le plus dense du cours : une vente n'est pas un seul
formulaire, c'est **un formulaire (la vente : client, paiement,
remise) plus un nombre variable de sous-formulaires (une ligne par
produit vendu)**. C'est exactement le probleme que resolvent les
*formsets* Django, et plus precisement les *inline formsets* quand
les sous-formulaires representent une relation `ForeignKey` vers
l'objet principal (ici, `LigneVente.vente`).

Si ce module est difficile a suivre en une seule fois, c'est normal :
prenez le temps de faire tourner le code et d'observer le HTML genere
(`view-source` dans le navigateur) avant de lire l'explication qui
suit.

## Etape 1 — Le formulaire de la vente elle-meme

```python
class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ['client', 'mode_paiement', 'remise']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].empty_label = "Client de passage"
```

Rien de nouveau par rapport au module 03, a un detail pres :
`empty_label`. Par defaut, un `ModelChoiceField` (genere pour une
`ForeignKey`) affiche `---------` comme option vide. On la remplace
par un texte qui a du sens dans le domaine metier : une vente sans
client selectionne, c'est une vente a un "Client de passage" (voir la
`ForeignKey` `null=True, blank=True` sur `Vente.client`, module 01).

## Etape 2 — Le formulaire d'une ligne, et son piege

```python
class LigneVenteForm(forms.ModelForm):
    produit = forms.ModelChoiceField(
        queryset=Produit.objects.all(), required=False,
        empty_label="— Choisir un produit —",
    )
    quantite = forms.IntegerField(min_value=1, required=False)

    class Meta:
        model = LigneVente
        fields = ['produit', 'quantite']
```

**Pourquoi redeclarer `produit` et `quantite` a la main au lieu de
laisser le `ModelForm` les generer automatiquement ?** C'est le piege
le plus instructif de ce module. Le modele `LigneVente` a
`quantite = models.PositiveIntegerField(default=1)`. Or Django
recopie automatiquement le `default` d'un champ de modele comme
`initial` du champ de formulaire correspondant. Consequence : dans un
formset ou l'on affiche 5 lignes vides "au cas ou" (voir etape 3),
chaque ligne vide aurait quand meme `quantite` pre-rempli a `1`, alors
que `produit` resterait vide. Django compare ensuite les valeurs
soumises aux valeurs initiales pour decider si une ligne a ete
"touchee" par l'utilisateur (`form.has_changed()`) ; avec `quantite`
toujours a `1`, **une ligne jamais touchee par l'utilisateur serait
quand meme consideree comme modifiee**, et Django exigerait alors un
produit ("Ce champ est obligatoire") sur des lignes que l'utilisateur
a legitimement laissees vides. En redeclarant les deux champs sans
`initial` et avec `required=False`, une ligne vraiment vide (aucun des
deux champs rempli) reste detectee comme "non modifiee" et le formset
la laisse tranquillement de cote.

La validation metier de la ligne se fait dans `clean()` :

```python
def clean(self):
    cleaned_data = super().clean()
    produit = cleaned_data.get('produit')
    quantite = cleaned_data.get('quantite')
    if produit and not quantite:
        raise forms.ValidationError("Indiquez une quantite pour ce produit.")
    if quantite and not produit:
        raise forms.ValidationError("Choisissez un produit pour cette ligne.")
    if produit and quantite and quantite > produit.stock:
        raise forms.ValidationError(
            f"Stock insuffisant pour {produit.nom} ({produit.stock} disponible(s))."
        )
    return cleaned_data
```

Trois regles : les deux champs doivent etre remplis ensemble ou pas du
tout, et la quantite demandee ne peut pas depasser le stock reellement
disponible — verifiee **cote serveur**, jamais seulement cote
JavaScript (un utilisateur malveillant peut toujours desactiver le
JS ou poster une requete directement).

## Etape 3 — Le formset et sa regle "au moins une ligne"

```python
class BaseLigneVenteFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        lignes_remplies = [
            form.cleaned_data for form in self.forms
            if form.cleaned_data and form.cleaned_data.get('produit')
        ]
        if not lignes_remplies:
            raise forms.ValidationError("Ajoutez au moins un produit a la vente.")

LigneVenteFormSet = inlineformset_factory(
    Vente, LigneVente,
    form=LigneVenteForm,
    formset=BaseLigneVenteFormSet,
    extra=5,
    can_delete=False,
)
```

`inlineformset_factory(Vente, LigneVente, ...)` fabrique une classe de
formset qui sait que chaque `LigneVente` doit etre reliee a une
`Vente` precise (via la `ForeignKey` du module 01). `extra=5` affiche
5 lignes vides par defaut — l'equivalent formulaire de "servez-vous,
remplissez celles dont vous avez besoin". La regle "au moins une
ligne remplie" ne peut pas se verifier ligne par ligne (chaque ligne
individuelle a le droit d'etre vide) : c'est une regle **sur
l'ensemble du panier**, donc on la place dans le `clean()` du formset
lui-meme, pas dans celui d'une ligne.

## Etape 4 — La vue : deux formulaires, une transaction

```python
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
    return render(request, 'ventes/form.html', {...})
```

Points a detailler avec les eleves :

- **`instance=vente` partage entre les deux formulaires.** `vente`
  est une instance `Vente()` pas encore enregistree (`pk=None`). Le
  formset est construit avec cette meme instance Python : quand
  `vente_form.save()` enregistre la vente et lui attribue un `pk`,
  l'objet `vente` (et donc `formset.instance`, qui pointe vers le meme
  objet) se retrouve automatiquement avec ce `pk` a jour — pas besoin
  de le re-assigner a la main.
- **`ligne.prix_unitaire = ligne.produit.prix` avant `save()`.** Le
  formulaire ne demande que `produit` et `quantite` (voir etape 2) :
  le prix unitaire n'est jamais saisi par l'utilisateur, il est
  toujours recopie depuis le prix **actuel** du produit au moment de
  la vente. C'est ce qui fige le prix sur la facture meme si le prix
  du produit change plus tard (`Produit.prix` a l'etape suivante peut
  evoluer sans jamais changer les factures deja emises).
- **La decrementation du stock est faite a la main**, pas par un
  signal Django : `produit.stock -= ligne.quantite`. C'est
  volontairement explicite pour que le lien "vendre un produit reduit
  son stock" soit visible directement dans le code de la vue, plutot
  que cache dans un signal declenche automatiquement ailleurs.
- **`transaction.atomic()`** garantit que soit toutes les operations
  reussissent ensemble (creer la vente, creer chaque ligne, decrementer
  chaque stock), soit aucune n'est appliquee. Sans ca, une erreur
  survenant apres la creation de 2 lignes sur 3 laisserait la base de
  donnees dans un etat incoherent (une vente avec seulement une partie
  de ses lignes).

## Etape 5 — Le template : afficher un formset

```django
<form method="post" class="pos-layout">
  {% csrf_token %}
  ...
  {{ formset.management_form }}
  {% for ligne_form in formset %}
    <div class="cart-item">
      {{ ligne_form.produit }}
      {{ ligne_form.quantite }}
    </div>
  {% endfor %}
```

`{{ formset.management_form }}` est **obligatoire** et facile a
oublier : elle genere des champs caches (`lignes-TOTAL_FORMS`,
`lignes-INITIAL_FORMS`...) qui disent a Django, au moment du POST,
combien de formulaires ont ete envoyes. Sans elle, Django ne sait pas
combien de `<div class="cart-item">` chercher dans les donnees
postees et le formset leve une erreur `ManagementForm data is
missing`.

## Testez

1. `/ventes/nouvelle/` : le catalogue de gauche liste les 6 produits
   actifs avec leur prix et leur stock. Le formulaire de droite montre
   5 lignes vides.
2. Laissez tout vide et cliquez "Encaisser" : vous devez voir l'erreur
   "Ajoutez au moins un produit a la vente."
3. Choisissez un produit sur la premiere ligne sans indiquer de
   quantite : "Indiquez une quantite pour ce produit."
4. Choisissez un produit en rupture (Paracetamol) avec une quantite de
   5 : "Stock insuffisant pour Paracetamol 500mg (0 disponible(s))."
5. Remplissez correctement 2 lignes et validez : vous devez etre
   redirige vers la facture generee, avec le bon total, et le stock
   des produits vendus doit avoir diminue (verifiable sur `/produits/`
   ou `/stock/`).

Passez au [module 07](07-factures.md).
