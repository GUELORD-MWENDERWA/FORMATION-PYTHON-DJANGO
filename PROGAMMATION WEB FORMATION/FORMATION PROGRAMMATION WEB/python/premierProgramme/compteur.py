LARGEUR_BORDURE = 72

produit = [ "mangue", "avocat"]
price = [200, 500]
quantity = [2,4]
total = [223, 454]

print("*" * LARGEUR_BORDURE)
print(f"* {'N°':<5} * {'Produit':<15} * {'Prix Unitaire':<15} * {'Quantité':<10} * {'Prix Total':<10} *")
print("*" * LARGEUR_BORDURE)

for indice, elements in enumerate(produit):
   #nombre = indice + 1
   print(f"* {indice +1:<5} * {elements:<15} * {price[indice]:<15} * {quantity[indice]:<10} * {total[indice]:<10} *")
print("*" * LARGEUR_BORDURE)