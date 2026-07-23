#LES VARIABLEES ET DECLAATION

"""
premierNombre = int(input('entrer le premer nombre '))
deuxiemeNombre = int(input("entrer le deuxieme nombre "))
somme = 0
division = 0


somme = float(premierNombre + deuxiemeNombre)
division = int(premierNombre/ deuxiemeNombre)



print("la somme de " , premierNombre , " et " , deuxiemeNombre, " egal a " , somme)
print("la division de " , premierNombre , " avec " , deuxiemeNombre, " fait " , division)
"""
"""
# commentaire sur une seule ligne 
name = input("quel est votre nom ? ")
postName = input("quel est votre postnom ? ")
age = int(input("quel est votre age "))


if age == 39:
   print("votre nom est ", name, "", postName, "et vous etes proche de la quarantaine")

elif age == 30:
    print("votre nom est ", name, "", postName, "et vous etes vieux")

if age < 18:
   print("votre nom est ", name, "", postName, "et vous etes mineur")
else:
   print("DESOLER VOTRE AGE N'EST PAS VAILDE")
"""
"""
liste = []

for i in range(10):
   print("entrer le nom du ", i+1, "produit")
   liste[i] = input()


liste1 = [2,34, 234, 345, 345, 883, "mangue", "avovat"]

for element in liste1:
   print(element)

"""

#nom du produit, prix du produit, Quantite et le total a la fin
#for

#while

from xml.etree.ElementTree import Element


listeProduct = []
listPrice = []
listQuantinty = []
listTotalPrice = []
elementEntry = ""

while True:
   print("entrer le nom d'un produit ou saisisez '-1' pour arreter" )
   elementEntry = input().strip().upper()
  
   if elementEntry == "":
       print("le nom d'un element ne doit pas etre vide svp !!!" )
       continue
         
   elif elementEntry == "-1":
      print("voici les produits completer")
      """
      ==========================================
      = no  produit   prix unt  Qte  prix tot  =
      =  1   mangue     3400      2    6800    =
      =  2   avocat     4500      2    9000    =
     """
      print(listeProduct)
      print(listPrice)
      print(listQuantinty)
      print(listTotalPrice)
      break

   else:   
      listeProduct.append(elementEntry)
      print("entrer le prix de", elementEntry)
      price = float(input())
      listPrice.append(price)

      print("entrer la quantinte de", elementEntry)
      quantinty  = int(input())
      listQuantinty.append(quantinty)
      
      #on fait le total pour un element 
      total = float(price*quantinty)
      listTotalPrice.append(total)
        

def printUser(utilisateur):
   if(utilisateur == ""):
      print('le nom doit etre completer')
   else:
      print("bonjour", utilisateur)

def comptNombre(rang):
   for nombre in range(rang):
      print(nombre)

