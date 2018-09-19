# player.py
from modules.hp import HealthPoints
""" This is the module for all things player related"""
from modules.locatable import Locatable
from modules.hp import HealthPoints
from modules.weapon import Weapon
import random
class Player(Locatable, HealthPoints):
    """This class holds information about the player."""
    def __init__(self, name):
        Locatable.__init__(self)
        HealthPoints.__init__(self, 100)
        self.description = name
        self.name = "player"
        self.display = "我"
        self.display_priority = 1
        self.inside = False
        self.wea = None
        self.maxph = 100

    def in_room(self):
        """Called to determine if the player is inside or outside a level"""
        return self.inside

    def enter(self, coords):
        """Places the player in a level at a particular location"""
        self.place(coords)
        self.inside = True

    def exit(self):
        """Removes the player from a level"""
        self.inside = False
    #玩家的初始攻击力
    weapon = Weapon(2)
    deviation = 1
    
    def dies(self):
        return "你被杀死了!\n胜败乃兵家常事 大侠请重新来过。"
