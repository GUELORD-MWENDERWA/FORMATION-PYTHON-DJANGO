listeProduct = []
listPrice = []
listQuantinty = []
listTotalPrice = []

while True:
    print("Entrer le nom d'un produit ou saisissez '-1' pour arrêter :")
    nom_produit = input().strip()
  
    if nom_produit == "":
        print("Le nom d'un produit ne doit pas être vide svp !!!")
        continue
         
    elif nom_produit == "-1":
        
      if len(listeProduct) == 0:
         print("Aucun produit n'a été enregistré.")
         while True:
            print("voulez vous arreter taper 'A/a' ou enregistré un produit ? taper 'E/e'")
            reponse = input().strip().lower()
         if reponse == "a":
            break
         elif reponse == "e":
            continue
         break
      
        
      print("\nVoici les produits complétés :")
      LARGEUR_BORDURE = 71
        
      # Affichage de l'en-tête du tableau
      print("*" * LARGEUR_BORDURE)
      print(f"* {'N°':<5} * {'Produit':<15} * {'Prix Unitaire':<15} * {'Quantité':<10} * {'Prix Total':<10} *")
      print("*" * LARGEUR_BORDURE)
      
      # Affichage des lignes de données
      for i in range(len(listeProduct)):
         numero = i + 1
         print(f"* {numero:<5} * {listeProduct[i]:<15} * {listPrice[i]:<15.2f} * {listQuantinty[i]:<10} * {listTotalPrice[i]:<10.2f} *")
      
      print("*" * LARGEUR_BORDURE)
      break

    else:   
        listeProduct.append(nom_produit)

        print(f"Entrer le prix de {nom_produit} :")
        prix = float(input())
        listPrice.append(prix)

        print(f"Entrer la quantité de {nom_produit} :")
        quantite = int(input())
        listQuantinty.append(quantite)
         
        total = prix * quantite
        listTotalPrice.append(total)



