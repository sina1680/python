# -*- coding:utf-8 -*-
# level_loader.py
"""This module handles hydrating the levels from files"""

from os.path import join
import json
from modules.item import Item
from modules.monsters import Cockroach,Wolf, Dog,Monster
from modules.level import Level
from modules.weapon import Excalibur,Weapon
import random
class LevelLoader:
    """This class handles the loading of level data to and from files"""
    def __init__(self, library_path, first_file):
        self.room_file = first_file
        self.library_path = library_path
        self.description = None
        self.exit_text = None
        self.name = None
        self.next_level = None
        self.reset()

    def enter(self, player, entrance_name):
        """Inserts a locatable object into a level"""
        self.reset()
        level = self.get_room_data()
        locatable = level.get_by_name(entrance_name)
        coords = locatable.locate()
        player.enter(coords)
        level.add(player)
        return level

    def enter_next_level(self, player):
        """If the current level specifies a next level, this method will
        move the player from the current level to the next"""
        has_next_level = self.next_level != None
        level = None

        if has_next_level:
            self.room_file = self.next_level
            level = self.enter(player, "entrance")

        return level, has_next_level

    def reset(self):
        """Returns the state of the object to it's initial values"""
        self.exit_text = None
        self.next_level = None
        self.name = None
        self.description = None
        self.contents = []

    def room_description(self):
        """Returns the description of the level"""
        return self.description

    def get_room_data(self):
        """finds and reads the level file and returns a level object ready
        to use"""
        path_n_file = join(self.library_path, self.room_file)

        with open(path_n_file, "rb") as file_handle:
            data = json.load(file_handle)

        size = data['size']
        contents = hydrate(data['locations'],size)
        

        level = Level(contents, size)

        self.name = data['room']
        self.description = data['description']

        room_keys = data.keys()

        if 'exit_text' in room_keys:
            self.exit_text = data['exit_text']

        if 'next_level' in room_keys:
            self.next_level = data['next_level']
        else:
            self.next_level = None

        return level

def hydrate(data,size):
    random_place = []
    """Populates the level with data from the file"""
    contents = []
    
    if data == None:
        return contents

    for key, value in data.items():
        content_type = "item"
        keys = value.keys()
        description = None
        target = None
        damage = None

        if "x" not in keys or "y" not in keys:
            pass
        else:
            if "type" in keys:
                content_type = value["type"]

            if "description" in keys:
                description = value["description"]

            if "target" in keys:
                target = value["target"]

            if "damage" in keys:
                damage = value["damage"]
            if content_type == "creature":
                if value["display"] == "蟑":
                    locatable = Cockroach(key, description)
                elif value["display"] == "狗":
                    locatable = Dog(key, description)
                elif value["display"] == "狼":
                    locatable = Wolf(key, description)
                else:
                    locatable = Dog(key, description)
                locatable.target = target
		# if target:
                #     for itm in contents:
                #         if itm.name == target:
                #             locatable.set_target(itm)
                #     else:
                #         #What should go here?
                #         pass
            else:
                locatable = Item(key, description)

            if content_type == "weapon":
                if value["display"] == "剑":
                    locatable = Excalibur(damage)
                locatable.name = key
                locatable.description = description
            post_x = random.randint(0,size-1)
            post_y = random.randint(0,size-1)
            post_data=str(post_x)+'*'+str(post_y)
            while post_data in random_place:
                post_x = random.randint(0,size-1)
                post_y = random.randint(0,size-1)
                post_data=str(post_x)+'*'+str(post_y) 
            random_place.append(post_data)

            locatable.place((post_x, post_y))

            if "display" in keys:
                locatable.set_display(value["display"])

            contents.append(locatable)
    index=[]
    for item in contents:
        if isinstance(item, Monster):
            index.append(contents.index(item))
    for i in index:
        creature = contents.pop(i)
        for itm in contents:
            if itm.name == creature.target: 
                creature.set_target(itm)
        contents.insert(i,creature)
    return contents
