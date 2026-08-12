from django.db import models

# Create your models here.
#
# C'est ici que se definiront les "models" de l'application, la partie
# M du schema MVT (Model - View - Template) : chaque classe heritant de
# models.Model represente une table de la base de donnees, et chaque
# attribut (models.CharField, models.DecimalField, ...) une colonne.
# Exemple pour ce projet : class Produit(models.Model): nom =
# models.CharField(max_length=100), prix = models.DecimalField(...),
# stock = models.IntegerField(...), etc.
#
# Tant qu'aucun modele n'est ecrit ici, les vues de views.py ne peuvent
# afficher que des templates statiques (voir products/views.py) : c'est
# l'etat actuel du projet. Des qu'un modele sera ajoute, il faudra
# generer et appliquer une migration pour creer la table correspondante
# dans db.sqlite3 :
#   python manage.py makemigrations
#   python manage.py migrate
