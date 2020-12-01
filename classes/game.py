import random
from .magic import Spell
import pprint


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    B0LD = "\033[1m"
    UNDERLINE = "\033[4m"


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.name = name
        self.actions = ["Attack", "Magic", "Items"]

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        self.hp = self.hp - dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp = self.hp + dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp = self.mp - cost

    def choose_action(self):
        i = 1
        print("    " + bcolors.B0LD + self.name + bcolors.ENDC)
        print(bcolors.OKBLUE + bcolors.B0LD + "    Actions" + bcolors.ENDC)
        for item in self.actions:
            print("    " + str(i) + ":", item)
            i = i+1

    def choose_magic(self):
        i = 1
        print(bcolors.OKBLUE + bcolors.B0LD + "        Magic" + bcolors.ENDC)
        for spell in self.magic:
            print("        " + str(i) + ":", spell.name, "(cost:", str(spell.cost) + ")")
            i = i+1

    def choose_items(self):
        i = 1
        print(bcolors.OKGREEN + bcolors.B0LD + "        ITEMS:", bcolors.ENDC)
        for item in self.items:
            print("        " + str(i) + ".", item["item"].name, ":", item["item"].description, " (x", item["quantity"], ")")
            i = i+1

    def choose_target(self, enemies):
        i = 1
        print("\n" + bcolors.FAIL + bcolors.B0LD + "    TARGET:" + bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print("        " + str(i) + ". " + enemy.name)
                i = i+1
        choice = int(input("    choose Target:")) - 1
        return choice

    def get_enemy_stats(self):
        hp_bar = ""
        bar_tick = (self.hp/self.maxhp)*100/2

        while bar_tick > 0:
            hp_bar = hp_bar + "█"
            bar_tick = bar_tick -1
        while len(hp_bar) < 50:
            hp_bar = hp_bar + " "
        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""
        if len(str(self.hp)) != len(str(self.maxhp)):
            decreased = len(str(self.maxhp)) - len(str(self.hp))
            while decreased > 0:
                current_hp = current_hp + " "
                decreased = decreased - 1
            current_hp = current_hp + hp_string
        else:
            current_hp = hp_string
        print("                     __________________________________________________")
        print(bcolors.B0LD + self.name + ":    " + current_hp + "|" + bcolors.FAIL +
              hp_bar + bcolors.ENDC + "|")

    def get_stats(self):
        hp_bar = ""
        hp_bar_ticks = int((self.hp/self.maxhp) * 25)
        while hp_bar_ticks > 0:
            hp_bar = hp_bar + "█"
            hp_bar_ticks = hp_bar_ticks - 1
        while len(hp_bar) < 25:
            hp_bar = hp_bar + " "

        mp_bar = ""
        mp_bar_ticks = int((self.mp / self.maxmp) * 10)
        while mp_bar_ticks > 0:
            mp_bar = mp_bar + "█"
            mp_bar_ticks = mp_bar_ticks - 1
        while len(mp_bar) < 10:
            mp_bar = mp_bar + " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""
        if len(str(self.hp)) != len(str(self.maxhp)):
            decreased = len(str(self.maxhp)) - len(str(self.hp))
            while decreased > 0:
                current_hp = current_hp + " "
                decreased = decreased - 1
            current_hp = current_hp + hp_string
        else:
            current_hp = hp_string

        mp_string = str(self.mp) + "/" + str(self.maxmp)
        current_mp = ""
        if len(str(self.mp)) != len(str(self.maxmp)):
            decreased = len(str(self.maxmp)) - len(str(self.mp))
            while decreased > 0:
                current_hp = current_hp + " "
                decreased = decreased - 1
            current_mp = current_mp + mp_string
        else:
            current_mp = mp_string

        print("                  _________________________          __________")
        print(bcolors.B0LD + self.name + ":    " + current_hp + "|" + bcolors.OKGREEN +
              hp_bar + bcolors.ENDC + bcolors.B0LD + "| " + mp_string +
              "  |" + bcolors.OKBLUE + mp_bar + bcolors.ENDC + "|")

    def enemy_choose_magic(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg = spell.generate_damage()
        if self.mp < spell.cost:
            self.enemy_choose_magic()
        else:
            return spell, magic_dmg

