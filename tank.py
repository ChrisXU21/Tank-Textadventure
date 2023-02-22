import random, time
import variables
from tank_game import game, skillcheck
from wrapper import error, number_input, make_score
from os import system
from inspect import currentframe


# CLASS STUFF
class Tank:
    def __init__(self, allegiance=0):
        self.allegiance = random.randint(1, 3) if allegiance == 0 else allegiance
        self.loaded = True
        self.turn = None

        self.upgrades = {
            "engine": random.randint(1, 3) if allegiance == 0 else 1,
            "tracks": random.randint(1, 3) if allegiance == 0 else 1,
            "barrel": random.randint(1, 3) if allegiance == 0 else 1
        }
        self.inventory = {
            "shells": 3,
            "spyglasses": 2,
            "anti-air": random.choice((True, False)) if allegiance == 0 else False,
            "pow": 0
        }

    def reload(self):
        if self.loaded == False and self.inventory['shells'] > 0:
            self.loaded = True
            return True
        else:
            return False

    def ammo_change(self, action, value):
        '''action=True(+)|False(-)'''
        if action == True:
            self.inventory['shells'] += value
        elif action == False:
            self.inventory['shells'] -= value


# GAME
if __name__ == "__main__":
    try:
        # SETUP
        RUNNING = True
        highscore = [False]
        highscore_l = [False]

        # GAME LOOP
        while RUNNING:
            # Start
            highscore[0] = False
            highscore_l[0] = False
            system("cls")
            print(f"Welcome to the Tank game!\n{random.choice(variables.introduction)}\n\nPlease put in your name!")
            user_n = ""
            while len(user_n) < 3:
                user_n = input()
                if len(user_n) < 3 and len(user_n) > 32:
                    print("Your username needs to be at least 3 characters long, to a maximum of 32 characters!")
            time.sleep(0.5)
            system("cls")

            # Generate factions and let player choose faction
            i = 1
            while i < 4:
                gen = random.choice(variables.all_factions)
                if gen not in variables.factions.values():
                    variables.factions[i] = gen
                    i += 1

            print(f"Choose which faction you want to play as!\n(Choose with numbers)\n\n1. {variables.factions[1]}\n2. {variables.factions[2]}\n3. {variables.factions[3]}")
            player = number_input()
            player_tank = Tank(player)
            time.sleep(0.5)
            system("cls")


            # Declare how many enemies are wanted
            print(f"Choose how many tanks you want there to be on the battlefield!")
            tank_amount = number_input(mini=10, maxi=200)

            enemies = 0
            while enemies < 5:
                # Generating enemies
                tanks = []
                for i in range(1, tank_amount+1):
                    tanks.append(Tank())

                # Count enemies and allies - Also send start message
                enemies = 0
                allies = 0
                for elem in tanks:
                    if elem.allegiance == player_tank.allegiance:
                        allies += 1
                    else:
                        enemies += 1
            
            time.sleep(0.5)
            system("cls")

            # Set difficulty
            print("You're ready for war! Repeat the upcoming phrase!")
            stringthing = random.choice(variables.difficulty_set)
            while variables.difficulty == None:
                check = skillcheck(stringthing, 0.5, detailed=True)
                if check[0] != 2:
                    variables.difficulty = (check[1] / 1000) / (len(stringthing) * 1.5) + 0.3
                else:
                    print("You can do better! Try again!")


            # Clear screen
            time.sleep(0.5)
            system("cls")

            if enemies > 4:
                print(f"--START--\nYou're {user_n}, the commander of a tank, defending your brothers of the {variables.factions[player_tank.allegiance]}!\nThe lives of your crew are in your hands, so choose wisely!\nThere are {enemies} enemies on the battlefield and {allies} allies.\n\nThere are 3 directions you can interact with. Those being west, north and east.")

                #Start active game loop
                active_game = 0
                surroundings = {}
                turn = 1
                events = []
                while active_game == 0:
                    active_game, surroundings, enemies, allies, turn, events, tanks = game(player_tank, enemies, allies, surroundings, turn, events, tanks)

                time.sleep(0.5)
                # Game won
                if active_game == 1:
                    print(f" - YOU WIN! -\n{random.choice(variables.winning_lines)}\n")
                # Game lost
                elif active_game == 2 and player_tank != None:
                    print(f" - YOU LOSE -\n{random.choice(variables.loosing_lines)}\n")
                    player_tank.inventory['pow'] = 0
                elif active_game == 4:
                    print("THE GAME HAS RUN INTO A SEVERE ISSUE AND CRASHED")
                    input()
                    exit()

                
                # Create score impact table for easy score adjustment
                # Calculate score
                score = make_score(variables.difficulty, variables.stats, player_tank)
                # Create main stats
                gen_t = f""" -- STATS --\n
Killed {variables.stats['killed_allies']} {'allies' if variables.stats['killed_allies'] != 1 else 'ally'}
Killed {variables.stats['killed_enemies']} {'enemies' if variables.stats['killed_enemies'] != 1 else 'enemy'}
Fired {variables.stats['rounds_shot']} {'shells' if variables.stats['rounds_shot'] != 1 else 'shell'}
Scouted {variables.stats['scouted']} {'times' if variables.stats['scouted'] != 1 else 'time'}
Crafted {variables.stats['crafts']} {'times' if variables.stats['crafts'] != 1 else 'time'}
Advanced {variables.stats['moves']} {'times' if variables.stats['moves'] != 1 else 'time'}
Almost died {variables.stats['skillchecks']} {'times' if variables.stats['skillchecks'] != 1 else 'time'}"""
                # Add pow's to stats if there is any
                if player_tank.inventory['pow'] != 0:
                    pow_t = f"\nYou rescued {player_tank.inventory['pow']} {'POWs' if player_tank.inventory['pow'] != 1 else 'POW'} from the battlefield!"
                else:
                    pow_t = ""

                # Highscore stuff
                if len(highscore) == 1:
                    highscore.append(score)
                    highscore[0], champ_name, champ_tanks, champ_turns = True, user_n, tank_amount, turn
                elif highscore[1] < score:
                    highscore[0], highscore[1], champ_name, champ_tanks, champ_turns = True, score, user_n, tank_amount, turn
                print(f"{gen_t}{pow_t}\n\nScore: {score}\Highscore: {'*NEW* ' if highscore[0] == True else ''}{highscore[1]} - {champ_name} with {champ_tanks} tanks on the battlefield and {champ_turns} {'turns' if champ_turns != 1 else 'turn'}\n\nTip: {random.choice(variables.tips)}")

            else:
                print("Well... looks like no enemies made it to the battlefied... go join another war! Dream bigger!")


            print("Do you want to restart?\nY / N")
            restart = None
            while restart == None:
                restart = input()
                if restart.lower() != "y" and restart.lower() != "n":
                    print("Please type either Y or N!")
                    restart = None
                else:
                    if restart.lower() == "n":
                        print(f"Goodbye, commander {user_n}!")
                        RUNNING = False
                    else:
                        system("cls")
                        variables.scouted = {1: False, 2: False, 3: False}
                        variables.difficulty = None
                        variables.stats = {"killed_allies": 0, "killed_enemies": 0, "rounds_shot": 0, "scouted": 0, "moves": 0, "skillchecks": 0, "crafts": 0, "shot_pows": 0}

    except Exception as ex:
        error(ex, currentframe().f_code.co_name)
