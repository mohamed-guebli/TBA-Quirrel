# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character
from door import Door
from quest import Quest 

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.characters = []
        self.player = None
    
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
        back = Command("back", " : revenir dans la salle précédente", Actions.back, 0)
        self.commands["back"] = back
        look = Command("look", " : regarder les items présents dans la salle", Actions.look, 0 )
        self.commands["look"] = look
        take = Command("take", " <item> : prendre un objet", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " <item> : déposer un objet", Actions.drop, 1)
        self.commands["drop"] = drop
        check = Command("check", " : vérifier l'inventaire du joueur", Actions.check, 0)
        self.commands["check"] = check
        talk = Command("talk"," : parler à un PNJ", Actions.talk, 1)
        self.commands["talk"] = talk
        fight = Command("fight"," : combattre un ennemi", Actions.fight, 1)
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
        # Setup rooms

        howling_cliffs = Room("Howling Cliffs", "non loin des frontières du royaume située au nord-ouest. Les falaises hurlantes n'ont pas l'air peuplées du tout.")
        self.rooms.append(howling_cliffs)
        dirtmouth = Room("Dirtmouth", "dans un petit village presque abandonné, nommé Dirtmouth. Il y a quand même un peu de lumière et de vie cependant. (Une des maisons semble être une sorte de magasin mais il est actuellement fermé)")
        self.rooms.append(dirtmouth)
        crystal_peak = Room("Crystal Peak", "à une certaine hauteur, dans un lieu scintillant prénommé Mont Cristal. De nombreuses mines ont été creusées dans la falaise pour obtenir les précieux cristaux roses.")
        self.rooms.append(crystal_peak)
        greenpath = Room("Greenpath", "à Vertchemin, un lieu dont la végétation luxuriante et les insectes recouverts de feuillage en font un endroit splendide. On trouve également des flaques d'acides brûlant et une épaisse prolifération rendant la navigation difficile.")
        self.rooms.append(greenpath)
        forgotten_crossroads = Room("Forgotten Crossroads", "au beau milieu des Routes Oubliées, situé sous le village de Dirtmouth. Elles permettaient autrefois de rejoindre de nombreuses autres régions du royaume.")
        self.rooms.append(forgotten_crossroads)
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

        howling_cliffs.exits = {"Up" : None, "E" : dirtmouth, "Down" : greenpath, "O" : None}
        dirtmouth.exits = {"Up" : None, "E" : crystal_peak, "Down" : forgotten_crossroads, "O" : howling_cliffs}
        crystal_peak.exits = {"Up" : None, "E" : None, "Down" : None, "O" : dirtmouth}
        greenpath.exits = {"Up" : howling_cliffs, "E" : forgotten_crossroads, "Down" : fog_canyon, "O" : None}
        forgotten_crossroads.exits = {"Up" : dirtmouth, "E" : temple_black_egg, "Down" : fungal_wastes, "O" : greenpath}
        temple_black_egg.exits = {"Up" : None, "E" : None, "Down" : None, "O" : forgotten_crossroads}
        blue_lake.exits = {"Up" : crystal_peak, "E" : None, "Down" : None, "O" : None}
        fog_canyon.exits = {"Up" : greenpath, "E" : fungal_wastes, "Down" : None, "O" : None}
        fungal_wastes.exits = {"Up" : forgotten_crossroads, "E" : Door(city_of_tears, locked=True, key= "blason de la ville"), "Down" : mantis_village, "O" : fog_canyon}
        city_of_tears.exits = {"Up" : None, "E" : None, "Down" : None, "O" : None}
        mantis_village.exits = {"Up" : forgotten_crossroads, "E" : None, "Down" : deepnest, "O" : None}
        deepnest.exits = {"Up" : mantis_village, "E" : None, "Down" : None, "O" : None}

        #create items for rooms
        journal_vagabond_1 = Item("journal vagabond 1", "Ces journaux nous offrent un aperçu intéressant des esprits et des cœurs de ceux qui ont vécu avant nous.", 2)
        journal_vagabond_2 = Item("journal vagabond 2", "Ces journaux nous offrent un aperçu intéressant des esprits et des cœurs de ceux qui ont vécu avant nous.", 2)
        journal_vagabond_3 = Item("journal vagabond 3", "Ces journaux nous offrent un aperçu intéressant des esprits et des cœurs de ceux qui ont vécu avant nous.", 2)
        lanterne = Item("lanterne", "Une lanterne en cristal qui éclaire les cavernes plongées de Deepnest afin que les voyageurs puissent retrouver leur chemin.", 1)
        minerai_pale_1 = Item("minerai pale 1", "Un minerai rare et pale, prié par ceux qui fabriquent des armes.", 2)
        minerai_pale_2 = Item("minerai pale 2", "Un minerai rare et pale, prié par ceux qui fabriquent des armes.", 2)
        cle_marchand = Item("cle du marchand", "Une clé de cuivre qui ouvre la boutique du Marchand à Dirtmouth.", 0.5)
        sceau_hallownest_1 = Item("sceau hallownest 1", "Ces sceaux ornés étaient les symboles officiels du Roi et de ses Chevaliers, et étaient précieux de ceux qui les portaient.", 2)
        sceau_hallownest_2 = Item("sceau hallownest 2", "Ces sceaux ornés étaient les symboles officiels du Roi et de ses Chevaliers, et étaient précieux de ceux qui les portaient.", 2)
        sceau_hallownest_3 = Item("sceau hallownest 3", "Ces sceaux ornés étaient les symboles officiels du Roi et de ses Chevaliers, et étaient précieux de ceux qui les portaient.", 2)
        trampass = Item("trampass", "Un pass qui permet d'accéder à Blue Lake.", 0.2)
        idole_roi_1 = Item("idole du roi 1", "Une icône du roi de Hallownest, vénéré à la fois comme dieu et comme souverain. Fabriqués dans un matériau blanc mystérieux, ils sont rares et très précieux.", 2)
        idole_roi_2 = Item("idole du roi 2", "Une icône du roi de Hallownest, vénéré à la fois comme dieu et comme souverain. Fabriqués dans un matériau blanc mystérieux, ils sont rares et très précieux.", 2)
        blason_ville = Item("blason de la ville", "dalle de pierre arborant le blason de la capitale d'Hallownest.", 1)
        masque_erudit = Item("masque de l'erudit", "Un masque ancien qui augmente votre sagesse.", 1)
        oeuf_arcanique = Item("oeuf arcanique", "Cela semble être un simple oeuf, mais c’est en réalité une relique précieuse d’avant la naissance de Hallownest !", 2)

        howling_cliffs.inventory[journal_vagabond_1.name] = journal_vagabond_1
        fog_canyon.inventory[journal_vagabond_2.name] = journal_vagabond_2
        crystal_peak.inventory[journal_vagabond_3.name] = journal_vagabond_3

        dirtmouth.inventory[lanterne.name] = lanterne

        crystal_peak.inventory[minerai_pale_1.name] = minerai_pale_1
        deepnest.inventory[minerai_pale_2.name] = minerai_pale_2

        crystal_peak.inventory[cle_marchand.name] = cle_marchand

        greenpath.inventory[sceau_hallownest_1.name] = sceau_hallownest_1
        forgotten_crossroads.inventory[sceau_hallownest_2.name] = sceau_hallownest_2
        fungal_wastes.inventory[sceau_hallownest_3.name] = sceau_hallownest_3

        fog_canyon.inventory[trampass.name] = trampass
        
        city_of_tears.inventory[idole_roi_1.name] = idole_roi_1
        mantis_village.inventory[idole_roi_2.name] = idole_roi_2

        mantis_village.inventory[blason_ville.name] = blason_ville

        deepnest.inventory[oeuf_arcanique.name] = oeuf_arcanique

        #Setup PNJ
            #pnj pacifique

        sly = Character("Sly","Un marchand qui semble s'y connaitre dans l'art de l'aiguillon", forgotten_crossroads, ["Donne l'argent là"],level=999,hostile=False,is_boss=False)
        self.characters.append(sly)
        lemm = Character("Lemm","Un chercheur de reliques passionné par l'histoire du royaume", city_of_tears, ["ez les reliques"],level=999,hostile=False,is_boss=False)
        self.characters.append(lemm)
        forgeron = Character("Forgeron","A faire", fungal_wastes, ["a faire"],level=999,hostile=False,is_boss=False)
        self.characters.append(forgeron)
        elderbug = Character("Elderbug","A faire", dirtmouth, ["a faire"],level=999,hostile=False,is_boss=False)
        self.characters.append(elderbug)
        monomon = Character("Monomon l'erudit","A faire", fog_canyon, ["a faire"],level=999,hostile=False,is_boss=False)
        self.characters.append(monomon)
        sheo = Character("Sheo","A faire", deepnest, ["a faire"],level=999,hostile=False,is_boss=False)
        self.characters.append(sheo)
        oro = Character("Oro","A faire", crystal_peak, ["a faire"],level=999,hostile=False,is_boss=False)
        self.characters.append(oro)
        mato = Character("Mato","A faire", blue_lake, ["a faire"],level=999,hostile=False,is_boss=False)
        self.characters.append(mato)
        zote = Character("Zote", "A faire", dirtmouth, ["a faire"],level=999,hostile=False,is_boss=False)
        self.characters.append(zote)

            #pnj hostile
        
        uumuu = Character("Uumuu","A faire", fog_canyon, ["a faire"], level=1,hostile=True,is_boss=True)
        self.characters.append(uumuu)
        hollow_knight = Character("Le Hollow Knight","A faire", temple_black_egg, ["a faire"], level=1,hostile=True,is_boss=True)
        self.characters.append(hollow_knight)
        soul_master = Character("Le Maitre de l'ame","A faire", city_of_tears, ["a faire"], level=1,hostile=True,is_boss=True)
        self.characters.append(soul_master)
        hornet = Character("Hornet","A faire", greenpath, ["a faire"], level=1,hostile=True,is_boss=True)
        self.characters.append(hornet)
        mantis_lord = Character("Dames Mantes","A faire", mantis_village, ["a faire"], level=1,hostile=True,is_boss=True)
        self.characters.append(mantis_lord)



        # Setup player and starting room

        self.player = Player("Quirrel")
        self.player.current_room = howling_cliffs

        #item de départ dans l'inventaire du joueur
        self.player.inventory[masque_erudit.name] = masque_erudit

        # Gestion directions et directions inconnues

        self.direction_up = {'Haut', 'HAUT','haut','H','h','UP', 'U','Up','up','u'}
        self.direction_down = {'Bas','BAS','B','b','bas','DOWN','down','Down','D','d'}
        self.direction_west = {'Gauche','GAUCHE','gauche','G','g','Ouest','OUEST','ouest','O','o'}
        self.direction_east = {'Droite','DROITE','droite','D','d','EST','Est','est','e','E'}

    def _setup_quests(self):
        """Initialize all quests."""
        #Quête d'item : récupérer la clé du marchand
        quest_cle = Quest(
            title="clé du marchand",
            description="Sly a perdu sa clé. Retrouvez-la au sommet du royaume.",
            objectives=["prendre cle du marchand"],
            reward="Boutique de Sly débloquée"
        )

        #Quête déplacement,combat, intéraction : Uumuu et Monomon (good ending)
        quest_monomon = Quest(
            title="débloquer Monomon",
            description="Atteignez Fog Canyon, vianquez Uumuu et parlez à Monomon.",
            objectives=["Visiter Fog Canyon",
                        "Combattre Uumuu",
                        "Parler Monomon l'erudit"],
            reward="Personnage de Monomon débloquée"
        )

        # Quête intéraction : s'entraîner chez les 3 frères
        quest_freres = Quest(
            title="les trois frères d'aiguillon",
            description="Trouvez les trois frères et parlez-leur pour progresser dans l'art de l'aiguillon.",
            objectives=["trouver Sheo, Oro et Mato",
                        "s'entrainer avec les trois frères."],
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
    

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
            
            if self.loose():
                print("\nVous êtes mort... Deepnest était trop dangereux sans lanterne.\n")
                self.finished = True
            
            if self.win():
                print("\nFélicitations ! Vous avez complété toutes les quêtes et sauvé le royaume d'Hallownest !\n")
                self.finished = True
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        

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
        Retourne True si le joueur a complété toutes les quetes.
        """
        for quest in self.player.quest_manager.quests:
            if not quest.completed:
                return False
        return True

    def loose(self):
        """
        Retourne True si le joueur est mort.
        """
        if self.player.current_room.name == "Deepnest" and not self.player.has_item("lanterne"):
            return True
        return False

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
#test