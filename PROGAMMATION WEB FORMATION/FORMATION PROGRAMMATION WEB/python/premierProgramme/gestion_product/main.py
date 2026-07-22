#nom du produit, prix du produit, Quantite et le total a la fin
#for

#while

listeProduct = []
listPrice = []
listQuantinty = []
listTotalPrice = []

nombreElement = int(input("voulez vous completer combien de produit ? "))

if(nombreElement < 1):
    print("DESOLER LE NOMBRE DE PRODUIT ENTRER EST INVALIDE ")

else:   
    for produit in range(nombreElement):
        print("entrer le nom du produit ")
        listeProduct.append(input()) 

    for indice, produit in enumerate(listeProduct):
        print("entrer le prix de", produit)
        listPrice.append(float(input()))

        print("entrer la quantinte de", produit)
        listQuantinty.append(int(input()))
        
        #on fait le total pour un element 
        total = float(listPrice[indice]*listQuantinty[indice])
        listTotalPrice.append(total)
        



"""
no  produit   prix unt  Qte  prix tot
1   mangue     3400      2    6800
2   avocat     4500      2    9000
"""
print(listeProduct)
print(listPrice)
print(listQuantinty)
print(listTotalPrice)