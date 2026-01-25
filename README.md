# TBA - Hollow Knight

Ce repo contient une version du jeu d’aventure TBA reprenant les idées du jeu **Hollow Knight**.

## Description de l'univers

 Le jeu se déroule dans le royaume souterrain d'Hallownest. Vous pourrez vous aventurer dans 12 lieux souterrains différents :
 - Falaises hurlantes
 - Dirtmouth
 - Mont Cristal
 - Vertchemin
 - Routes oubliées
 - Temple de l'oeuf noir
 - Lac Bleu
 - Brumes Canyon
 - Caverne nocive
 - Cité des Larmes
 - Village des Mantes 
 - Nid profond

 Le joueur incarne **Quirrel**, un voyageur amnésique explorant le royaume d'**Hallownest**. Le joueur progresse en explorant les lieux tels que des cavernes obscures, des ruines remplies d'ennemis, des temples scellés par des forces anciennes. 


## Structuration

Il y a 8 modules contenant chacun une classe et 1 module contenant deux classes.

- `game.py` / `Game` : description de l'environnement, interface avec le joueur ;
- `room.py` / `Room` : propriétés génériques d'un lieu  ;
- `player.py` / `Player` : le joueur ;
- `command.py` / `Command` : les consignes données par le joueur ;
- `actions.py` / `Action` : les interactions entre ;
- `item.py` / `Item` : la gestion des objets ;
- `character.py` / `Character` : les PNJ pacifiques et hostiles ;
- `door.py` / `Door` : accès à certaines portes sous condition ;
- `quest.py` / `Quest`,`QuestManager` : les quêtes à accomplir et les récompenses obtenues.


## Objectif du jeu

L'objectif final du jeu est de vaincre le **Hollow Knight** afin de déterminer le destin du royaume.
Pour y parvenir, Quirrel doit faire attention autour de lui et doit :
- explorer les différentes régions ;
- accomplir toutes les quêtes ;
- avant de débloquer l'accès au **Temple de l'oeuf Noir** pour sauver le royaume d'Hallownest.


## Condition de victoire et de défaite

- Le joueur **gagne** lorsque le **Hollow Knight** est vaincu au **Temple de l'oeuf Noir**.
L'accès au Temple de l'oeuf Noir, là où se trouve le boss final, est bloqué tant que toutes les quêtes ne sont pas complétées.

- Le joueur **perd** s'il engage un combat contre un ennemi hostile dont le niveau est strictement supérieur à celui de Quirrel. 
La mort met fin à la partie.


## Déplacement et exploration
Quirrel se situe dans les sous-terrains profonds d'Hallownest. Pour explorer les différents lieux du royaume, vous pouvez vous déplacer selon quatre directions : Haut Bas Ouest Est (Up, Down, O, E).

Certaines zones :
- nécessitent des objets spécifiques (les portes sont verrouillées sans ces objets).
- sont inaccessibles tant que certaines quêtes ne sont pas terminées. 
- peuvent être plongées dans l’obscurité. (Vous ne pourrez alors pas apercevoir l'inventaire de la pièce sans l'item spécifique : la lanterne)


## Système de quêtes

Le jeu intègre un système de quêtes composé de :
- quête d'items : récupérer un objet spécifique dans une pièce donnée ;
- quête de déplacement : visiter une pièce spécifique ;
- quête de combat : vaincre un PNJ spécifique ;
- quête d’interaction : interagir avec un PNJ spécifique.

L'accomplissement de toutes les quêtes est indispensable pour accéder au boss final situé à Temple de l'oeuf Noir et terminer le jeu.


## Commandes disponibles

- `help` : Affiche la liste des commandes;
- `go` direction : se déplacer dans une direction cardinale;
- `history` : afficher l'historique des pièces visitées;
- `back` : revenir dans la salle précédente;
- `look` : regarder les items présents dans la salle;
- `take` item : prendre un objet;
- `drop` item : déposer un objet;
- `check` : vérifier l'inventaire du joueur;
- `talk` ou `talk` pnj : parler à un PNJ;
- `fight` : combattre un ennemi;
- `quests` : afficher la liste des quêtes;
- `quest` titre : afficher les détails de la quête;
- `activate` titre : activer une quête;
- `rewards` : afficher les récompenses obtenues;
- `sell` ou `sell` item : vendre un objet;
- `buy` ou `buy` item : acheter un objet;
- `train` : s'entrainer auprès d'un maître;
- `upgrade` : améliorer une arme auprès d'un forgeron;
- `quit` : quitter le jeu.


## Perspectives de développement
- Ajouter un inventaire dans l'inventaire. Parmi nos items, il y avait des reliques tels que le journal du vagabond, le sceau d'hallownest, l'idole du roi et l'oeuf arcanique. Il serait interessant d'ajouter une mallette dans l'inventaire et d'ajouter une condition `relique=True` pour que les reliques soient placées dans la mallette.
- Faire en sorte que certains PNJ hostile deviennent non hostiles apres les avoir combattus. A l'inverse, faire en sorte que des PNJ non hostile le deviennent après certains événements.
- Ajouter de la stratégie au système de combat (attack/defense).
- Ajouter des dialogues interactives, où l'on peut choisir sa réponse ou bien ses questions.






