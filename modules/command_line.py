# command_line_interface.py
"""This module handles interacting with the user on the command line"""
from collections import OrderedDict


class CommandLine:
    '''This class contains interactions with the user via command line.'''
    def __init__(self, engine, prompt_func=input, print_func=print):
        self.prompt = prompt_func
        self.display = print_func
        self.command_mapping = self.commands(engine)

    def commands(self, engine):
        """Returns a list of valid commands in tuple form
        tuple is (command, function, description, valid_outside_room)
        """
        command_list = OrderedDict([
            ("q", (None, "退出游戏", True)),
            ("help", (engine.display_help, "显示帮助菜单", True)),
            ("begin", (engine.start, "开始游戏", True)),
            ("x", (engine.coordinates, "显示当前角色坐标", False)),
            ("exit", (engine.exit, "进入下一关地图", False)),
            ("c", (engine.item_count, "查看物品", False)),
            ("m", (self.map_key, "显示地图信息", True))
            ])

        return command_list

    def current_commands(self, in_room):
        """Returns information in tuple form on the commands that are currently
        valid; this can change based on whetheror not the player has typed
        'begin'
        """
        if in_room:
            commands = self.command_mapping
        else:
            commands = OrderedDict(filter(lambda x: x[1][2] == True, self.command_mapping.items()))
            #The x's passed into the lambda are (key,list) tuples from the command_mapping OrderedDict.

        return commands

    def display_help(self, in_room):
        """Creates a string containing all of the currently valid commands"""
        possible_commands = self.current_commands(in_room)

        help_text = """
听说你需要我的帮助？

下面是你可以用到的命令:
"""

        self.display(help_text)
        for command, command_list in possible_commands.items():
            self.display("{0} - {1}".format(command, command_list[1]))

    def map_key(self):
        """Displays a list of symbols on the map"""
        return self.display("""
        地图信息\n
        %s: 入口\n
        %s: 钥匙\n
        %s: 出口\n
        %s: 玩家\n
        %s: 黄金\n
        %s: 蟑螂\n
        %s: 神剑\n
        %s: 食物
        """ % ("入", "钥", "出", "我", "钱", "蟑", "剑", "食"))

    def greet(self):
        """Welcomes the player and gets their name"""
        #response = self.prompt("你好, 你叫什么名字: ")
        response = "冒险者"
        self.display("欢迎来到文字冒险游戏, {0}!".format(response))
        return response

    def display_end_of_game(self):
        """Displays the end of game message to the user"""
        self.display("恭喜你，你已经通关了。")
