# TBA - Hollow Knight

Ce repo contient la première version (minimale) du jeu d’aventure TBA.

## Description de l'univers

 Le jeu se déroule dans le royaume souterrain d'Hallownest. Vous pourrez vous aventurer dans 12 lieux souterrains différents :
 - Howling Cliffs
 - Dirtmouth
 - Crystal Peak
 - Greenpath
 - Forgotten Crossroads
 - Temple of the Black Egg
 - Blue Lake
 - Fog Canyon
 - Fungal Wastes
 - City of Tears
 - Mantis Village
 - Deepnest

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
- avant de débloquer l'accès au **Temple of the Black Egg** pour sauver le royaume d'Hallownest.

## Condition de victoire et de défaite

- Le joueur gagne lorsque le **Hollow Knight** est vaincu à **Temple of the Black Egg**
L'accès au Temple of the Black Egg, là où se trouve le boss final est bloqué tant que toutes les quêtes ne sont pas complétées.

- Le joueur perd s'il engage un combat contre un ennemi hostile dont le niveau est strictement supérieur à celui de Quirrel. 
La mort met fin à la partie.


