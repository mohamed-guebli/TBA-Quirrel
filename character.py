#character.py
import random
class Character:
    """"""
    """"""

    def __init__(self, name : str, description : str, current_room : str, msgs : list, level: int = 1, hostile: bool = False, is_boss: bool = False, merchant=False, stock=None,trainer = False,training_cost = 0, reward_geos=0, blacksmith = False, upgrade_cost = 0):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs
        self.level = level
        self.hostile = hostile
        self.is_boss = is_boss
        self.defeated = False
        self.merchant = merchant
        self.stock = stock if stock is not None else {}
        self.trainer = trainer
        self.training_cost = training_cost
        self.reward_geos = reward_geos
        self.blacksmith = blacksmith
        self.upgrade_cost = upgrade_cost
        
    def __str__(self):
        return f"{self.name} : {self.description}"
    
    def move(self):
        """
        Déplace les PNJ aléatoirement avec une chance sur deux.
        Retourne True si le PNJ s'est déplacé, False sinon.
        """
        if random.choice([True, False]):
            # Récupérer les pièces adjacentes valides
            possible_exits = [room for room in self.current_room.exits.values() if room is not None]
            if not possible_exits:
                return False

            # Choisir une pièce adjacente au hasard
            next_room = random.choice(possible_exits)

            # Mettre à jour la pièce actuelle et l'historique
            self.current_room = next_room

            return True
        else:
            #Les PNJ ne se déplacent pas
            return False
        
    def get_msg(self):
        if not self.msgs :
            return "..."
        msg = self.msgs.pop(0)
        self.msgs.append(msg)
        return msg