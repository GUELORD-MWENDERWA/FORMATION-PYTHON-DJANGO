# Prompt de reproduction (a coller tel quel dans un autre outil IA)

Ce prompt sert quand un AUTRE outil/IA (pas Claude Code sur ce repo)
doit generer ou modifier des pages de GestionPharmacie et doit
reproduire EXACTEMENT le meme resultat visuel/structurel que
l'existant, sans y avoir directement acces. Copier-coller le bloc
ci-dessous tel quel. Le garder synchronise si le design evolue.

---

```
Tu construis/modifies des pages pour "GestionPharmacie", une application web de
gestion de pharmacie (Django, templates HTML + un seul fichier CSS custom, pas de
framework CSS, pas de librairie JS). Respecte EXACTEMENT la structure suivante,
sans rien inventer ni simplifier : le but est un rendu identique a l'existant,
pas une interpretation libre.

=== 1. STRUCTURE GENERALE DE LA PAGE ===

La page est un "app shell" a deux zones cote a cote :
- Une colonne laterale GAUCHE FIXE ("sidebar"), largeur 200px, qui ne defile jamais
  et reste identique sur toutes les pages de l'application.
- Une zone de CONTENU a droite, qui occupe le reste de la largeur. C'est LA SEULE
  partie qui change d'une page a l'autre, et c'est la SEULE partie qui defile
  verticalement (un seul conteneur de scroll par page, jamais de zone qui reste
  coupee sans moyen de la voir en entier).

Ces deux zones sont posees dans un conteneur central max-width: 2000px, centre
horizontalement (margin: 0 auto), occupant toute la hauteur de l'ecran (100dvh),
avec un fond legerement encadre (border-radius: 4px, une ombre douce autour).

=== 2. LE MENU LATERAL (SIDEBAR) — CONTENU EXACT ===

De haut en bas :

1. Un logo en haut (icone SVG, une forme de mortier/pilule ou equivalent, couleur
   qui suit le texte du sidebar), dans un bloc "sidebar-header".
2. Une liste de navigation, DANS CET ORDRE EXACT, avec une icone line-style
   (feather icons : SVG 24x24, stroke="currentColor", stroke-width="2", pas de
   remplissage) a gauche de chaque libelle :
     1. Accueil        (icone maison)       -> tableau de bord
     2. Produits        (icone sac)          -> liste des produits
     3. Stock            (icone paquet/boite) -> etat des stocks
     4. Ventes           (icone panier)       -> historique des ventes + point de vente
     5. Clients          (icone personnes)    -> fichier clients
     6. Fournisseurs     (icone camion)       -> fichier fournisseurs
     7. Factures         (icone document)     -> factures emises
     8. Statistiques     (icone camembert)    -> rapports / indicateurs
     9. Notifications    (icone cloche)       -> alertes stock/peremption
    10. Parametres       (icone engrenage)    -> reglages de la pharmacie/compte
   Ne pas ajouter, retirer, fusionner ou reordonner ces entrees sans qu'on le
   demande explicitement. L'element de la liste qui correspond a la page
   actuellement affichee est visuellement actif : fond legerement plus clair
   (ou plus fonce selon le theme) + une petite barre verticale coloree (couleur
   d'accent) collee au bord droit de l'item.
3. Tout en bas de la sidebar (margin-top: auto, colle au bas) : un bloc "compte
   connecte" avec, sur une ligne : une photo de profil ronde (32x32, object-fit:
   cover), le nom de l'utilisateur a cote (ex. "Monica G."), et un bouton
   "..." (trois points horizontaux) tout a droite pour un futur menu de compte.

Ce menu lateral est identique sur TOUTES les pages de l'application (inclus une
seule fois dans un gabarit de base, jamais duplique/re-genere par page).

=== 3. THEME CLAIR / SOMBRE ===

L'application demarre en theme SOMBRE par defaut, avec un bouton bascule
(icone lune) present dans l'en-tete de chaque page de contenu (pas dans la
sidebar). Toutes les couleurs viennent de variables CSS (custom properties),
jamais de couleurs codees en dur dans un composant, pour que le bouton puisse
tout re-theme-r d'un coup en ajoutant une classe "light" sur <html>.

Palette exacte a utiliser :

  Sombre (par defaut)                          Clair (classe .light)
  --app-bg: #101827                            #ffffff
  --sidebar: rgba(21,30,47,1)                  #f3f6fd
  --sidebar-main-color: #ffffff                #1f1c2e
  --sidebar-link: #ffffff                      #1f1c2e
  --sidebar-hover-link: #1a2539                 rgba(195,207,244,.5)
  --sidebar-active-link: #1d283c                rgba(195,207,244,1)
  --app-content-main-color: #ffffff             #1f1c2e
  --app-content-secondary-color: #1d283c        #f3f6fd   (fond des cartes/tableaux)
  --action-color: #2869ff                       #2869ff   (couleur d'accent/liens/CTA)
  --action-color-hover: #6291fd                 #6291fd
  --table-border: #1a2131                       #1a2131
  --status-warning: #d69a2d
  --status-danger: #e0555f
  --status-info: #2869ff

Police : "Poppins" (Google Fonts, graisses 300/400/500). Coins arrondis 4px
presque partout (8px seulement pour la carte de connexion et les cartes produit
en mode grille).

=== 4. EN-TETE DE CHAQUE PAGE DE CONTENU ===

En haut de la zone de contenu (pas dans la sidebar), sur chaque page :
[titre de la page <h1>] ................ [bouton bascule theme] [bouton
d'action principal si pertinent, ex. "Ajouter un produit"]
Sur les pages de formulaire ou de detail, ajouter en plus a l'extreme gauche
un bouton "retour" (fleche gauche) qui ramene vers la page de liste du module —
JAMAIS de bouton "Annuler" qui ne fait rien : c'est toujours un vrai lien vers
la liste parente.
Cet en-tete reste visible en haut de l'ecran meme quand on fait defiler le
contenu de la page (position sticky), sur fond identique au fond de page pour
ne pas laisser voir le contenu passer "a travers".

=== 5. CARTES vs TABLEAUX — REGLE IMPORTANTE ===

NE PAS transformer les listes de donnees en cartes. La regle est :

- Cartes ("stat-cards") : UNIQUEMENT pour les indicateurs chiffres du tableau
  de bord et de la page statistiques (ex. "128 produits references", "24 ventes
  aujourd'hui", "842 € de chiffre d'affaires", "7 produits en alerte"). Une carte
  = une icone coloree + une grande valeur + un petit libelle. 4 par ligne sur
  grand ecran, 2 sur tablette, 1 sur mobile.
- TABLEAUX : pour TOUTES les listes de donnees metier — clients, fournisseurs,
  ventes, factures, stock. Chaque ligne = une entite, chaque colonne = un champ.
  Une ligne d'en-tete de colonnes en haut (fond legerement different). PAS de
  carte par client/vente/facture/fournisseur/produit-en-stock — ce sont des
  lignes de tableau, en colonnes, pas des vignettes.
  Exception : la page "Produits" propose EN PLUS un bouton bascule optionnel
  liste/grille (icone liste vs icone grille) qui permet de basculer en mode
  "cartes produit" avec photo — mais le mode par defaut a l'ouverture de la
  page reste la vue TABLEAU. Ne pas appliquer ce bouton bascule aux autres
  modules (clients, ventes, fournisseurs, factures, stock restent en tableau
  uniquement, pas de bascule carte).
- Sur petit ecran, ne PAS remplacer un tableau par des cartes empilees : reduire
  plutot le nombre de colonnes visibles (masquer les colonnes secondaires) et
  garder le format tableau/lignes.

=== 6. CHAQUE MODULE = SES PROPRES PAGES SEPAREES ===

Ne jamais regrouper plusieurs modules sur une seule page. Chaque module (Produits,
Stock, Ventes, Clients, Fournisseurs, Factures, Statistiques, Notifications,
Parametres) a ses propres URLs et pages dediees, typiquement :
  - une page LISTE (tableau + barre de recherche + bouton "Ajouter un X")
  - une page FORMULAIRE (ajout / modification), reutilisee pour les deux cas
  - une page DETAIL en lecture seule pour les entites qui en ont besoin
    (ex. le detail d'une facture, pensee pour etre imprimee)
Le tableau de bord (page d'accueil) est la seule page qui resume plusieurs
modules a la fois (chiffres cles en cartes + 2 listes courtes "Ventes recentes"
/ "Alertes" avec un lien "Voir tout" vers la vraie page liste du module).

=== 7. FORMULAIRES ===

Une carte (fond --app-content-secondary-color, padding genereux) contenant une
grille de champs sur 2 colonnes (1 colonne sur mobile), chaque champ = un label
au-dessus d'un input/select/textarea. Les champs qui doivent prendre toute la
largeur (description, notes, adresse longue) s'etendent sur les 2 colonnes.
En bas du formulaire : bouton secondaire "Annuler" (lien vers la liste) a
gauche du bouton principal "Enregistrer" (submit) — alignes a droite.

=== 8. COMPORTEMENT RESPONSIVE / MOBILE — OBLIGATOIRE ===

- En dessous de 1024px de large, la sidebar NE DISPARAIT PAS purement et
  simplement : elle devient un tiroir (panneau qui glisse depuis la gauche,
  par-dessus le contenu, avec un fond assombri cliquable derriere pour le
  refermer). Un bouton "hamburger" (trois traits horizontaux), TOUJOURS visible
  en haut de chaque page dans une petite barre fixe (avec le nom/logo de
  l'appli a cote), ouvre ce tiroir. Le tiroir se ferme au clic sur le fond
  assombri, sur une croix dans son propre en-tete, avec la touche Echap, ou des
  qu'on choisit un lien du menu. La navigation ne doit JAMAIS etre totalement
  inaccessible sur un petit ecran.
- Chaque page doit rester scrollable jusqu'a son dernier element sur tous les
  formats d'ecran, y compris sans ecran tactile (molette, barre de defilement
  visible, navigation clavier) — jamais de contenu coupe sans moyen de le voir.
- Points de rupture a reutiliser tels quels : 1024px (bascule sidebar/tiroir),
  900px (mise en page point de vente 2 colonnes -> 1), 820px (2 panneaux du
  tableau de bord -> 1), 780px (texte des tableaux plus petit), 620px (grille
  de formulaire 2 colonnes -> 1), 520px (cartes stats et barre de recherche
  empilees), 480px (masquer une colonne de tableau supplementaire).

=== 9. CE QU'IL NE FAUT PAS FAIRE ===

- Ne pas utiliser un framework CSS (Bootstrap/Tailwind) ni une librairie de
  composants : tout est en CSS custom avec variables, coherent avec l'existant.
- Ne pas remplacer les icones par une police d'icones ou une librairie externe :
  SVG inline "feather style" uniquement.
- Ne pas faire disparaitre la navigation sur mobile sans remplacement.
- Ne pas transformer les listes de donnees en cartes (voir section 5).
- Ne pas laisser un bouton "Annuler"/"Retour" sans lien reel.
- Ne pas dupliquer le contenu de la sidebar par page : un seul gabarit de base
  partage par toutes les pages.
```

---

## Notes pour toi (Claude Code, dans ce repo)

Si l'utilisateur demande de faire evoluer ce prompt, garder ce fichier
synchronise avec `architecture.md`, `components.md` et
`design-tokens.md` — ce prompt en est un resume "portable" destine a
un outil externe qui n'a pas acces au code source du projet.
