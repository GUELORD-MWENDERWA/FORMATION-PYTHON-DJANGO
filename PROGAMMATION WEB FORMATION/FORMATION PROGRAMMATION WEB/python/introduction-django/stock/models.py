from django.db import models

# Create your models here.
class Produit(models.Model):
      nom = models.CharField(max_length=100)
      description = models.TextField()
      prix = models.DecimalField(max_digits=10, decimal_places=2)
      quantite = models.IntegerField()
      is_actif = models.BooleanField(default=False)

      class Meta:
         verbose_name = "Produit"
         verbose_name_plural = "Produits"

      def __str__(self):
         return self.nom