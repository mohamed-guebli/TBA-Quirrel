# Define the Player class.
from quest import QuestManager
from door import Door


class Player:
    """
    This class represents a player in the game. A player has a name and a current room.

    Attributes:
        name(str) : The name.
        current_room(Room) : The current room.

    Methods:
        __init__(self,name) : The constructor.
        move(self,direction) : Move the player in the given direction.

    Examples:
    >>> player = Player("Hero")
    >>> player.name
    'Hero'
    >>> player.current_room is None
    True
    >>> from room import Room
    >>> room1 = Room("Salle de départ", "dans la salle de départ", {})
    >>> room2 = Room("Salle de nord", "dans la salle au nord", {})
    >>> room1.exits['N'] = room2
    >>> player.current_room = room1
    >>> player.move('N')
    '\nVous êtes dans la salle au nord\n\nSorties: \n'
    >>> player.current_room == room2
    True

    """

    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = {}
        self.geos = 0
        self.level = 1
        self.alive = True
        self.move_count = 0
        self.quest_manager = QuestManager(self)
        self.rewards = []  # List to store earned rewards
        self.history_limit = 5

        # Define the move method.

    def move(self, direction):
        exit_obj = self.current_room.exits.get(direction)

        if exit_obj is None:
            print("\nAucune porte dans cette direction !\n")
            return False

        # Gestion des portes
        if isinstance(exit_obj, Door):
            if exit_obj.locked:
                if exit_obj.key and self.has_item(exit_obj.key):
                    exit_obj.locked = False
                    print(
                        "\nVous utilisez le Trampass. La voie est maintenant ouverte.\n"
                    )
                else:
                    print(
                        "\nCette voie est verrouillée. Il vous manque quelque chose...\n"
                    )
                    return False
            next_room = exit_obj.destination
        else:
            next_room = exit_obj

        # Sauvegarde de la pièce précédente
        self.history.append(self.current_room)

        # Déplacement
        self.current_room = next_room
        print(self.current_room.get_long_description())
        self.get_history()

        # Quêtes et compteurs
        self.quest_manager.check_room_objectives(self.current_room.name)
        self.move_count += 1
        self.quest_manager.check_counter_objectives(
            "Se déplacer", self.move_count)
        if hasattr(self, "game"):
            self.game.move_zote_randomly()

        return True

    def add_reward(self, reward):
        """
        Add a reward to the player's rewards list.

        Args:
            reward (str): The reward to add.

        Examples:

        >>> player = Player("Bob")
        >>> player.add_reward("Épée magique") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Épée magique
        <BLANKLINE>
        >>> "Épée magique" in player.rewards
        True
        >>> player.add_reward("Épée magique") # Adding same reward again
        >>> len(player.rewards)
        1
        """
        if reward and reward not in self.rewards:
            self.rewards.append(reward)
            print(f"\n🎁 Vous avez obtenu: {reward}\n")

    def show_rewards(self):
        """
        Display all rewards earned by the player.

        Examples:

        >>> player = Player("Charlie")
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        >>> player.add_reward("Bouclier d'or") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Bouclier d'or
        <BLANKLINE>
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vos récompenses:
        • Bouclier d'or
        <BLANKLINE>
        """
        if not self.rewards:
            print("\n🎁 Aucune récompense obtenue pour le moment.\n")
        else:
            print("\n🎁 Vos récompenses:")
            for reward in self.rewards:
                print(f"  • {reward}")
            print()

    def get_history(self):
        if not self.history:
            return

        limit = self.history_limit
        recent_rooms = self.history[-limit:]

        print("\nVous avez déja visité les pièces suivantes:")
        for room in recent_rooms:
            print(f"    - {room.name}")

    def get_inventory(self):
        inv = f"\n💰 Geos : {self.geos}\n"

        if not self.inventory:
            inv += "\nVotre inventaire est vide.\n"
            return inv

        inv += "\nVous disposez des items suivants :\n"
        for item in self.inventory.values():
            inv += f"    - {item}\n"

        return inv

    # pour détecter si le joueur possède un item
    def has_item(self, item_name):
        return item_name in self.inventory

    # fonction de la mort qui tue
    def die(self):
        print(
            "Vous êtes mort...\n Quirrel, le royaume d'Hallownest a besoin de vous...\n"
        )
        self.alive = False

    def get_minerai_pale(self):
        """
        Retourne le premier minerai pâle trouvé dans l'inventaire, ou None.
        """
        for item in self.inventory.values():
            if item.name.startswith("minerai pale"):
                return item
        return None

    def remove_item(self, item_name):
        """
        Retire un item de l'inventaire du joueur.

        Args:
            item_name (str): Le nom de l'item à retirer.

        Examples:

        >>> player = Player("Alice")
        >>> from item import Item
        >>> sword = Item("épée", "Une épée en acier.", value=100)
        >>> player.inventory[sword.name] = sword
        >>> player.remove_item("épée")
        True
        >>> player.has_item("épée")
        False
        >>> player.remove_item("bouclier")
        False
        """
        if item_name in self.inventory:
            del self.inventory[item_name]
            return True
        return False

    def add_item(self, item):
        """
        Ajoute un item à l'inventaire du joueur.

        Args:
            item (Item): L'item à ajouter.

        Examples:

        >>> player = Player("Alice")
        >>> from item import Item
        >>> sword = Item("épée", "Une épée en acier.", value=100)
        >>> player.add_item(sword)
        >>> player.has_item("épée")
        True
        """
        self.inventory[item.name] = item

    def has_item(self, item_name):
        """
        Vérifie si le joueur possède un item dans son inventaire.

        Args:
            item_name (str): Le nom de l'item à vérifier.

        Returns:
            bool: True si l'item est dans l'inventaire, False sinon.

        Examples:

        >>> player = Player("Alice")
        >>> from item import Item
        >>> sword = Item("épée", "Une épée en acier.", value=100)
        >>> player.add_item(sword)
        >>> player.has_item("épée")
        True
        >>> player.has_item("bouclier")
        False
        """
        return item_name in self.inventory

    def level_status(self):
        """
        Retourne une chaîne décrivant le niveau actuel du joueur.

        Examples:

        >>> player = Player("Alice")
        >>> player.level_status()
        '\n⭐ Niveau actuel : 1\n'
        >>> player.level = 5
        >>> player.level_status()
        '\n⭐ Niveau actuel : 5\n'
        """
        return f"\n⭐ Niveau actuel : {self.level}\n"
