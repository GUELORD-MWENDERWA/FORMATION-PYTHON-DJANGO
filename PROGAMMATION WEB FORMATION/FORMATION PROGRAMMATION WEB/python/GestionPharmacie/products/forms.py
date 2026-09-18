from django import forms

from .models import Client, Produit, Client, Fournisseur, Vente, LigneVente
from django.forms import BaseInlineFormSet, inlineformset_factory 

class ProduitForm(forms.ModelForm):
   class Meta:
      model = Produit
      fields = [
         'nom', 'categorie', 'fournisseur', 'prix', 'prix_achat',
         'stock', 'seuil_alerte', 'lot', 'date_peremption', 'actif',
         'image', 'description'
      ]
      widgets = {
         'date_peremption': forms.DateInput(attrs={'type': 'date'}),
         'description': forms.Textarea(attrs={
            'placeholder': 'Composition, Posologie, precautions d\'emploi ....',
            }),
      }


class ClientForm(forms.ModelForm):
   class Meta:
      model = Client
      fields = ['nom', 'prenom', 'email', 'telephone', 'adresse',
                'date_naissance', 'note'
                ]
      widgets = {
         'adresse': forms.Textarea(attrs={
            'placeholder': 'Adresse du client',
            }),

         'date_naissance': forms.DateInput(attrs={'type': 'date'}),
         'notes': forms.Textarea(attrs={
            'placeholder': 'Information utile pour le  pharmacien',
            }),
      }

class FournisseurForm(forms.ModelForm):   
   class Meta:
      model = Fournisseur
      fields = ['nom', 'telephone', 'email', 'adresse', 'notes', 'actif','contact']
      widgets = {
         'adresse': forms.Textarea(attrs={
            'placeholder': 'Adresse du fournisseur',
            }),
         'notes': forms.Textarea(attrs={
            'placeholder': 'Condition de paiement, delais de livraison, ...',
            }),
      }

class VenteForm(forms.ModelForm):
   class Meta:
      model= Vente   
      fields =['client', 'mode_paiement', 'remise']

   def __int__(self, *args, **kwargs):
      super().__init__(*args, **kwargs) 
      self.fields['client'].empty_label  = "Client de passage"


class LigneVenteForm(forms.ModelForm):
   produit = forms.ModelChoiceField(
      queryset=Produit.objects.all(), required=False,
      empty_label="-- Choisir un produit --", 
   )
   quantite = forms.IntegerField(min_value=1, required=False)

   class Meta:
      model: LigneVente
      fields =  ['produit', 'quantite']

   def clean(self):
      cleaned_data = super().clean
      produit = cleaned_data.get('produit')
      quantite = cleaned_data.get('quantite')
      if produit and not quantite:
         raise forms.ValidationError("Indiquer une  quantinte pour ce produit.")
      if quantite and not produit:
         raise forms.ValidationError("Choisissez un produit pour cette ligne")
      if produit and quantite and quantite > produit.stock:
         raise forms.ValidationError(
            f"Stock insuffisant pour {produit.nom} "
            f"({produit.stock}) disponible"
         )
      return cleaned_data

class BaseLigneVenteFormSet(BaseInlineFormSet):
   def clean(self):
      if any(self.errors):
         return
      lignes_remplies = [
         form.cleaned_data for form in self.forms 
         if form.cleaned_data and form.cleaned_data.get('produit')
      ]

LigneVenteFormSet =  inlineformset_factory(
   Vente, LigneVente,
   form=LigneVenteForm,
   formset=BaseLigneVenteFormSet,
   extra=5,
   can_delete=False,
)