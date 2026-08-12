# 05 — Clients et Fournisseurs (repeter le patron CRUD)

Fichiers concernes : `products/forms.py` (`ClientForm`,
`FournisseurForm`), `products/views.py` (sections *Clients* et
*Fournisseurs*), `clients/*.html`, `fournisseurs/*.html`

## Objectif du module

Appliquer, sans surprise, exactement le meme patron que le module 03
(formulaire + vue creation/edition + vue suppression + boucle dans le
template) a deux nouveaux modeles. C'est fait expres : une fois
qu'on a compris le CRUD une fois, le repeter est mecanique. Notez a
quel point `clients_form` et `fournisseurs_form` dans `views.py`
ressemblent a `produits_form` — seuls le modele et le formulaire
changent.

C'est aussi l'occasion d'introduire une nuance : **quand est-ce qu'on
extrait une fonction generique au lieu de repeter le patron ?** Avec
seulement 3 modeles suivant ce patron, dupliquer reste plus lisible
qu'une usine a gaz generique (`generic_crud_view(model, form_class,
...)`). Si vous ajoutez un 4e ou 5e module suivant exactement le meme
schema (voir l'exercice "Commandes" du module 09), c'est le bon moment
pour montrer aux eleves les vues generiques bassees sur les classes de
Django (`ListView`, `CreateView`, `UpdateView`, `DeleteView`) — hors
perimetre de ce cours pour rester sur des vues fonctions, plus simples
a lire pour un premier contact avec Django.

## Ce qui differe legerement : les annotations sur la liste Clients

```python
def clients_liste(request):
    clients = Client.objects.annotate(
        nb_achats=Count('ventes'),
        dernier_achat=Max('ventes__date'),
    )
    return render(request, 'clients/liste.html', {'clients': clients})
```

Les colonnes "Achats" et "Dernier achat" du tableau (deja presentes
dans le HTML d'origine, avec des valeurs figees) sont calculees
directement en base de donnees via `Count` et `Max` sur la relation
inverse `client.ventes` (le `related_name='ventes'` defini sur
`Vente.client` au module 01). Comme pour `total_ventes` sur les
produits (module 03), c'est le meme principe : laisser la base de
donnees agreger, plutot que de boucler en Python sur toutes les
ventes de chaque client.

## Le champ `actif` (BooleanField) sur Fournisseur

```python
class Meta:
    model = Fournisseur
    fields = ['nom', 'contact', 'telephone', 'email', 'adresse', 'notes', 'actif']
```

Le mockup HTML d'origine utilisait un `<select><option>Actif</option>
<option>Desactive</option></select>` pour le statut. Le `ModelForm`
genere a la place une case a cocher (`actif` est un `BooleanField`
sur le modele) : c'est plus idiomatique en Django (un booleen reste
un booleen de bout en bout, pas une chaine "Actif"/"Desactive" a
reinterpreter), mais visuellement different du mockup — un compromis
assume plutot que de forcer un `<select>` a la main pour un simple
vrai/faux.

## Testez

1. `/clients/` : 4 clients, avec un nombre d'achats et une date de
   dernier achat coherents avec les ventes de la fixture (module 02).
2. `/fournisseurs/` : 3 fournisseurs, dont un affiche "Inactif"
   (SantePlus Grossiste dans la fixture).
3. Creez, modifiez puis supprimez un client de test — verifiez que
   les messages de confirmation (vert) apparaissent a chaque etape
   (voir module 08 pour le detail de ce mecanisme).

Passez au [module 06](06-ventes-et-formsets.md), le plus consequent du
cours.
