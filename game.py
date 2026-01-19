# Description: Game class
import random

# Import modules
from pathlib import Path
import sys

# Tkinter imports for GUI
import tkinter as tk
from tkinter import ttk, simpledialog

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character
from door import Door
from quest import Quest 

class Game:
    """The Game class manages the overall game state and flow."""

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.characters = []
        self.player = None
        self.items = {}

    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (Up, E, Down, O)", Actions.go, 1)
        self.commands["go"] = go
        history = Command("history", " : afficher l'historique des pièces visitées", Actions.history, 0)
        self.commands["history"] = history
        back = Command("back", " : revenir dans la salle précédente", Actions.back, 0, consumes_turn=False)
        self.commands["back"] = back
        look = Command("look", " : regarder les items présents dans la salle", Actions.look, 0, consumes_turn=False)
        self.commands["look"] = look
        take = Command("take", " <item> : prendre un objet", Actions.take, 1, consumes_turn=True)
        self.commands["take"] = take
        drop = Command("drop", " <item> : déposer un objet", Actions.drop, 1, consumes_turn=True)
        self.commands["drop"] = drop
        check = Command("check", " : vérifier l'inventaire du joueur", Actions.check, 0, consumes_turn=False)
        self.commands["check"] = check
        talk = Command("talk"," : parler à un PNJ", Actions.talk, 1, consumes_turn=False)
        self.commands["talk"] = talk
        fight = Command("fight"," : combattre un ennemi", Actions.fight, 1, consumes_turn=True)
        self.commands["fight"] = fight
        self.commands["quests"] = Command("quests"
                                          , " : afficher la liste des quêtes"
                                          , Actions.quests
                                          , 0)
        self.commands["quest"] = Command("quest"
                                         , " <titre> : afficher les détails d'une quête"
                                         , Actions.quest
                                         , 1)
        self.commands["activate"] = Command("activate"
                                            , " <titre> : activer une quête"
                                            , Actions.activate
                                            , 1)
        self.commands["rewards"] = Command("rewards"
                                           , " : afficher vos récompenses"
                                           , Actions.rewards
                                           , 0)
        sell = Command("sell", " : vendre un objet", Actions.sell, 0, consumes_turn=False)
        self.commands["sell"] = sell
        buy = Command("buy", " : acheter un objet", Actions.buy, 0, consumes_turn=False)
        self.commands["buy"] = buy
        train = Command("train", " : s'entraîner auprès d'un maître", Actions.train, 0, consumes_turn=False)
        self.commands["train"] = train
        upgrade = Command("upgrade", " : améliorer une arme auprès d'un forgeron", Actions.upgrade, 0, consumes_turn=False)
        self.commands["upgrade"] = upgrade


        # Setup rooms

        howling_cliffs = Room("Howling Cliffs", "non loin des frontières du royaume située au nord-ouest. Les falaises hurlantes n'ont pas l'air peuplées du tout.")
        self.rooms.append(howling_cliffs)
        self.dirtmouth = Room("Dirtmouth", "dans un petit village presque abandonné, nommé Dirtmouth. Il y a quand même un peu de lumière et de vie cependant. (Une des maisons semble être une sorte de magasin mais il est actuellement fermé)")
        self.rooms.append(self.dirtmouth)
        crystal_peak = Room("Crystal Peak", "à une certaine hauteur, dans un lieu scintillant prénommé Mont Cristal. De nombreuses mines ont été creusées dans la falaise pour obtenir les précieux cristaux roses.")
        self.rooms.append(crystal_peak)
        greenpath = Room("Greenpath", "à Vertchemin, un lieu dont la végétation luxuriante et les insectes recouverts de feuillage en font un endroit splendide. On trouve également des flaques d'acides brûlant et une épaisse prolifération rendant la navigation difficile.")
        self.rooms.append(greenpath)
        self.forgotten_crossroads = Room("Forgotten Crossroads", "au beau milieu des Routes Oubliées, situé sous le village de Dirtmouth. Elles permettaient autrefois de rejoindre de nombreuses autres régions du royaume.")
        self.rooms.append(self.forgotten_crossroads)
        temple_black_egg = Room("Temple of the Black Egg", "en face du Temple de l'Œuf Noir, on peut y entendre que quelque chose crie depuis l'intérieur et qu'un évènement risque de déterminer l'avenir du royaume.")
        self.rooms.append(temple_black_egg)
        blue_lake = Room("Blue Lake", "en face d'un lac bleu. Celui ci semble inoffensif et reposant à un tel point que l'on souhaiterait rester en face jusqu'à l'écroulement d'Hallownest.")
        self.rooms.append(blue_lake)
        fog_canyon = Room("Fog Canyon", "dans Brumes Canyon, un endroit effervescent et gélatineux de part les méduses qui y habitent. Cependant, gare à vous car les méduses peuvent exploser au contact d'une paroi tout comme leur nid. Une énorme structure s'y trouve.")
        self.rooms.append(fog_canyon)
        fungal_wastes = Room("Fungal Wastes", "dans la Caverne Nocive qui est une zone humide et recouverte de champignons de toutes les sortes. En plus de cela, des flaques d'acide caustiques sont abondantes dans toute la région.")
        self.rooms.append(fungal_wastes)
        city_of_tears = Room("City Of Tears", "dans la Cité des Larmes. C'était la capitale d'Hallownest. Elle est couverte d'une pluie perpétuelle qui provient du plafond qui la surplombe étant donné qu'elle est située en dessous du Lac Bleu. Son nom original a été perdu dans l'histoire. En plein centre de la Cité se trouve la place de la Fontaine, où se trouve la fontaine commémorative du Hollow Knight.")
        self.rooms.append(city_of_tears)
        mantis_village = Room("Mantis Village","dans le Village des Mantes. Un endroit où l'honneur et la souveraineté ne sont pas ceux du royaume d'Hallownest. Un pacte a été effectué pour qu'elle conserve la souveraineté sur leur domaine en échange de garder à distance les horribles bêtes du Nid Profond. Un village de guerriers et de guerrières qui défendent leur territoire au péril de leur vie !")
        self.rooms.append(mantis_village)
        deepnest = Room("Deepnest", "dans le Nid Profond. Son environnement lugubre et sombre, jonché d'épaisses couches de toile d'araignées, peut en faire fuir beaucoup. Malgré tout, des traces d'anciennes civilisations sont présentes, ce qui en fait un lieu riche en histoire.",dark=True)
        self.rooms.append(deepnest)

        # Create exits for rooms

        howling_cliffs.exits = {"Up" : None, "E" : self.dirtmouth, "Down" : greenpath, "O" : None}
        self.dirtmouth.exits = {"Up" : None, "E" : crystal_peak, "Down" : self.forgotten_crossroads, "O" : howling_cliffs}
        crystal_peak.exits = {"Up" : None, "E" : None, "Down" : None, "O" : self.dirtmouth}
        greenpath.exits = {"Up" : howling_cliffs, "E" : self.forgotten_crossroads, "Down" : fog_canyon, "O" : None}
        self.forgotten_crossroads.exits = {"Up" : self.dirtmouth, "E" : Door(temple_black_egg,locked=True), "Down" : fungal_wastes, "O" : greenpath}
        temple_black_egg.exits = {"Up" : None, "E" : None, "Down" : None, "O" : self.forgotten_crossroads}
        blue_lake.exits = {"Up" : crystal_peak, "E" : None, "Down" : None, "O" : None}
        fog_canyon.exits = {"Up" : greenpath, "E" : fungal_wastes, "Down" : None, "O" : None}
        fungal_wastes.exits = {"Up" : self.forgotten_crossroads, "E" : Door(city_of_tears, locked=True, key= "blason de la ville"), "Down" : mantis_village, "O" : fog_canyon}
        city_of_tears.exits = {"Up" : None, "E" : None, "Down" : None, "O" : None}
        mantis_village.exits = {"Up" : fungal_wastes, "E" : None, "Down" : deepnest, "O" : None}
        deepnest.exits = {"Up" : mantis_village, "E" : None, "Down" : None, "O" : None}

        #create items for rooms
        journal_vagabond_1 = Item("journal vagabond 1", "Ces journaux nous offrent un aperçu intéressant des esprits et des cœurs de ceux qui ont vécu avant nous.", value=500)
        journal_vagabond_2 = Item("journal vagabond 2", "Ces journaux nous offrent un aperçu intéressant des esprits et des cœurs de ceux qui ont vécu avant nous.", value=500)
        journal_vagabond_3 = Item("journal vagabond 3", "Ces journaux nous offrent un aperçu intéressant des esprits et des cœurs de ceux qui ont vécu avant nous.", value=500)
        lanterne = Item("lanterne", "Une lanterne en cristal qui éclaire les cavernes plongées de Deepnest afin que les voyageurs puissent retrouver leur chemin.", value=2000)
        self.items[lanterne.name] = lanterne
        minerai_pale_1 = Item("minerai pale 1", "Un minerai rare et pale, prié par ceux qui fabriquent des armes.", value=0)
        minerai_pale_2 = Item("minerai pale 2", "Un minerai rare et pale, prié par ceux qui fabriquent des armes.", value=0)
        cle_marchand = Item("cle du marchand", "Une clé de cuivre qui ouvre la boutique du Marchand à Dirtmouth.", value=1)
        sceau_hallownest_1 = Item("sceau hallownest 1", "Ces sceaux ornés étaient les symboles officiels du Roi et de ses Chevaliers, et étaient précieux de ceux qui les portaient.", value=1000)
        sceau_hallownest_2 = Item("sceau hallownest 2", "Ces sceaux ornés étaient les symboles officiels du Roi et de ses Chevaliers, et étaient précieux de ceux qui les portaient.", value=1000)
        sceau_hallownest_3 = Item("sceau hallownest 3", "Ces sceaux ornés étaient les symboles officiels du Roi et de ses Chevaliers, et étaient précieux de ceux qui les portaient.", value=1000)
        trampass = Item("trampass", "Un pass qui permet d'accéder à Blue Lake.", value=0)
        idole_roi_1 = Item("idole du roi 1", "Une icône du roi de Hallownest, vénéré à la fois comme dieu et comme souverain. Fabriqués dans un matériau blanc mystérieux, ils sont rares et très précieux.", value=1500)
        idole_roi_2 = Item("idole du roi 2", "Une icône du roi de Hallownest, vénéré à la fois comme dieu et comme souverain. Fabriqués dans un matériau blanc mystérieux, ils sont rares et très précieux.", value=1500)
        blason_ville = Item("blason de la ville", "dalle de pierre arborant le blason de la capitale d'Hallownest.", value=1000)
        self.items[blason_ville.name] = blason_ville
        masque_erudite = Item("masque de l'érudite", "Un masque ancien qui augmente votre sagesse.", value=0)
        aiguillon = Item("aiguillon", "Un aiguillon simple mais efficace pour combattre les ennemis.", value=0)
        oeuf_arcanique = Item("oeuf arcanique", "Cela semble être un simple oeuf, mais c’est en réalité une relique précieuse d’avant la naissance de Hallownest !", value=3999)

        howling_cliffs.inventory[journal_vagabond_1.name] = journal_vagabond_1
        fog_canyon.inventory[journal_vagabond_2.name] = journal_vagabond_2
        crystal_peak.inventory[journal_vagabond_3.name] = journal_vagabond_3


        crystal_peak.inventory[minerai_pale_1.name] = minerai_pale_1
        deepnest.inventory[minerai_pale_2.name] = minerai_pale_2

        crystal_peak.inventory[cle_marchand.name] = cle_marchand

        greenpath.inventory[sceau_hallownest_1.name] = sceau_hallownest_1
        self.forgotten_crossroads.inventory[sceau_hallownest_2.name] = sceau_hallownest_2
        fungal_wastes.inventory[sceau_hallownest_3.name] = sceau_hallownest_3

        fog_canyon.inventory[trampass.name] = trampass
        
        city_of_tears.inventory[idole_roi_1.name] = idole_roi_1
        mantis_village.inventory[idole_roi_2.name] = idole_roi_2

        deepnest.inventory[oeuf_arcanique.name] = oeuf_arcanique

        #Setup PNJ
            #pnj pacifique

        sly = Character( "Sly", "Un insecte replié sur lui-même, marmonnant des paroles incohérentes.", self.forgotten_crossroads, [ "…hein ?", "Laisse-moi tranquille…", "Je ne me souviens de rien…" ], merchant=False, stock={} )
        self.characters.append(sly)

        lemm = Character("Lemm","Un chercheur de reliques passionné par l'histoire du royaume.",city_of_tears, ["Je me présente en tant que Lemm, chercheurs de reliques d'Hallownest. Il existe une histoire oubliée, cachée dans les antiquités de ce royaume. Cependant, rares sont ceux qui sont disposés à s'y intéresser. Certains viennent juste pour dénicher des trésors dans les fissures et dans les ruines",
                                                                                                                "Si tu trouves une sorte de journal, celui ci offre un aperçu intéressant dans l'esprit et le coeur de ceux qui ont vécu avant nous. Je pourrais vous l'acheter contre quelques Geo","Les sceaux ornés étaient les symboles officiels du roi et de ses chevaliers, et chéris par ceux qui les portaient. Je vous en offrirai une modeste somme en échange.",
                                                                                                                "Il existe des idoles du roi d'Hallownest qui était vénéré à la fois comme un dieu et un souverain. Fabriquées à partir d'un matériau blanc mystérieux, celles-ci sont rares et très précieuses. Si vous me les vendez, je vous offrirai une bonne somme de Geo en échange.",
                                                                                                                "Il existe dans les profondeurs du royaume un oeuf qui parait simple. Mais c'est en fait, une précieuse relique qui remonte bien avant l'existence d'Hallownest ! Je vous en donnerai une petite fortune. Vendez-le-moi s'il vous plaît."], merchant=True)
        self.characters.append(lemm)

        forgeron = Character("Forgeron","Un forgeron en quête à la forge de l'aiguillon pur.", fungal_wastes, ["Mon aiguille est émoussée... tout comme ce royaume","Apporte-moi des Geo, et je rendrai ton aiguillon digne d'un véritable guerrier."], blacksmith=True, upgrade_cost=1500)
        self.characters.append(forgeron)

        elderbug = Character("Elderbug","Un des rares résident de Dirtmouth, il a l'air vieux et sage.", self.dirtmouth, ["J’ai bien peur qu’il ne reste plus que moi pour t’accueillir. Notre ville est devenue très silencieuse au fil du temps. Tous les autres résidents ont disparu.","Je suis Elderbug. Si tu as besoin d’aide, n’hésite pas à me parler.","Si tu cherches un marchand, tu le trouveras souvent aux Routes Oubliées ou à Dirtmouth. Il s’appelle Sly."], trainer=False)
        self.characters.append(elderbug)

        monomon = Character("Monomon l'érudite","Soudain, un air très familier frappe Quirrel lorsqu'il aperçoit la Rêveuse face à lui.", fog_canyon, ["…Quirrel. Ton esprit n'est plus lié aux chaînes d'autrefois, et pourtant tu es revenu jusqu'à moi.",
                                                                                                                                                        "Le masque que tu portes n'est plus un sceau, mais un souvenir. Un fragment de ce que tu étais.",
                                                                                                                                                        "Je t'ai confié mon savoir pour que tu marches librement, loin du poids des Rêveurs.",
                                                                                                                                                        "Le chemin que tu as suivi te ramène ici, mais le choix t'appartient désormais.",
                                                                                                                                                        "Souviens-toi : la connaissance éclaire, mais elle n'absout pas."])
        self.characters.append(monomon)

        sheo = Character("Sheo","Un insecte robuste muni d'un pinceau. Sa technique semble être celle d'une entaille implacable.", deepnest, ["Oh ! Un Visiteur ? Voilà qui rompt la monotonie.","Le combat est un art. Chaque mouvement doit être peint avec intention.","Manie ton aiguillon comme un pinceau."], trainer=True, training_cost=1000)
        self.characters.append(sheo)

        oro = Character("Oro","Un insecte robuste muni d'un aiguillon énorme. Sa technique semble être celle d'une entaille rapide comme l'éclair.", crystal_peak, ["Ne perds pas de temps. L'hésitation est une faiblesse.","La vitesse est la clé de la survie.","Si tu veux apprendre, je te montrerais mon mouvement, la Coupe de Dash."], trainer=True, training_cost=3000)
        self.characters.append(oro)

        mato = Character("Mato","Un insecte robuste muni d'un aiguillon énorme. Sa technique semble être celle d'une entaille circulaire.", blue_lake, ["La force brute ne suffit pas.","Observe ton ennemi, puis frappe là où il ne s'y attend pas.","ma technique, le Cyclone Slash, balaie tout sur son passage."], trainer=True, training_cost=5000)
        self.characters.append(mato)

        self.zote = Character("Zote", "L'incroyable et redoutable Zote se dresse devant vous ! Rare sont les créatures aussi faible que lui.", self.dirtmouth, ["a faire"])
        self.characters.append(self.zote)

            #pnj hostile
        
        hollow_knight = Character("Hollow Knight","Il a été choisi il y a fort longtemps pour sceller la Radiance… Ce vaisseau était autrefois fils du roi et de la reine d'Hallownest.", temple_black_egg, ["..."], level=14,hostile=True,is_boss=True)
        self.characters.append(hollow_knight)

        uumuu = Character("Uumuu","Une énorme méduse infecté par la Radiance. Il semble être le défenseur de la chambre de stase de Monomon.", fog_canyon, ["..."], level=10,hostile=True,is_boss=True,reward_geos=500)
        self.characters.append(uumuu)

        soul_master = Character("Le Maitre de l'ame","Chef du Sanctuaire de l'âme dans la cité des larmes, il menait des expériences sur l'Ame pour trouver un autre moyen de repousser l'infection de la Radiance. Cela a échoué à priori…", city_of_tears, ["a faire"], level=12,hostile=True,is_boss=True,reward_geos=500)
        self.characters.append(soul_master)

        hornet = Character("Hornet","Une voyageuse habile qui manie un aiguillon et un fil. Elle abat tout ce qui ce trouve sur son chemin.", greenpath, ["Recule. Ce territoire n'est pas le tien.",
                                                                                                                                                            "Tu avances trop librement pour quelqu'un qui devrait se souvenir de son rôle.",
                                                                                                                                                            "Ton masque… je reconnais son origine. Et cela me déplaît.",
                                                                                                                                                            "Les échecs du passé ne doivent pas se répéter. Je ne te laisserai pas interférer.",
                                                                                                                                                            "Si tu fais un pas de plus, je t'arrêterai moi-même."], level=3,hostile=True,is_boss=True,reward_geos=500)
        self.characters.append(hornet)

        mantis_lord = Character("Dames Mantes","Trois sœurs Mante qui siègent chacune sur trois trônes. Leur coordination est redoutable et en font un ennemi coriace.", mantis_village, ["a faire"], level=5,hostile=True,is_boss=True,reward_geos=500)
        self.characters.append(mantis_lord)

        crystal_guardian = Character("Gardien de cristal","Un ancien protecteur des mines de cristal, maintenant corrompu par l'infection.", crystal_peak, ["..."], level=2,hostile=True,is_boss=True,reward_geos=500)
        self.characters.append(crystal_guardian)

        false_knight = Character("Faux Chevalier","Un ver rendu fou par une force étrange. Il vit dans une carapace cuirassée qu’il a volé.", self.forgotten_crossroads, ["..."], level=1,hostile=True,is_boss=True ,reward_geos=500)
        self.characters.append(false_knight)

        mawlek = Character("Mawlek Maussade","Une bête féroce, mais extrêmement sociale. Elle devient agressive si elle ne peut pas s'amuser avec ceux de son espèce.", howling_cliffs, ["..."], level=4,hostile=True,is_boss=True,reward_geos=500)
        self.characters.append(mawlek)

        nosk = Character("Nosk","Un prédateur métamorphe qui imite la forme de ses proies pour les attirer dans des embuscades.", deepnest, ["..."], level=9,hostile=True,is_boss=True,reward_geos=500)
        self.characters.append(nosk)

        elder_hu = Character("Hu L'Ancien","Un rêve persistant, appartenant à un guerrier mort. Il a voyagé partout dans ce monde et s’est occupé de ceux affectés par ce fléau.", fungal_wastes, ["..."], level=7,hostile=True,is_boss=True,reward_geos=500)
        self.characters.append(elder_hu)



        # Setup player and starting room

        self.player = Player("Quirrel")
        self.player.current_room = howling_cliffs
        self.player.game = self

        #item de départ dans l'inventaire du joueur
        self.player.inventory[masque_erudite.name] = masque_erudite
        self.player.inventory[aiguillon.name] = aiguillon

        # Setup quests
        self._setup_quests()

        # Gestion directions et directions inconnues

        self.direction_up = {'Haut', 'HAUT','haut','H','h','UP', 'U','Up','up','u'}
        self.direction_down = {'Bas','BAS','B','b','bas','DOWN','down','Down','D','d'}
        self.direction_west = {'Gauche','GAUCHE','gauche','G','g','Ouest','OUEST','ouest','O','o'}
        self.direction_east = {'Droite','DROITE','droite','D','d','EST','Est','est','e','E'}

    def _setup_quests(self):
        """Initialize all quests."""
        #Quête d'item : récupérer la clé du marchand
        quest_cle = Quest(
            title="cle du marchand",
            description="Sly a perdu sa clé. Retrouvez-la au sommet du royaume.",
            objectives=["prendre cle du marchand et lui vendre"],
            reward="Boutique de Sly débloquée"
        )

        #Quête déplacement,combat, intéraction : Uumuu et Monomon (good ending)
        quest_monomon = Quest(
            title="débloquer Monomon",
            description="Atteignez Fog Canyon, vianquez Uumuu et parlez à Monomon.",
            objectives=["Visiter Fog Canyon",
                        "vaincre Uumuu",
                        "parler à Monomon l'érudite"],
            reward="Personnage de Monomon débloquée"
        )

        # Quête intéraction : s'entraîner chez les 3 frères
        quest_freres = Quest(
            title="les trois frères d'aiguillon",
            description="Trouvez les trois frères et parlez-leur pour progresser dans l'art de l'aiguillon.",
            objectives=["parler à Oro",
                        "parler à Mato",
                        "parler à Sheo",],
            reward="Maîtrise de l'aiguillon augmentée"
        )

        # Quête d'item : l'oeuf arcanique (Lemm)
        quest_oeuf = Quest(
            title="oeuf arcanique",
            description="Lemm est à la recherche d'une relique précieuse : un oeuf arcanique caché dans les profondeurs.",
            objectives=["prendre oeuf arcanique",
                        "parler à Lemm"],
            reward="Connaissances du Roi Pale"
        )

        # Quête d'item : minerais pales (Forgeron)
        quest_minerais = Quest(
            title="minerais pales",
            description="Trouvez les minerais pales dans les profondeurs et apportez-les au forgeron.",
            objectives=["prendre minerai pale 1",
                        "prendre minerai pale 2",
                        "parler à Forgeron"],
            reward="Arme améliorée"
        )


        # Add quests to player's quest manager
        self.player.quest_manager.add_quest(quest_cle)
        self.player.quest_manager.add_quest(quest_monomon)
        self.player.quest_manager.add_quest(quest_freres)
        self.player.quest_manager.add_quest(quest_oeuf)
        self.player.quest_manager.add_quest(quest_minerais)
    
    #débloquer la porte de Temple of the Black Egg si toutes les quetes sont complétées
    def unlock_temple_black_egg(self):
        for room in self.rooms:
            for direction, exit_room in room.exits.items():
                if isinstance(exit_room, Door) and exit_room.destination.name == "Temple of the Black Egg": 
                    if not exit_room.locked:
                        return False
                        
                    for quest in self.player.quest_manager.quests:
                        if not quest.is_completed:
                            return False

                    exit_room.locked = False
                    print("\nLa porte du Temple de l'Œuf Noir s'est déverrouillée !\n")
                    return True
        return False    

    # Play the game
    def play(self):
        """Main game loop."""

        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
            self.unlock_temple_black_egg()

            # Check win/loose conditions
            if self.loose():
                print("\nVous êtes mort... Quirrel a été vaincu.\n")
                self.finished = True
            
            if self.win():
                print("\nFélicitations ! Vous avez vaincu Le Hollow Knight et sauvé le royaume d'Hallownest !\n")
                self.finished = True
            while not self.finished:
                command = input("> ")
                self.process_command(command)

    # Process the command entered by the player
    def process_command(self, command_string) -> None:
        """Process the command entered by the player."""
        # Split the command string into a list of words
        list_of_words = command_string.split(" ")
        command_word = list_of_words[0]


        if command_word not in self.commands.keys():
            if command_word == "":
                print(f">")
            else:
                print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")

        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def print_welcome(self):
        print(f"\nVous incarnerez {self.player.name}, un insecte amnésique provenant d'une contrée lointaine.\nCependant, votre masque, le masque de l'érudit, vous a guidé jusqu'au royaume mourant d'Hallownest. Est-ce une coïncidence ?")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())

    def get_characters_in_room(self):
        room = self.player.current_room
        return [c for c in self.characters if c.current_room == room]
    
    def win(self):
        """
        Retourne True si Le Hollow Knight a été vaincu.
        """
        for c in self.characters:
            if c.name == "Le Hollow Knight":
                return c.defeated
        return False

    def loose(self):
        """
        Retourne True si le joueur est mort(perdre un combat contre un ennemi plus fort).
        """
        return not self.player.alive

    def move_zote_randomly(self):
        """Fait se déplacer Zote aléatoirement entre Forgotten Crossroads et Dirtmouth."""
        if not hasattr(self, "zote"):
            return

        zote = self.zote

        # Zote ne bouge que s'il est dans l'une des deux zones
        if zote.current_room not in (self.forgotten_crossroads, self.dirtmouth):
            return

        # Une chance sur deux de bouger
        if random.choice([True, False]):
            # Choisir l'autre salle
            next_room = (
                self.dirtmouth
                if zote.current_room == self.forgotten_crossroads
                else self.forgotten_crossroads
            )
            zote.current_room = next_room


##############################
# Tkinter GUI Implementation #
##############################

class _StdoutRedirector:
    """Redirect sys.stdout writes into a Tkinter Text widget."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, msg):
        """Write message to the Text widget."""
        if msg:
            self.text_widget.configure(state="normal")
            self.text_widget.insert("end", msg)
            self.text_widget.see("end")
            self.text_widget.configure(state="disabled")

    def flush(self):
        """Flush method required by sys.stdout interface (no-op for Text widget)."""



class GameGUI(tk.Tk):
    """Tkinter GUI for the text-based adventure game.

    Layout layers:
    L3 (top): Split into left image area (600x400) and right buttons.
    L2 (middle): Scrolling terminal output.
    L1 (bottom): Command entry field.
    """

    IMAGE_WIDTH = 600
    IMAGE_HEIGHT = 400

    def __init__(self):
        super().__init__()
        self.title("TBA")
        self.geometry("900x700")  # Provide enough space
        self.minsize(900, 650)

        # Underlying game logic instance
        self.game = Game()

        # Ask player name via dialog (fallback to 'Joueur')
        name = simpledialog.askstring("Nom", "Entrez votre nom:", parent=self)
        if not name:
            name = "Joueur"
        self.game.setup()  # Pass name to avoid double prompt
        self.game.player.name = name

        # Build UI layers
        self._build_layout()

        # Redirect stdout so game prints appear in terminal output area
        self.original_stdout = sys.stdout
        sys.stdout = _StdoutRedirector(self.text_output)

        # Print welcome text in GUI
        self.game.print_welcome()

        # Load initial room image
        self._update_room_image()

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_close)


    # -------- Layout construction --------
    def _build_layout(self):
        # Configure root grid: 3 rows (L3, L2, L1)
        self.grid_rowconfigure(0, weight=0)  # Image/buttons fixed height
        self.grid_rowconfigure(1, weight=1)  # Terminal output expands
        self.grid_rowconfigure(2, weight=0)  # Entry fixed
        self.grid_columnconfigure(0, weight=1)

        # L3 Top frame
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="nsew", padx=6, pady=(6,3))
        top_frame.grid_columnconfigure(0, weight=0)
        top_frame.grid_columnconfigure(1, weight=1)

        # L3L Image area (left)
        image_frame = ttk.Frame(top_frame, width=self.IMAGE_WIDTH, height=self.IMAGE_HEIGHT)
        image_frame.grid(row=0, column=0, sticky="nw", padx=(0,6))
        image_frame.grid_propagate(False)  # Keep requested size
        self.canvas = tk.Canvas(image_frame,
                                width=self.IMAGE_WIDTH,
                                height=self.IMAGE_HEIGHT,
                                bg="#222")
        self.canvas.pack(fill="both", expand=True)

        # Initialize image reference (will be loaded by _update_room_image)
        self._image_ref = None  # Keep reference to prevent garbage collection
        # Initial image will be loaded after welcome message

        # L3R Buttons area (right)
        buttons_frame = ttk.Frame(top_frame)
        buttons_frame.grid(row=0, column=1, sticky="ne")
        for i in range(10):
            buttons_frame.grid_rowconfigure(i, weight=0)
        buttons_frame.grid_columnconfigure(0, weight=1)

        # Load button images (keep references to prevent garbage collection)
        assets_dir = Path(__file__).parent / 'assets'
        # Load pre-resized 50x50 PNG images for better quality
        self._btn_help = tk.PhotoImage(file=str(assets_dir / 'help-50.png'))
        self._btn_up = tk.PhotoImage(file=str(assets_dir / 'up-arrow-50.png'))
        self._btn_down = tk.PhotoImage(file=str(assets_dir / 'down-arrow-50.png'))
        self._btn_left = tk.PhotoImage(file=str(assets_dir / 'left-arrow-50.png'))
        self._btn_right = tk.PhotoImage(file=str(assets_dir / 'right-arrow-50.png'))
        self._btn_quit = tk.PhotoImage(file=str(assets_dir / 'quit-50.png'))

        # Command buttons
        tk.Button(buttons_frame,
                  image=self._btn_help,
                  command=lambda: self._send_command("help"),
                  bd=0).grid(row=0, column=0, sticky="ew", pady=2)
        # Movement buttons (N,E,S,O)
        move_frame = ttk.LabelFrame(buttons_frame, text="Déplacements")
        move_frame.grid(row=1, column=0, sticky="ew", pady=4)
        tk.Button(move_frame,
                  image=self._btn_up,
                  command=lambda: self._send_command("go N"),
                  bd=0).grid(row=0, column=0, columnspan=2)
        tk.Button(move_frame,
                  image=self._btn_left,
                  command=lambda: self._send_command("go O"),
                  bd=0).grid(row=1, column=0)
        tk.Button(move_frame,
                  image=self._btn_right,
                  command=lambda: self._send_command("go E"),
                  bd=0).grid(row=1, column=1)
        tk.Button(move_frame,
                  image=self._btn_down,
                  command=lambda: self._send_command("go S"),
                  bd=0).grid(row=2, column=0, columnspan=2)

        # Quit button
        tk.Button(buttons_frame,
                  image=self._btn_quit,
                  command=lambda: self._send_command("quit"),
                  bd=0).grid(row=2, column=0, sticky="ew", pady=(8,2))

        # L2 Terminal output area (Text + Scrollbar)
        output_frame = ttk.Frame(self)
        output_frame.grid(row=1, column=0, sticky="nsew", padx=6, pady=3)
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(output_frame, orient="vertical")
        self.text_output = tk.Text(output_frame,
                                   wrap="word",
                                   yscrollcommand=scrollbar.set,
                                   state="disabled",
                                   bg="#111", fg="#eee")
        scrollbar.config(command=self.text_output.yview)
        self.text_output.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # L1 Entry area
        entry_frame = ttk.Frame(self)
        entry_frame.grid(row=2, column=0, sticky="ew", padx=6, pady=(3,6))
        entry_frame.grid_columnconfigure(0, weight=1)

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(entry_frame, textvariable=self.entry_var)
        self.entry.grid(row=0, column=0, sticky="ew")
        self.entry.bind("<Return>", self._on_enter)
        self.entry.focus_set()


    # -------- Image update --------
    def _update_room_image(self):
        """Update the canvas image based on the current room."""
        if not self.game.player or not self.game.player.current_room:
            return

        room = self.game.player.current_room
        assets_dir = Path(__file__).parent / 'assets'

        # Use room-specific image if available, otherwise fallback
        if room.image:
            image_path = assets_dir / room.image
        else:
            image_path = assets_dir / 'scene.png'

        try:
            # Load new image
            self._image_ref = tk.PhotoImage(file=str(image_path))
            # Clear canvas and redraw image
            self.canvas.delete("all")
            self.canvas.create_image(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                image=self._image_ref
            )
        except (FileNotFoundError, tk.TclError):
            # Fallback to text if image not found or cannot be loaded
            self.canvas.delete("all")
            self.canvas.create_text(
                self.IMAGE_WIDTH/2,
                self.IMAGE_HEIGHT/2,
                text=f"Image: {room.name}",
                fill="white",
                font=("Helvetica", 18)
            )


    # -------- Event handlers --------
    def _on_enter(self, _event=None):
        """Handle Enter key press in the entry field."""
        value = self.entry_var.get().strip()
        if value:
            self._send_command(value)
        self.entry_var.set("")


    def _send_command(self, command):
        if self.game.finished:
            return
        # Echo the command in output area
        print(f"> {command}\n")
        self.game.process_command(command)
        # Update room image after command (in case player moved)
        self._update_room_image()
        if self.game.finished:
            # Disable further input and schedule close (brief delay to show farewell)
            self.entry.configure(state="disabled")
            self.after(600, self._on_close)


    def _on_close(self):
        # Restore stdout and destroy window
        sys.stdout = self.original_stdout
        self.destroy()


def main():
    """Entry point.

    If '--cli' is passed as an argument, start the classic console version.
    Otherwise launch the Tkinter GUI.
    Fallback to CLI if GUI cannot be initialized (e.g., headless environment).
    """
    args = sys.argv[1:]
    if '--cli' in args:
        Game().play()
        return
    try:
        app = GameGUI()
        app.mainloop()
    except tk.TclError as e:
        # Fallback to CLI if GUI fails (e.g., no DISPLAY, Tkinter not available)
        print(f"GUI indisponible ({e}). Passage en mode console.")
        Game().play()

    
if __name__ == "__main__":
    main()
#test