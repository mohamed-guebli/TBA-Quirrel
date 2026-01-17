#character.py
import random
class Character:
    """"""
    """"""

    def __init__(self, name : str, description : str, current_room : str, msgs : list,
                  level: int = 1, hostile: bool = False, is_boss: bool = False,
                  merchant=False, stock=None,
                  trainer = False,training_cost = 0, reward_geos=0,
                  blacksmith = False, upgrade_cost = 0):
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
    
    def move_between(self, room_a, room_b):
        """
        Fait bouger le PNJ aléatoirement entre deux salles.
        """
        self.current_room = random.choice([room_a, room_b])
        
    def get_msg(self):
        if not self.msgs :
            return "..."
        msg = self.msgs.pop(0)
        self.msgs.append(msg)
        return msg