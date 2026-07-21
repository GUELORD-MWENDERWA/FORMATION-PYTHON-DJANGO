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

    for produit in listeProduct:
        print("entrer le prix de", produit)
        listPrice.append(input())

        print("entrer la quantinte de", produit)
        listQuantinty.append(input())

        listTotalPrice += listPrice[-1] * listQuantinty[-1]
        

    print(listeProduct)
    print(listPrice)
    print(listQuantinty)
    print(listQuantinty)