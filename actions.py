# Description: The actions module.


# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

from door import Door

class Actions:

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (Up, E, Down, O).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:
        
        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "Up"], 1)
        True
        >>> go(game, ["go", "Up", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False

        """
        
        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the direction from the list of words.
        direction = list_of_words[1]
        if direction in game.direction_up :
            direction = "Up"
        elif direction in game.direction_down :
            direction = "Down"
        elif direction in game.direction_east :
            direction = "E"
        elif direction in game.direction_west :
            direction = "O"
        else :
            print(f"Quirrel a heurté un mur en se dirigeant vers '{direction}'")
            return True

        exit_obj = player.current_room.exits.get(direction)
        if exit_obj is None:
            print(f"\nIl n'y a pas de sortie vers '{direction}' depuis cette pièce.\n")
            return True 

        # Move the player in the direction specified by the parameter.
        if not isinstance(exit_obj, Door):
            player.move(direction)
            return True
        
        #si il y a une porte verrouillée
        if exit_obj.locked:
            if exit_obj.key is None:
                print(f"\nLa porte est scellée par une force ancienne. Terminez toutes vos quetes pour tenter d'y accéder.\n")
                return True
            #vérifier si le joueur a l'item requis
            if player.has_item(exit_obj.key):
                print(f"\nVous utilisez '{exit_obj.key}' pour déverrouiller la porte vers '{direction}'.\n")
                exit_obj.locked = False
            else:
                print(f"\nLa porte vers '{direction}' est verrouillée. Il vous faut '{exit_obj.key}' pour l'ouvrir.\n")
                return True
        
        
        player.current_room = exit_obj.destination
        player.history.append(player.current_room) # On ajoute la salle actuelle à l'historique
        print(player.current_room.get_long_description())
        player.get_history()

        #quete : visiter une nouvelle pièce
        player.quest_manager.check_room_objectives(player.current_room.name)

        player.move_count += 1
        player.quest_manager.check_counter_objectives("Se déplacer", player.move_count)
        return True
                

    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "Up"], 0)
        False
        >>> quit(game, ["quit", "Up", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def history(game, list_of_words, number_of_parameters):

            l = len(list_of_words)
            if l != number_of_parameters + 1:
                command_word = list_of_words[0]
                print(MSG0.format(command_word=command_word))
                return False
            
            player = game.player
            player.get_history()
            return True
    
    def look(game, list_of_words, number_of_parameters):

            l = len(list_of_words)
            if l != number_of_parameters + 1:
                command_word = list_of_words[0]
                print(MSG0.format(command_word=command_word))
                return False
            
            room = game.player.current_room

            # gestion pièce sombre
            if room.dark and not game.player.has_item("lanterne"):
                print("\nIl fait trop sombre pour voir quoi que ce soit ici... Il vous faut une lanterne.\n")
                return True

            # Affichage inventaire de la pièce
            print(room.get_inventory())
            print(room.get_characters(game.characters))
            return True
            

    def take(game, list_of_words, number_of_parameters):
        l = len(list_of_words)
        if l < 2:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        #on accepte plusieurs mots pour le nom de l'objet
        else:
            command_word = list_of_words[0]
            list_word = list_of_words[1:]
            item_name = " ".join(list_word).lower()


        player = game.player
        room = player.current_room
        

        if item_name not in room.inventory:
            print(f"\nL'objet '{item_name}' n'est pas dans la pièce.\n")
            return True

        item = room.inventory[item_name]


        # transfert de la pièce vers inventaire du joueur
        item = room.inventory.pop(item_name)
        player.inventory[item_name] = item

        print(f"\nVous avez pris l'objet '{item_name}'.\n")
        player.quest_manager.check_action_objectives("prendre",item_name)
        return True        

    def drop(game, list_of_words, number_of_parameters):

        l = len(list_of_words)
        if l < 2:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        else:
            command_word = list_of_words[0]
            list_word = list_of_words[1:]
            item_name = " ".join(list_word).lower()

        player = game.player
        room = player.current_room


        if item_name not in player.inventory:
            print(f"\nL'objet '{item_name}' n'est pas dans l'inventaire.\n")
            return True

        # transfert inventaire du joueur vers la pièce
        item = player.inventory.pop(item_name)
        room.inventory[item_name] = item

        print(f"\nVous avez déposé l'objet '{item_name}'.\n")
        return True 
    
    def check(game, list_of_words, number_of_parameters):

            l = len(list_of_words)
            if l != number_of_parameters + 1:
                command_word = list_of_words[0]
                print(MSG0.format(command_word=command_word))
                return False
            
            player = game.player
            print(player.get_inventory())
            print(player.level_status())
            return True

    def back(game, list_of_words, number_of_parameters):
                # Vérification du nombre de paramètres
            l = len(list_of_words)
            if l != number_of_parameters + 1:
                command_word = list_of_words[0]
                print(MSG0.format(command_word=command_word))
                return False
            player = game.player
            # Si l'historique est vide, on ne peut pas revenir en arrière
            if not player.history:
                print("\nVous ne pouvez pas revenir en arrière : aucun déplacement précédent.\n")
                return True
            
            previous_room = player.history.pop() # On retire la dernière salle visitée (pop)
            player.current_room = previous_room # On déplace le joueur dans la salle précédente
            print(player.current_room.get_long_description()) # On affiche la description de la salle
            player.get_history() # Et on réaffiche l’historique restant
            return True

    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "Up"], 0)
        False
        >>> help(game, ["help", "Up", "E"], 0)
        False

        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True
    
    def talk(game, list_of_words, number_of_parameters):

        characters_here = game.get_characters_in_room()

        # talk
        if len(list_of_words) == 1:
            if not characters_here:
                print("\nÀ part le mur, il n'y a personne à qui parler.\n")
            else:
                print("\nVous pouvez parler à :")
                for c in characters_here:
                    print(f"    - {c.name}")
                print()
            return True

        # talk <nom>
        if len(list_of_words) >= 2:
            name = " ".join(list_of_words[1:]).lower()

            for c in characters_here:
                if c.name.lower() == name:
                    print("\n" + c.get_msg() + "\n")
                    game.player.quest_manager.check_action_objectives("parler à",c.name)
                    return True

            print("\nCette personne n'est pas ici.\n")
            return True

        print("\nParler à qui exactement ?\n")
        return False


    #La commande pour "combattre"
    def fight(game, list_of_words, number_of_parameters):
        player_in_room = game.player.current_room

        # les ennemis hostiles sont présent ?
        ennemis = [c for c in game.characters
                   if c.current_room == player_in_room and c.hostile and not c.defeated]
        
        # quand on ecrit fight sans argument
        if len(list_of_words) == 1:
            if not ennemis:
                print("\nA part le mur, il n'y a personne à combattre ici.\n")
                return True
            
            print("\nVous pouvez combattre :")
            for e in ennemis:
                print(f"    - {e.name} (niveau {e.level})")
            return True
        
        # quand on fait fight [nom de l'ennemi]
        target_name = " ".join(list_of_words[1:]).lower()
        target = next ((e for e in ennemis if e.name.lower() == target_name), None)

        if not target:
            print("\nQuirrel n'aperçoit aucun ennemi de ce nom ici.\n")
            return True
        
        Actions.resolve_fight(game.player,target)
        return True
    
    # Le combat n'est pas une mécanique qui nécessite au joueur d'effectuer des actions
    # dans notre jeu, c'est une porte qu'il faut enfoncer pour progresser dans l'histoire

    def resolve_fight(player, enemy):
        print(f"\nQuirrel affronte {enemy.name}...\n")

        if enemy.level > player.level:
            player.die()
            return
        
        print(f"Quirrel a vaincu d'un coup précis d'aiguillon {enemy.name}.")

        if enemy.is_boss:
            if enemy.defeated:
                print("Ce boss a déjà été vaincu.")
                return
            if enemy.reward_geos > 0:
                player.geos += enemy.reward_geos
                print(
                    f"\nVous récupérez {enemy.reward_geos} Geos "
                    f"sur les restes de {enemy.name}."
                )
            enemy.defeated = True
            player.quest_manager.check_action_objectives("vaincre", enemy.name)
            player.level += 1
            print (f"\nQuirrel s'est amélioré dans l'art de l'aiguillon grâce à ce combat !\nSon niveau augmente ! \nNiveau actuel : {player.level}\n")

    def quests(game, list_of_words, number_of_parameters):
        """
        Show all quests and their status.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quests(game, ["quests"], 0)
        <BLANKLINE>
        📋 Liste des quêtes:
          ❓ Grand Explorateur (Non activée)
          ❓ Grand Voyageur (Non activée)
          ❓ Découvreur de Secrets (Non activée)
        <BLANKLINE>
        True
        >>> Actions.quests(game, ["quests", "param"], 0)
        <BLANKLINE>
        La commande 'quests' ne prend pas de paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all quests
        game.player.quest_manager.show_quests()
        return True


    @staticmethod
    def quest(game, list_of_words, number_of_parameters):
        """
        Show details about a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quest(game, ["quest", "Grand", "Voyageur"], 1)
        <BLANKLINE>
        📋 Quête: Grand Voyageur
        📖 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        Objectifs:
          ⬜ Se déplacer 10 fois (Progression: 0/10)
        <BLANKLINE>
        🎁 Récompense: Bottes de voyageur
        <BLANKLINE>
        True
        >>> Actions.quest(game, ["quest"], 1)
        <BLANKLINE>
        La commande 'quest' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Prepare current counter values to show progress
        current_counts = {
            "Se déplacer": game.player.move_count
        }

        # Show quest details
        game.player.quest_manager.show_quest_details(quest_title, current_counts)
        return True


    @staticmethod
    def activate(game, list_of_words, number_of_parameters):
        """
        Activate a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.activate(game, ["activate", "Grand", "Voyageur"], 1) # doctest: +ELLIPSIS
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Grand Voyageur
        📝 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        True
        >>> Actions.activate(game, ["activate"], 1)
        <BLANKLINE>
        La commande 'activate' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Try to activate the quest
        if game.player.quest_manager.activate_quest(quest_title):
            return True

        msg1 = f"\nImpossible d'activer la quête '{quest_title}'. "
        msg2 = "Vérifiez le nom ou si elle n'est pas déjà active.\n"
        print(msg1 + msg2)
        # print(f"\nImpossible d'activer la quête '{quest_title}'. \
        #             Vérifiez le nom ou si elle n'est pas déjà active.\n")
        return False


    @staticmethod
    def rewards(game, list_of_words, number_of_parameters):
        """
        Display all rewards earned by the player.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.rewards(game, ["rewards"], 0)
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        True
        >>> Actions.rewards(game, ["rewards", "param"], 0)
        <BLANKLINE>
        La commande 'rewards' ne prend pas de paramètre.
        <BLANKLINE>
        False
        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all rewards
        game.player.show_rewards()
        return True
    
    def sell(game, list_of_words, number_of_parameters):
        player = game.player
        room = player.current_room

        # Personnages présents
        room_characters = [c for c in game.characters if c.current_room == room]

        sly = next((c for c in room_characters if c.name.lower() == "sly"), None)
        merchants = [c for c in room_characters if getattr(c, "merchant", False)]

        if not merchants and not sly:
            print("\nPersonne ici ne semble intéressé par vos objets.\n")
            return True

        # sell (sans argument)
        if len(list_of_words) == 1:
            sellable = [
                item for item in player.inventory.values()
                if item.value is not None and item.value > 0
            ]

            if not sellable:
                print("\nVous n'avez rien à vendre.\n")
                return True

            merchant = merchants[0] if merchants else sly
            print(f"\n{merchant.name} peut acheter :")
            for item in sellable:
                print(f"    - {item.name} ({item.value} Geos)")
            return True

        item_name = " ".join(list_of_words[1:]).lower()

        # 🔑 CAS SPÉCIAL : clé du marchand
        if item_name == "cle du marchand" and sly:
            if not player.has_item("cle du marchand"):
                print("\nVous n'avez pas cette clé.\n")
                return True

            # Retirer la clé (objet unique)
            del player.inventory["cle du marchand"]

            print("\nSly récupère la clé, son regard s'éclaire.\n")

            # ✅ Compléter l'objectif (PAS complete_quest)
            player.quest_manager.complete_objective("prendre cle du marchand")

            # Débloquer la boutique
            sly.current_room = game.dirtmouth
            sly.merchant = True
            sly.stock = {
                "lanterne": game.items["lanterne"],
                "blason de la ville": game.items["blason de la ville"]
            }
            sly.description = "Un marchand qui semble s'y connaître dans l'art de l'aiguillon."
            sly.msgs = [
                "Ah ! Ma clé ! Je commençais à désespérer.",
                "Ma boutique est de nouveau ouverte à Dirtmouth.",
                "Jette un œil à mes marchandises, voyageur."
            ]

            print("🛒 Boutique de Sly débloquée !\n  Sly se trouvera à présent à Dirtmouth.\n")
            return True

        # 💰 Vente classique
        item = player.inventory.get(item_name)
        if not item:
            print("\nVous ne possédez pas cet objet.\n")
            return True

        merchant = merchants[0] if merchants else sly

        if item.value is None or item.value <= 0:
            print(f"\n{merchant.name} n'est pas intéressé par cet objet.\n")
            return True

        player.geos += item.value
        del player.inventory[item_name]

        print(f"\n{merchant.name} vous donne {item.value} Geos pour {item.name}.")
        print(f"💰 Geos actuels : {player.geos}\n")

        return True

    
    def buy(game, list_of_words, number_of_parameters):
        player = game.player
        room = player.current_room

        merchants = [
            c for c in game.characters
            if c.current_room == room and c.merchant
        ]

        if not merchants:
            print("\nIl n'y a personne ici à qui acheter quoi que ce soit.\n")
            return True

        merchant = merchants[0]

        # buy (sans argument)
        if len(list_of_words) == 1:
            if not merchant.stock:
                print(f"\n{merchant.name} n'a rien à vendre.\n")
                return True

            print(f"\n{merchant.name} vend :")
            for item in merchant.stock.values():
                print(f"    - {item.name} ({item.value} Geos)")
            return True

        # buy <objet>
        item_name = " ".join(list_of_words[1:]).lower()

        if item_name not in merchant.stock:
            print(f"\n{merchant.name} ne vend pas cet objet.\n")
            return True

        item = merchant.stock[item_name]

        if player.geos < item.value:
            print("\nVous n'avez pas assez de Geos.\n")
            return True

        # transaction
        player.geos -= item.value
        player.inventory[item.name] = item
        del merchant.stock[item_name]

        print(
            f"\nVous achetez {item.name} pour {item.value} Geos."
            f"\nGeos restants : {player.geos}\n"
        )

        return True
    
    def train(game, list_of_words, number_of_parameters):
        player = game.player
        room = player.current_room

        trainers = [
            c for c in game.characters
            if c.current_room == room and c.trainer
        ]

        if not trainers:
            print("\nIl n'y a personne ici pour vous entraîner.\n")
            return True

        # train (sans argument)
        if len(list_of_words) == 1:
            print("\nVous pouvez vous entraîner auprès de :")
            for t in trainers:
                cost = t.training_cost
                print(f"    - {t.name} ({cost} Geos pour le niveau suivant)")
            return True

        # train <nom>
        target_name = " ".join(list_of_words[1:]).lower()

        trainer = next(
            (t for t in trainers if t.name.lower() == target_name),
            None
        )

        if not trainer:
            print("\nCette personne ne peut pas vous entraîner.\n")
            return True

        cost = trainer.training_cost * player.level

        if player.geos < cost:
            print("\nVous n'avez pas assez de Geos pour cet entraînement.\n")
            return True

        # entraînement réussi
        player.geos -= cost
        player.level += 1

        print(
            f"\n{trainer.name} vous entraîne longuement."
            f"\nVotre maîtrise de l'aiguillon s'améliore."
            f"\nNiveau actuel : {player.level}"
            f"\nGeos restants : {player.geos}\n"
        )

        return True


    def upgrade(game, list_of_words, number_of_parameters):
        player = game.player

        # Vérifier forgeron
        room = player.current_room
        forgeron = next(
            (c for c in game.characters if c.current_room == room and c.blacksmith),
            None
        )

        if not forgeron:
            print("\nIl n'y a personne ici capable d'améliorer votre arme.\n")
            return True

        COST = 500

        if player.geos < COST:
            print("\nVous n'avez pas assez de Geos.\n")
            return True

        minerai = player.get_minerai_pale()

        if not minerai:
            print("\nIl vous faut un minerai pâle pour améliorer votre aiguillon.\n")
            return True

        # Paiement
        player.geos -= COST
        del player.inventory[minerai.name]

        # Upgrade
        player.level += 1

        print(
            f"\nLe forgeron frappe l'aiguillon avec puissance...\n"
            f"L'aiguillon est amélioré !\n"
            f"Niveau actuel : {player.level}\n"
        )
        return True

