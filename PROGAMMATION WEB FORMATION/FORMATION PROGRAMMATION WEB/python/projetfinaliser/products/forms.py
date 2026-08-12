from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory

from .models import Client, Fournisseur, LigneVente, Produit, Vente


class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = [
            'nom', 'categorie', 'fournisseur', 'prix', 'prix_achat',
            'stock', 'seuil_alerte', 'lot', 'date_peremption', 'actif',
            'image', 'description',
        ]
        widgets = {
            'date_peremption': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={
                'placeholder': 'Composition, posologie, precautions d\'emploi...',
            }),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'nom', 'prenom', 'telephone', 'email',
            'date_naissance', 'adresse', 'notes',
        ]
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={
                'placeholder': 'Informations utiles pour le pharmacien',
            }),
        }


class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['nom', 'contact', 'telephone', 'email', 'adresse', 'notes', 'actif']
        widgets = {
            'notes': forms.Textarea(attrs={
                'placeholder': 'Conditions de livraison, delais habituels...',
            }),
        }


class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ['client', 'mode_paiement', 'remise']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].empty_label = "Client de passage"


class LigneVenteForm(forms.ModelForm):
    # Champs redeclares explicitement (sans `initial` recopie du modele) :
    # sinon `quantite` (qui a default=1 sur le modele) serait toujours
    # considere "rempli", et une ligne du formset laissee vide par
    # l'utilisateur ne serait plus jamais reconnue comme vide.
    produit = forms.ModelChoiceField(
        queryset=Produit.objects.all(), required=False,
        empty_label="— Choisir un produit —",
    )
    quantite = forms.IntegerField(min_value=1, required=False)

    class Meta:
        model = LigneVente
        fields = ['produit', 'quantite']

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
                f"Stock insuffisant pour {produit.nom} "
                f"({produit.stock} disponible(s))."
            )
        return cleaned_data


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
