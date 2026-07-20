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
liste = []

for i in range(10):
   print("entrer le nom du ", i+1, "produit")
   liste[i] = input()


liste1 = [2,34, 234, 345, 345, 883, "mangue", "avovat"]

for element in liste1:
   print(element)

