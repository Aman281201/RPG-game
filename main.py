from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Items
import random


# create black magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 14, 140, "black")

# create white magic

cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")


# creating some items
potion = Items("Potion", "potion", "Heals 50 HP", 50)
hipotion = Items("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Items("Super-Potion", "potion", "Heals 500 HP", 500)

elixir = Items("Elixir", "elixir", "Fully restores HP/MP of one member", 9999)
hielixir = Items("MegaElixir", "elixir", "Fully restores HP/MP of the Team", 9999)

grenade = Items("Grenade", "attack", "Deals 500 Damage", 500)

# initialization of player and enemy
player_spells = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixir, "quantity": 5},
                {"item": hielixir, "quantity": 2}, {"item": grenade, "quantity": 5}]

player1 = Person("Valos", 460, 65, 60, 34, player_spells, player_items)
player2 = Person("Nick ", 460, 65, 60, 34, player_spells, player_items)
player3 = Person("Robot", 460, 65, 60, 34, player_spells, player_items)

players = [player1, player2, player3]

enemy_spells = [fire, meteor, cure]
enemy1 = Person("Magnus", 3000, 65, 100, 15, enemy_spells, [])
enemy2 = Person("Imp1  ", 1200, 70, 60, 10, enemy_spells, [])
enemy3 = Person("Imp2  ", 1200, 70, 60, 10, enemy_spells, [])

enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.B0LD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("=====================================")
    print("Name              HP                                 MP")
    for player in players:
        player.get_stats()
    print("\n\n")
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        print("\n\n")

        player.choose_action()
        choice = input("choose action:")
        index = int(choice) - 1
        if index == 0:
            dmg = player.generate_damage()

            enemy = enemies[player.choose_target(enemies)]

            enemy.take_damage(dmg)
            print("you attacked " + enemy.name.replace(" ", "") + "for" + str(dmg) + "points of damage. ")

            if enemy.get_hp() == 0:
                print(enemy.name.replace(" ", "") + "has died")
                i = 0
                for enem in enemies:

                    if enemy == enemies[i]:
                        del enemies[i]
                        break
                    i = i + 1

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("choose the magic you would like to use")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]

            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()
            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nyou don't have enough MP to use this spell\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)

            elif spell.type == "black":
                enemy = enemies[player.choose_target(enemies)]

                enemy.take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to" + enemy.name)

            if enemy.get_hp() == 0:
                print(enemy.name.replace(" ", "") + "has died")
                i = 0
                for enem in enemies:

                    if enemy == enemies[i]:
                        del enemies[i]
                        break
                    i = i + 1

        elif index == 2:
            player.choose_items()
            item_choice = int(input("Enter your choice")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]
            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + item.name + " has been finished" + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] = player.items[item_choice]["quantity"] - 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + "heals for", str(item.prop), "HP" + bcolors.ENDC)
            if item.type == "elixir":
                player.hp = player.maxhp
                player.mp = player.maxmp
                print(bcolors.OKGREEN + item.name + "fully restores HP/MP" + bcolors.ENDC)
            if item.type == "attack":
                enemy = enemies[player.choose_target(enemies)]

                enemy.take_damage(item.prop)
                print(bcolors.FAIL + item.name + "deals damage of", str(item.prop) + "to" + enemy.name + bcolors.ENDC)

                if enemy.get_hp() == 0:
                    print(enemy.name.replace(" ", "") + "has died")
                    i = 0
                    for enem in enemies:

                        if enemy == enemies[i]:
                            del enemies[i]
                            break
                        i = i+1
                                                                                                                        
        defeated_enemies = 0
        defeated_players = 0

        for enemy in enemies:
            if enemy.get_hp() == 0:
                defeated_enemies = defeated_enemies + 1
        for player in players:
            if player.get_hp() == 0:
                defeated_players = defeated_players + 1

        if enemy.get_hp() == 0 and player.get_hp() == 0:
            print(bcolors.OKBLUE + "Tie!!" + bcolors.ENDC)
            running = False

        elif defeated_enemies == 2:
            print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
            running = False
        elif defeated_players == 3:
            print(bcolors.FAIL + "Your enemy has defeated you!" + bcolors.ENDC)
            running = False

    for enemy in enemies:
        enemy_choice = random.randrange(0,2)
        if enemy_choice == 0:
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print(enemy.name + " did damage of " + str(enemy_dmg) + " to " + players[enemy_choice].name)
            if players[target].get_hp() == 0:
                print(bcolors.FAIL + players[target].name + " has died" + bcolors.ENDC)
                del players[target]

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.enemy_choose_magic()
            print(enemy.name + "chose" + spell.name)
            target = random.randrange(0, 3)
            if spell.type == 'black':
                players[target].take_damage(magic_dmg)
                print(spell.name + " spell deals damage of " + str(magic_dmg) + " on " + players[target].name)
            elif spell.type == 'white':
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + "heals " + enemy.name.replace(" ", "") + " for " + str(magic_dmg) +
                      "HP" + bcolors.ENDC)
            if players[target].get_hp() == 0:
                print(bcolors.FAIL + players[target].name + "has died" + bcolors.ENDC)
                del players[target]






