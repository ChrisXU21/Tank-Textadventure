def isNumber(n) -> int:
    try:
        return int(n)
    except:
        return 0

def error(msg, pos):
    print(f"ERROR\n\n{msg}\n{pos}\n\nPlease report the above error and describe what happened!\nPress enter to close the game...")
    input()
    exit()

def make_score(difficulty:float, stats:dict, player_tank) -> int:
    score_impact = {
        'moves': 10, #+
        'rounds_shot': 5, #+
        'scouted': 20, #+
        'killed_enemies': 50, #+
        'skillchecks': 80, #+
        'pow': 150, #+

        'crafts': 30, #-
        'shot_pows': 50, #-
        'killed_allies': 100 #-
    }
    difficulty_score = calc_score_diff(difficulty)
    pos_score = (stats['moves'] * score_impact['moves']) + (stats['scouted'] + score_impact['scouted']) + (stats['killed_enemies'] * score_impact['killed_enemies']) + (stats['skillchecks'] * score_impact['skillchecks']) + (player_tank.inventory['pow'] * score_impact['pow']) + (stats['rounds_shot'] * score_impact['rounds_shot']) + difficulty_score
    neg_score = (stats['crafts'] * score_impact['crafts']) + (stats['shot_pows'] * score_impact['shot_pows']) + (stats['killed_allies'] * score_impact['killed_allies'])
    score = pos_score - neg_score
    return score

def number_input(mini:int=1, maxi:int=3) -> int:
    action = 0
    while action < mini or action > maxi:
        action = isNumber(input())
        if action < mini or action > maxi:
            print(f"Please take a valid number! ({mini}-{maxi})")
    return action

def calc_score_diff(difficulty:float) -> int:
    if difficulty > 2:
        score = 0
    elif difficulty > 1:
        score = 30
    elif difficulty > 0.7:
        score = 50
    elif difficulty > 0.5:
        score = 90
    elif difficulty > 0.3:
        score = 130
    elif difficulty > 0:
        score = 200
    else:
        score = 0
    return score
