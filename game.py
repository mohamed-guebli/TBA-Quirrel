# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
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

        # Setup rooms

        howling_cliffs = Room("Howling Cliffs", ".")
        self.rooms.append(howling_cliffs)
        dirtmouth = Room("Dirtmouth", ".")
        self.rooms.append(dirtmouth)
        crystal_peak = Room("Crystal Peak", ".")
        self.rooms.append(crystal_peak)
        greenpath = Room("Greenpath", ".")
        self.rooms.append(greenpath)
        forgotten_crossroads = Room("Forgotten Crossroads", ".")
        self.rooms.append(forgotten_crossroads)
        temple_black_egg = Room("Temple of the Black Egg", ".")
        self.rooms.append(temple_black_egg)
        blue_lake = Room("Blue Lake", "test")
        self.rooms.append(blue_lake)
        fog_canyon = Room("Fog Canyon", ".")
        self.rooms.append(fog_canyon)
        fungal_wastes = Room("Fungal Wastes", ".")
        self.rooms.append(fungal_wastes)
        city_of_tears = Room("City Of Tears", ".")
        self.rooms.append(city_of_tears)
        mantis_village = Room("Mantis Village",".")
        self.rooms.append(mantis_village)
        deepnest = Room("Deepnest", ".",dark=True)
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
        fungal_wastes.exits = {"Up" : forgotten_crossroads, "E" : city_of_tears, "Down" : mantis_village, "O" : fog_canyon}
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
        masque_erudit = Item("masque erudit", "Un masque ancien qui augmente votre sagesse.", 1)
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

        sly = Character("Sly","Un marchand qui semble s'y connaitre dans l'art de l'aiguillon", forgotten_crossroads, ["Donne l'argent là"])
        forgotten_crossroads.characters[sly.name] = sly
        
        # Setup player and starting room

        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = howling_cliffs

        #item de départ dans l'inventaire du joueur
        self.player.inventory[masque_erudit.name] = masque_erudit

        # Gestion directions et directions inconnues

        self.direction_up = {'Haut', 'HAUT','haut','H','h','UP', 'U','Up','up','u'}
        self.direction_down = {'Bas','BAS','B','b','bas','DOWN','down','Down','D','d'}
        self.direction_west = {'Gauche','GAUCHE','gauche','G','g','Ouest','OUEST','ouest','O','o'}
        self.direction_east = {'Droite','DROITE','droite','D','d','EST','Est','est','e','E'}

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
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
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
#test