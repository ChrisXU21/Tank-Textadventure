import random, time
import variables
from wrapper import error, number_input
from os import system
from math import floor, sqrt
from inspect import currentframe

class Event():
    def __init__(self, e_type:int, turn:int, follows:bool = False):
        self.e_type = e_type
        self.turn = turn
        self.follows = follows


def scout(player_tank, surroundings:list, events:list, enemies:int, allies:int, tanks):
    try:
        print(" - SCOUT -")
        if False in variables.scouted.values():
            if player_tank.inventory['spyglasses'] > 0:
                variables.stats["scouted"] += 1
                player_tank.inventory['spyglasses'] -= 1
                print("You use a battery on your spyglasses and peek out of your tank to take look around...")
                time.sleep(3)
                print(f"You see the following tanks: West - {variables.factions[surroundings[1].allegiance] if surroundings[1] != None else 'None'} | North - {variables.factions[surroundings[2].allegiance] if surroundings[2] != None else 'None'} | East - {variables.factions[surroundings[3].allegiance] if surroundings[3] != None else 'None'}\n")
                for i in range(1, 4):
                    variables.scouted[i] = True
                time.sleep(4)
                ammo = random.randint(0, 1)
                if ammo != 0:
                    print(f"You have {player_tank.inventory['spyglasses']} {'batteries' if player_tank.inventory['spyglasses'] != 1 else 'battery'} left!\nYou additionally found {ammo} {'shell and take it with you' if ammo == 1 else 'shells and take them with you'}!")
                    player_tank.ammo_change(True, ammo)

                if surroundings[2] != None:
                    if surroundings[2].allegiance != player_tank.allegiance:
                        print("You feel like the northern tank may have seen you and quickly rush back to your tank, getting ready to engage.")
                        if surroundings[2].turn == None:
                            surroundings[2].turn = 2 # After your next turn, it will attack
                    else:
                        print(f"The commander of the allied tank to your north {random.choice(variables.northern_ally_lines)}")
            else:
                print("You want to grab a battery of yours to put into your spyglasses, only for you to notice you no longer have any.")
                return player_tank, surroundings, events, enemies, allies, False, tanks
        else:
            print(f"You quickly remind yourself of the positions of the tanks around you:\nWest - {variables.factions[surroundings[1].allegiance] if surroundings[1] != None else 'None'} | North - {variables.factions[surroundings[2].allegiance] if surroundings[2] != None else 'None'} | East - {variables.factions[surroundings[3].allegiance] if surroundings[3] != None else 'None'}")
            return player_tank, surroundings, events, enemies, allies, False, tanks
        
        print("\n-----\n")
        return player_tank, surroundings, events, enemies, allies, True, tanks
    except Exception as ex:
        error(ex, currentframe().f_code.co_name)


def atk(player_tank, surroundings:list, events:list, enemies:int, allies:int, tanks):
    try:
        print(" - ATTACK -")
        print(f"Which one do you want to shoot?\n1. West{f' - {variables.factions[surroundings[1].allegiance]}' if variables.scouted[1] == True and surroundings[1] != None else ' - Unkown' if surroundings[1] != None else ' - None'}\n2. North{f' - {variables.factions[surroundings[2].allegiance]}' if variables.scouted[2] == True and surroundings[2] != None else ' - Unkown' if surroundings[2] != None else ' - None'}\n3. East{f' - {variables.factions[surroundings[3].allegiance]}' if variables.scouted[3] == True and surroundings[3] != None else ' - Unkown' if surroundings[3] != None else ' - None'}\n - - -\n4. Return")

        # Wait for correct player input
        action = number_input(maxi=4)
        
        if action != 4:
            target_allegiance = surroundings[action].allegiance
            if player_tank.loaded == True:
                variables.stats["rounds_shot"] += 1
                # Radio report - Shell is loaded
                if surroundings[action] != None:
                    part_chance = (60, 80, 95)
                    if random.randint(1, 100) > part_chance[player_tank.upgrades['barrel'] - 1]:
                        shot_success = True
                    else:
                        print("This is a hard shot to do and the barrel is a bit shakey. You gotta shout just at the right time...")
                        if skillcheck(random.choice(variables.confront_skillcheck), variables.difficulty, player_tank, "barrel") == 0:
                            shot_success = True
                        else:
                            shot_success = False

                    if shot_success == True:
                        print(f"You shoot a tank of the {variables.factions[surroundings[action].allegiance]} and pick up the radio...")
                        time.sleep(1)
                        if surroundings[action].allegiance == player_tank.allegiance:
                            variables.stats["killed_allies"] += 1
                            print(f"\"{random.choice(variables.shot_ally_lines)}\" *click*")
                            allies -= 1
                        else:
                            variables.stats["killed_enemies"] += 1
                            print(f"\"{random.choice(variables.shot_enemy_lines)}\" *click*")
                            enemies -= 1

                        tanks.remove(surroundings[action])
                        surroundings[action] = None
                    else:
                        if surroundings[action].allegiance != player_tank.allegiance:
                            print(f"You miss your shot and pick up the radio...\n\"{random.choice(variables.shot_empty_lines)}\" *click*\nThe enemy you just shot at will definitely go for you now...")
                            surroundings[action].turn = 2
                        else:
                            print(f"You miss your shot and pick up the radio...\n\"{random.choice(variables.shot_ally_lines)}\" *click*")

                else:
                    print(f"You shoot at an empty spot and pick up the radio...\n\"{random.choice(variables.shot_empty_lines)}\" *click*")


                player_tank.ammo_change(False, 1)
                player_tank.loaded = False
                print(f"You have {player_tank.inventory['shells']} {'shell' if player_tank.inventory['shells'] == 1 else 'shells'} remaining and need to reload now!\nAll enemy tanks around you have heard the action and may engage in the next few turns.")
                # Makes enemies around you agro
                for pos, tank in surroundings.items():
                    if tank != None:
                        if tank.allegiance != player_tank.allegiance:
                            if tank.turn == None:
                                if random.randint(1, 10) < 9:
                                    tank.turn = random.randint(3, 4) # After 2 or 3 turns they will attack you
                        else:
                            if random.randint(1, 10) > 3 and target_allegiance != player_tank.allegiance and shot_success == True:
                                variables.scouted[pos] = True
                                print(f"The commander of the {'western' if pos == 1 else 'northern' if pos == 2 else 'eastern'} tank {random.choice(variables.kill_cheer_ally_lines)}")
                print("\n-----\n")
            else:
                # Shell not loaded
                print("You try to shoot, but there is no shell loaded.\n\n-----\n")

            return player_tank, surroundings, events, enemies, allies, True, tanks
        else:
            return player_tank, surroundings, events, enemies, allies, False, tanks
    except Exception as ex:
        error(ex, currentframe().f_code.co_name)


def move(player_tank, surroundings:list, events:list, enemies:int, allies:int, tanks):
    try:
        print(" - MOVE -")
        variables.stats["moves"] += 1
        can_move = True
        print(f"In which direction do you want to go?\n1. West{f' - {variables.factions[surroundings[1].allegiance]}' if variables.scouted[1] == True and surroundings[1] != None else ' - Unkown' if surroundings[1] != None else ' - None'}\n2. North{f' - {variables.factions[surroundings[2].allegiance]}' if variables.scouted[2] == True and surroundings[2] != None else ' - Unkown' if surroundings[2] != None else ' - None'}\n3. East{f' - {variables.factions[surroundings[3].allegiance]}' if variables.scouted[3] == True and surroundings[3] != None else ' - Unkown' if surroundings[3] != None else ' - None'}\n - - -\n4. Return")

        # Wait for correct player input
        action = number_input(maxi=4)

        if action != 4:
            if surroundings[action] != None:
                if surroundings[action].allegiance == player_tank.allegiance:
                    # Field is occupied by friendly
                    # Spyglass stuff
                    if surroundings[action].inventory['spyglasses'] != 0:
                        maggi = random.randint(1, surroundings[action].inventory['spyglasses'])
                        surroundings[action].inventory['spyglasses'] -= maggi
                        player_tank.inventory['spyglasses'] += maggi

                    # AA stuff
                    d = False
                    if surroundings[action].inventory['anti-air'] == True and player_tank.inventory['anti-air'] == False:
                        surroundings[action].inventory['anti-air'] = False
                        player_tank.inventory['anti-air'] = True
                        d = True

                    # Tank shell stuff
                    shelli = random.randint(1, surroundings[action].inventory['shells'])
                    surroundings[action].ammo_change(False, shelli)
                    player_tank.ammo_change(True, shelli)
                    if surroundings[action].inventory['shells'] == 0:
                        tanks.remove(surroundings[action])
                        surroundings[action] = None
                        allies -= 1
                        t = "won't return to the battlefield"
                    else:
                        t = "will return to the battlefield"

                    print(f"You drive near an allied tank and they decide to spare {shelli} {'shell' if shelli == 1 else 'shells'}{f' and {maggi} batteries' if 'maggi' in locals() and maggi != 1 else f' and {maggi} battery' if 'maggi' in locals() else ''} with you!\n\"{random.choice(variables.ally_interaction_lines)}\"\n{'Before falling back they remember they have an AA gun assigned to their command and decide to reassign it to you instead! - ' if d == True else ''}They're falling back and {t}.")
                    time.sleep(3)
                else:
                    # Field is occupied by enemy
                    print("You drive near an enemy tank and engage them directly. Think fast!")

                    if player_tank.loaded == False:
                        print("You currently have no shell loaded! Attempt a quick-reload!")
                        time.sleep(2)
                        quickload = skillcheck(random.choice(variables.broken_part), variables.difficulty, player_tank, "barrel")
                        variables.difficulty -= 0.075
                        if quickload == 0:
                            player_tank.loaded = True

                    if player_tank.loaded == True:
                        time.sleep(2)
                        deadoralive = skillcheck(random.choice(variables.confront_skillcheck), variables.difficulty, player_tank, "barrel", True)
                        variables.difficulty -= 0.075

                        if deadoralive[0] == 0:
                            print(f"You and your crew successfully blast away the tank in front of you. The radio buzzes...\n\"{random.choice(variables.shot_enemy_lines)}\" *click*")
                            player_tank.ammo_change(False, 1)
                            player_tank.loaded = False
                            enemies -= 1

                            tanks.remove(surroundings[action])
                            surroundings[action] = None
                        else:
                            print(f"{f'You were given {floor(deadoralive[2])} milliseconds of time, but with {floor(deadoralive[1])} milliseconds you were too slow' if deadoralive[0] == 1 else 'You gave a wrong command'}.")
                            player_tank = None
                    else:
                        print(f"You didn't manage to reload fast enough!")
                        player_tank = None
            else:
                # Field is empty
                # Driving
                print(f"You drive to the {'west' if action == 1 else 'north' if action == 2 else 'east'} and...")
                time.sleep(1)

                part_chance = (60, 80, 95)
                if random.randint(1, 200) > (part_chance[player_tank.upgrades['engine'] - 1] + part_chance[player_tank.upgrades['tracks'] - 1]): # Something fails
                    if random.randint(1, part_chance[player_tank.upgrades['engine'] - 1] + part_chance[player_tank.upgrades['tracks'] - 1]) > part_chance[player_tank.upgrades['engine'] - 1]:
                        # Engine failure
                        print("You hear your engine burst! Motivate your engineer!")
                        if skillcheck(random.choice(variables.broken_part), variables.difficulty, player_tank, "engine") == 0:
                            print("Your tank's engine cries as it turns back on!\nYou continue your drive...")
                        else:
                            can_move = False
                            print("Your motivation skills are lacking.\nThe engine is repaired now, but you didn't manage to move yet...")
                    else:
                        # Tracks failure
                        print("Your tracks get stuck! Motivate your engineer to fix them!")
                        if skillcheck(random.choice(variables.broken_part), variables.difficulty, player_tank, "tracks") == 0:
                            print("Your engineer jumps out of the tank with a quick movement and fixes the tracks in no-time!\nYou continue your drive...")
                        else:
                            can_move = False
                            print("Your motivation skills are lacking.\nThe engineer fixed the tracks now, but you didn't manage to move yet...")
                else: # All goes well
                    print("Don't run into any problems doing so.")

                # Reached the spot (P.O.W. stuff)
                if random.randint(1, 10) < 5: # 40% chance
                    player_tank = powstuff(player_tank)

            if can_move == True:
                for pos in surroundings:
                    if surroundings[pos] != None:
                        if surroundings[pos].turn != None:
                            surroundings[pos].ammo_change(False, 1)
                            surroundings[pos].turn = None
                keep = []
                for e in events:
                    if e.follows == False:
                        print("\nWARNING LIFTED - YOU DROVE AWAY FROM DANGER")
                    else:
                        if random.randint(1, 2) == 1:
                            print("\nWARNING - AN AIRSTRIKE THAT WAS CALLED IN ON YOU STAYS ON YOUR TRAIL - THEY WILL ATTACK IN 2 TURNS")
                            e.follows = False
                            e.turn = 3
                            keep.append(e)
                        else:
                            print("\nWARNING LIFTED - YOU ESCAPED AN AIRSTRIKE")
                events = []
                for e in keep:
                    events.append(e)
                surroundings = regen(surroundings)
            print("\n-----\n")
            return player_tank, surroundings, events, enemies, allies, True, tanks
        else:
            return player_tank, surroundings, events, enemies, allies, False, tanks
    except Exception as ex:
        error(ex, currentframe().f_code.co_name)


def rld(player_tank, surroundings:list, events:list, enemies:int, allies:int, tanks):
    try:
        print(" - RELOADING -")
        d = player_tank.reload()
        if d == True:
            print(f"You hear a click as the next shell gets loaded.\nYou have a total of {player_tank.inventory['shells']} {'shell' if player_tank.inventory['shells'] == 1 else 'shells'} left!")
            for pos in surroundings:
                if surroundings[pos] != None:
                    if surroundings[pos].allegiance != player_tank.allegiance and surroundings[pos].turn == None:
                        if random.randint(1, 6) == 1:
                            surroundings[pos].turn = 2
                            print("An enemy tank has spotted you while you were reloading!")
            print("\n-----\n")
            return player_tank, surroundings, events, enemies, allies, True, tanks
        else:
            print(f"{'You already have a shell loaded' if player_tank.loaded == True else 'You have no shells left'}!")
            print("\n-----\n")
            return player_tank, surroundings, events, enemies, allies, False, tanks
    except Exception as ex:
        error(ex, currentframe().f_code.co_name)


def inv(player_tank, surroundings:list, events:list, enemies:int, allies:int, tanks):
    try:
        print(f" - Inventory & Upgrades -\nInventory:\n{player_tank.inventory['shells']} tank {'shells' if player_tank.inventory['shells'] != 1 else 'shell'} ({'Ready to fire' if player_tank.loaded == True else 'Need to reload'})\n{player_tank.inventory['spyglasses']} {'batteries' if player_tank.inventory['spyglasses'] != 1 else 'battery'}")
        
        if player_tank.inventory['anti-air'] == True:
            print("One anti-air team")
        if player_tank.inventory['pow'] != 0:
            print(f"{player_tank.inventory['pow']} {'prisoner' if player_tank.inventory['pow'] == 1 else 'prisoners'} of war")

        gear_tears = [
            "Standard",
            "Advanced",
            "Superior"
        ]
        print(f"\nUpgrades:\nEngine - {gear_tears[player_tank.upgrades['engine'] - 1]}\nTracks - {gear_tears[player_tank.upgrades['tracks'] - 1]}\nBarrel - {gear_tears[player_tank.upgrades['barrel'] - 1]}")
        print(f"\nWhat do you want to do now?\n1. Craft shells out of scrap\n2. Craft an upgrade out of scrap\n - - -\n3. Return\n")
        action = number_input()

        if action == 1: # Craft shells
            variables.stats['crafts'] += 1
            ammo = random.randint(1, 3)
            player_tank.ammo_change(True, ammo)
            print("\nCrafting...")
            time.sleep(random.randint(2, 5))
            print(f"You successfully craft {ammo} {'shells' if ammo != 1 else 'shell'}!")
            time.sleep(2)
            for pos in surroundings:
                if surroundings[pos] != None:
                    if surroundings[pos].allegiance != player_tank.allegiance and surroundings[pos].turn == None:
                        if random.randint(1, 3) == 3:
                            surroundings[pos].turn = 2
                            print("An enemy tank has spotted you while you were crafting!")
            print("\n-----\n")
            return player_tank, surroundings, events, enemies, allies, True, tanks

        elif action == 2: # Craft upgrade
            variables.stats['crafts'] += 1
            trying = True
            i = 0
            print("\nCrafting...")
            time.sleep(random.randint(2, 5))
            while trying == True:
                part = random.choice(("engine", "tracks", "barrel"))
                i += 1
                if player_tank.upgrades[part] != 3:
                    trying = False
                    player_tank.upgrades[part] += 1

                    print(f"\nYou successfully upgraded your {part} to: {gear_tears[player_tank.upgrades[part] - 1]}!")
                    time.sleep(2)
                if i == 10:
                    trying = False
                    print("\nYou didn't manage to craft any upgrades...")

            for pos in surroundings:
                if surroundings[pos] != None:
                    if surroundings[pos].allegiance != player_tank.allegiance and surroundings[pos].turn == None:
                        if random.randint(1, 3) == 3:
                            surroundings[pos].turn = 2
                            print("An enemy tank has spotted you while you were crafting.")
            print("\n-----\n")
            return player_tank, surroundings, events, enemies, allies, True, tanks

        else: # Return
            print("\n-----\n")
            return player_tank, surroundings, events, enemies, allies, False, tanks
    except Exception as ex:
        error(ex, currentframe().f_code.co_name)





def powstuff(player_tank):
    try:
        gend = random.randint(1, 2)
        fact = None
        av = []
        for k, d in variables.factions.items():
            if k != player_tank.allegiance:
                av.append([k, d])

        fact = random.choice(av)

        print(f"\nThough as you're moving you run into a hostile soldier of the {fact[1]}. {'He' if gend == 1 else 'She'} {random.choice(variables.pow_desc)}")
        time.sleep(2)
        print(f"What do you want to do with {'him' if gend == 1 else 'her'}?\n\n1. Shoot\n2. Take prisoner\n3. Ignore")
        action = number_input()
        if action == 1:
            # Shot POW
            variables.stats['shot_pows'] += 1
            print(f"You take your handgun and shoot {'him' if gend == 1 else 'her'} where {'he' if gend == 1 else 'she'} stands and drive along.\n{'He' if gend == 1 else 'She'} didn't try to fight back...")
        elif action == 2:
            # Took POW
            player_tank.inventory['pow'] += 1
            print(f"You take them as a prisoner and lock tie them up in your tank. They may make things more difficult, but this war has already seen enough deaths.")
        else:
            # Ignored
            print(f"{'He' if gend == 1 else 'She'} stares at you in pure fear as you drive along.")
        return player_tank
    except Exception as ex:
        error(ex, currentframe().f_code.co_name)


def defending(surroundings:dict, player_tank, tanks):
    try:
        allies_s = []
        for pos in surroundings:
            if surroundings[pos] != None:
                if surroundings[pos].allegiance == player_tank.allegiance:
                    allies_s.append(pos)
                surroundings[pos].turn = None
        
        if allies_s != []:
            print("You're about to get hit! Your crew needs your command now!\nIf you manage to escape you could possibly make a run to the allied tank nearby.")
            time.sleep(2)
            deadoralive = skillcheck(random.choice(variables.crew_swap_skillcheck), variables.difficulty, player_tank, detailed=True)
            variables.difficulty -= 0.075

            if deadoralive[0] == 0:
                print(f"You and your crew successfully ditch your tank before it's hit! You run through the crossfire with your crew and manage to find shelter in an allied tank, which they put under your control.")
                player_tank.inventory = surroundings[allies_s[0]].inventory
                player_tank.loaded = True
                player_tank.upgrades = surroundings[allies_s[0]].upgrades

                tanks.remove(surroundings[allies_s[0]])
                surroundings[allies_s[0]] = None
                variables.stats["skillchecks"] += 1
                return False, surroundings, tanks # Changed tank
            else:
                print(f"{f'You were given {floor(deadoralive[2])} milliseconds of time, but you were with {floor(deadoralive[1])} milliseconds too slow' if deadoralive[0] == 1 else 'You gave a wrong command'}.")
                return True, surroundings, tanks # Is dead

        else:
            print(f"You see no way out...")
            return True, surroundings, tanks # Is dead
    except Exception as ex:
        error(ex, currentframe().f_code.co_name)


def skillcheck(string:str, difficulty:float, player_tank = None, engine_part:str = None, detailed:bool = False) -> int or tuple:
    try:
        print(" -- Skillcheck imminent! --\nPress Enter if you're ready")
        input()
        time.sleep(1)
        if player_tank != None:
            difficulty -= 0.125 * player_tank.inventory['pow']
            if difficulty < 0.07:
                difficulty = 0.07
            if engine_part != None:
                difficulty *= sqrt(player_tank.upgrades[engine_part] + 1)
        deadline = ((len(string)/1.2) * difficulty) * 1000 # * 1000 to turn it to milliseconds
        start = time.time() * 1000
        print(f"Shout:\n{string}")
        check = input()
        end = time.time() * 1000
        time.sleep(0.5)

        diff = end - start

        if check.lower() == string.lower():
            if diff <= deadline + 50:
                return 0 if detailed == False else (0, diff, deadline) # Success
            else:
                return 1 if detailed == False else (1, diff, deadline) # Out of time
        else:
            return 2 if detailed == False else (2, diff, deadline) # Incorrect string
    except Exception as ex:
        error(ex, currentframe().f_code.co_name)


def regen(surroundings:dict) -> bool or None:
    try:
        surroundings = {}
        return surroundings
    except Exception as ex:
        error(ex, currentframe().f_code.co_name)


def generate(tanks:list, i:int=1) -> dict and list:
    try:
        surroundings = {}
        while i < 4:
            gen = random.choice(tanks)
            if gen not in surroundings.values():
                surroundings[i] = gen
                i += 1

        return surroundings, tanks
    except Exception as ex:
        error(ex, currentframe().f_code.co_name)


def fill(tanks:list, spot:int, surroundings:dict) -> dict and list:
    try:
        success = False
        while success == False:
            gen = random.choice(tanks)
            if gen not in surroundings.values():
                surroundings[spot] = gen
                success = True
        variables.scouted[spot] = False

        return surroundings, tanks
    except Exception as ex:
        error(ex, currentframe().f_code.co_name)


def game(player_tank, enemies:int, allies:int, surroundings:list, turn:int, events:list, tanks:list):
    try:
        if enemies > 3:
            if surroundings == {}:
                for i in range(1, 4):
                    variables.scouted[i] = False
                surroundings, tanks = generate(tanks)
            
            time.sleep(1)
            print(f"""\n -- Turn {turn} --\n{f'The war is almost won! There are only {enemies} enemies left! ' if enemies < 6 else ''}You're a tank commander of the {variables.factions[player_tank.allegiance]}. There is {'one' if surroundings[1] != None else 'no'} tank to the west, {'one' if surroundings[2] != None else 'no'} tank to the north and {'one' if surroundings[3] != None else 'no'} tank to the east.\nWhat do you do?
            \n\n1. Scout{' - Already done' if False not in variables.scouted.values() else ''}\n2. Attack\n3. Move\n4. Reload\n5. Inventory""")

            action = number_input(maxi=5)

            # Player action
            system("cls")
            actions = {1: scout, 2: atk, 3: move, 4: rld, 5: inv}
            player_tank, surroundings, events, enemies, allies, passing, tanks = actions.get(action)(player_tank, surroundings, events, enemies, allies, tanks)

            # Player is dead
            if player_tank == None:
                return 2, surroundings, enemies, allies, turn, events, tanks

            # If time passes
            if passing == True:
                turn += 1
                # The enemy has their turn
                for pos, unit in surroundings.items():
                    if unit != None:
                        if unit.turn != None:
                            unit.turn -= 1
                            if unit.turn == 0:
                                unit.ammo_change(False, 1)
                                print("Your adrenaline rises further as a tank is about to shoot you...")
                                defense, surroundings, tanks = defending(surroundings, player_tank, tanks)
                                if defense == False:
                                    time.sleep(5)
                                    print("\n-----\n")
                                    surroundings = regen(surroundings)
                                    events = []
                                    allies -= 1
                                    return 0, surroundings, enemies, allies, turn, events, tanks # Game keeps going
                                else:
                                    print("\n-----\n")
                                    if unit.inventory['shells'] != -1:
                                        return 2, surroundings, enemies, allies, turn, events, tanks # Game lost
                                    else:
                                        print("... after a moment of shock you come to your senses... it was all in your mind, you're not dead! The enemy tank must be out of ammo! You can still win this!")
                                        return 0, surroundings, enemies, allies, turn, events, tanks # Game keeps going
                            else:
                                if unit.turn == 1:
                                    directions = ["WESTERN", "NORTHERN", "EASTERN"]
                                    print(f"WARNING - {directions[pos-1]} TANK WILL ENGAGE NEXT ROUND\n")
                                if random.randint(1, 10) < 5: # 40% chance
                                    if random.randint(1, 2) == 1: # Airstrike
                                        events.append(Event(1, 2, True))
                                    else: # Artillery
                                        events.append(Event(2, 2))
                    else:
                        if random.randint(1, 10) < 4:
                            surroundings, tanks = fill(tanks, pos, surroundings)
                            if surroundings[pos].allegiance != player_tank.allegiance:
                                surroundings[pos].turn = 2
                            directions = ["WEST", "NORTH", "EAST"]
                            print(f"SURROUNDINGS - A NEW TANK MOVED UP IN THE {directions[pos-1]} - THEY MAY ATTACK YOU\n")
                            

                # Events get checked
                for e in events:
                    e.turn -= 1
                    if e.turn == 0:
                        if len(events) != 1: # Not one event
                            after = False
                            all_e = [e]
                            for e2 in events:
                                if e2 != e:
                                    if after == True:
                                        if e2.turn - 1 == 0:
                                            all_e.append(e2)
                                else:
                                    after = True
                            
                            if len(all_e) > 2:
                                print(f"Too many aerial attacks are hitting you at once, even if you could flee your tank you'd die.")
                                return 2, surroundings, enemies, allies, turn, events, tanks # Game lost
                            elif len(all_e) == 2:
                                if all_e[0].e_type == 1 and player_tank.inventory['anti-air'] == True:
                                    print("Your anti-air team shoots down the enemy airplane, but needs to retreat for now!")
                                    player_tank.inventory['anti-air'] = False
                                    e = all_e[1]
                                    events.remove(all_e[0])
                                elif all_e[1].e_type == 1 and player_tank.inventory['anti-air'] == True:
                                    print("Your anti-air team shoots down the enemy airplane, but needs to retreat for now!")
                                    player_tank.inventory['anti-air'] = False
                                    e = all_e[0]
                                    events.remove(all_e[1])

                                else:
                                    print(f"Too many aerial attacks are hitting you at once, even if you could flee your tank you'd die.")
                                    return 2, surroundings, enemies, allies, turn, events, tanks # Game lost
                        
                        print("You hear a plane closing in on you..." if e.e_type == 1 else "You hear how mortar shells start to hit your area...")
                        time.sleep(3)
                        if e.e_type == 1 and player_tank.inventory['anti-air'] == True:
                            print("Your anti-air team shoots down the enemy airplane, but needs to retreat for now!")
                            print("\n-----\n")
                            player_tank.inventory['anti-air'] = False
                            events.remove(e)
                        else:
                            defense, surroundings, tanks = defending(surroundings, player_tank, tanks)
                            if defense == False:
                                time.sleep(5)
                                print("\n-----\n")
                                surroundings = {}
                                events = []
                                allies -= 1
                                return 0, surroundings, enemies, allies, turn, events, tanks # Game keeps going
                            else:
                                print("\n-----\n")
                                return 2, surroundings, enemies, allies, turn, events, tanks # Game lost
                    elif e.turn == 1:
                        if e.e_type == 1:
                            print(f"WARNING - AIRSTRIKE INBOUD - {'YOU HAVE ONE TURN LEFT TO SAVE YOURSELF' if player_tank.inventory['anti-air'] == False else 'YOUR ANTI-AIR TEAM WILL KEEP YOU SAFE IF YOU DO NOT MOVE'}\n")
                        elif e.e_type == 2:
                            print("WARNING - ARTILLERY INBOUND - YOU HAVE ONE TURN LEFT TO SAVE YOURSELF\n")
                


                atkd = {1: 0, 2: 0, 3: 0}
                it = False
                for elem in tanks:
                    if elem.inventory['shells'] != 0:
                        target = random.choice(tanks)
                        if target.allegiance != elem.allegiance and target not in surroundings.values():
                            if elem.allegiance == player_tank.allegiance:
                                if random.randint(1, 20) < 4:
                                    elem.inventory['shells'] -= 1
                                    atkd[target.allegiance] += 1
                                    tanks.remove(target)
                                    if target.allegiance == player_tank.allegiance:
                                        allies -= 1
                                    else:
                                        enemies -= 1
                                    it = True
                            else:
                                if random.randint(1, 20) < 3:
                                    elem.inventory['shells'] -= 1
                                    atkd[target.allegiance] += 1
                                    tanks.remove(target)
                                    if target.allegiance == player_tank.allegiance:
                                        allies -= 1
                                    else:
                                        enemies -= 1
                                    it = True
                    else:
                        if random.randint(1, 2) == 1:
                            elem.inventory['shells'] = random.randint(1, 2)
                if it == True:
                    battle_list = ""
                    if atkd[1] != 0:
                        battle_list += f"    •    {atkd[1]} {'tanks' if atkd[1] != 1 else 'tank'} of the {variables.factions[1]}\n"
                    if atkd[2] != 0:
                        battle_list += f"    •    {atkd[2]} {'tanks' if atkd[2] != 1 else 'tank'} of the {variables.factions[2]}\n"
                    if atkd[3] != 0:
                        battle_list += f"    •    {atkd[3]} {'tanks' if atkd[3] != 3 else 'tank'} of the {variables.factions[3]}\n"
                    print(f"BATTLEFIELD - Losses this turn:\n{battle_list}")


            # Random things after each everything
            if random.randint(1, 10) == 1:
                print(f"\nIn a moment of silence {random.choice(variables.silence)}")


            return 0, surroundings, enemies, allies, turn, events, tanks # Game keeps going

        else:
            return 1, surroundings, enemies, allies, turn, events, tanks # Game won
    except Exception as ex:
        error(ex, currentframe().f_code.co_name)