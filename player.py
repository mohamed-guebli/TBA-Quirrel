# Define the Player class.
import random
from quest import QuestManager

class Player():
    '''
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
        
    '''
    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = {}
    # on peut aussi ajouter max_weight si on veut s'en servir
        self.max_weight = 10  # poids max en kg
        self.level = 1
        self.alive = True
        self.move_count = 0
        self.quest_manager = QuestManager(self)
        self.rewards = []  # List to store earned rewards

    
    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]
       
        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Set the current room to the next room.
        self.current_room = next_room
        self.history.append(next_room)
        print(self.current_room.get_long_description())
        self.get_history()
        
        # Check room visit objectives
        self.quest_manager.check_room_objectives(self.current_room.name)

        # Increment move counter and check movement objectives
        self.move_count += 1
        self.quest_manager.check_counter_objectives("Se déplacer", self.move_count)
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
        
        print("\nVous avez déja visité les pièces suivantes:")
        for room in self.history:
            print(f"    - {room.name}")

    def get_inventory(self):
        if not self.inventory:
            return "\nVotre inventaire est vide.\n"
        
        inv = "\nVous disposez des items suivants :\n"
        for item in self.inventory.values():
            inv += f"    - {item}\n"
        return inv
    
    def get_total_weight(self):
        total = 0
        for item in self.inventory.values():
            total += item.weight
        return total

    # pour détecter si le joueur possède un item
    def has_item(self, item_name):
        return item_name in self.inventory
    
    #fonction de la mort qui tue
    def die(self):
        print("Vous êtes mort...\n Quirrel, le royaume d'Hallownest a besoin de vous...\n")
        self.alive = False
        exit()