scouted = {
    1: False,
    2: False,
    3: False
}

difficulty = None

factions = {
    1: "",
    2: "",
    3: ""
}

all_factions = [
    "Peacekeepers",
    "Empire",
    "Outlaws",
    "Rebels",
    "Deviants",
    "Dalek",
    "Crusaders",
    "Elves",
    "Orcs",
    "Flood"
]


## Stats
stats = {
    "killed_allies": 0,
    "killed_enemies": 0,
    "rounds_shot": 0,
    "scouted": 0,
    "moves": 0,
    "skillchecks": 0,
    "crafts": 0,
    "shot_pows": 0
}


## Voice Lines ##
shot_ally_lines = [
    "What are you doing, rookie?! Those were some of our finest men!",
    "Did you just shoot one of ours!?! Did you learn nothing at boot camp??",
    "No, you idiot!! That one was on our side, they could've helped you!",
    "Ah, well done. You're successfully digging your own grave.",
    "How are you even a commander?",
    "Are you even on our side?",
    "I can't believe we're losing men to this guy...",
    "It's not that hard rookie, shoot at the bad guys, not at us!"
]

shot_enemy_lines = [
    "Good job commander! Now go shoot more of them.",
    "Oh well done, you did it, you want a gold star or something?",
    "Good, keep your head up though, there might be more around.",
    "Blood for the blood god!",
    "Wiped out! There might be hope for you yet, commander.",
    "Yes! That's the way to do it!",
    "Don't pat yourself on the back just yet, the battle isn't over 'till I say it is!"
]

shot_empty_lines = [
    "What're you doing, rookie!?! You're wasting ammo!",
    "Are you proud of yourself rookie? You killed a ghost or something?",
    "Is this some kind of stupid diversion?",
    "You missed the guys by a mile!",
    "There was nothing there rookie! Stop messing around!",
    "You saw a spider or something, rookie? Because it sure isn't what we're aiming for."
]

ally_interaction_lines = [
    "I'm glad you're here! I'm sure you can put these shells to better use than we can...",
    "Phew, you came just in time! Please put these shells to good use!",
    "Take this, it's dangerous to go alone out there!",
    "I've seen you fight, you can put these to a better use out of these than we can...",
    "These are on the house!"
]

# "The commander of the allied tank to your north "
northern_ally_lines = [
    "gives you a thumbs up with a wide smile.",
    "throws their hands up in celebration of seeing you.",
    "is drinking a sip of wine as they give you a wink.",
    "makes funny faces at you.",
    "seems to be on their Tamagotchi",
    "yawns in boredom before seeing you.",
    "is picking their nose, thinking you wouldn't see them.",
    "is juggling grenades."
]

# "In a moment of silence "
silence = [
    "your engineer cracks open a cold one.",
    "your gunner rubs his eyes. The smoke seems to not treat them too well.",
    "you feel your eyes getting heavy, before hearing gunshots in the distance again.",
    "you feel the need to go home building up.",
    "you notice the engineer fiddling with some cables."
]

# "The commander of the [dir] tank "
kill_cheer_ally_lines = [
    "lights a cigarette in celebration of your kill.",
    "shouts “FUCK YEAH!” so loud, you don't need a radio to hear it.",
    "cackles with laughter loudly. He seems to be celebrating your kill? Is he okay?",
    "raises their fist in celebration.",
    "gives you a thumbs-up before going back into the tank.",
    "salutes you."
]


## Endings ##
winning_lines = [
    "The battlefield is quiet for a moment, before cheers from your own crew and on the radio erupt in joy. Your officer radios in to congratulate you for what you've done today. The few enemies that are left are retreating. The day is won.",
    "As the smoke settles from the last explosion, you see the last few enemies retreat into the distance. Your fellow soldiers start to celebrate your latest victory. You head back to base to regroup and rejoice in your winning.",
    "You've finished the war for your people. You have risen above the fallen and claimed victory. Your name shall be remembered throughout history."
]

loosing_lines = [
    "You're frantically trying to move away or counter in some way to save yourself, but it is in vain as the last shot hits you head-on, causing the tank to explode with you and your fellow soldiers in it.",
    "As the explosion echoes around you and everything fades to black, you can't help but think if your sacrifice was really worth it."
    "All your academic training... wasted because of some mistakes in the heat of action."
]


## Skillchecks ##
crew_swap_skillcheck = [
    "GET THE FUCK OUT!",
    "QUICKLY, RUN!",
    "WHAT'RE YOU WAITING FOR?",
    "RUN!",
    "DON'T JUST SIT AROUND!",
    "TIME TO ABANDON SHIP!",
    "THIS IS NO PLACE TO DIE!",
    "FLY, YOU FOOLS!"
]

confront_skillcheck = [
    "FIRE! NOW!",
    "GET THEM!",
    "SHOOT THEM OR SOMETHING!",
    "TAKE THEM OUT!",
    "FOR NARNIA!",
    "FOR FRODO!",
    "HARD IRON IN FRONT!",
    "DON'T HESITATE!",
    "MAKE THEM EAT LEAD!"
]

difficulty_set = [
    "INTO WAR!",
    "I'M HERE TO MAKE MY DOG PROUD!",
    "FOR GLORY!",
    "TIME TO DO THIS!"
]

broken_part = [
    "GET THAT SHIT FIXED!",
    "THIS IS YOUR TIME TO DIY!",
    "FIX IT DAMNIT!",
    "MAKE YOURSELF USEFUL!"
]


## Others ##
tips = [
    "Upgrades of your tank make skillchecks easier.",
    "Allied tanks hold all kinds of helpful things that they may share with you, so long as you just roll up to them in a friendly manner.",
    "Getting P.O.W.'s in your tank drastically increases the difficulty, but also gives you a much better score in the end.",
    "The higher the difficulty, the less time you have for skillchecks.",
    "Only the tank to your north may spot you while scouting.",
    "If you manage to escape death the difficulty will increase.",
    "The choice of faction makes no gameplay difference.",
    "It's okay to not *actually* shout during a skillcheck... you don't even need to write it in caps!",
    "The length of a skillcheck isn't making it more difficult, as you're given a certain amount of time per character, so don't worry!",
    "Scouting is helpful but also exposes you and can quickly get you killed if you're not careful.",
    "Our spyglasses are quite crappy, which is why they need a whole battery for a single scouting.",
    "Crafting something in your inventory lowers your score slightly, as it also serves as a secret difficulty tracker.",
    "An allied tank in your surroundings may react to when you kill someone, revealing themselves to you.",
    "Not all actions cost turns. You can safely \"Return\", check your inventory or attempt a reload while already having a shell loaded.",
    "While most actions give you points, shooting P.O.W's or allied tanks and crafting items lowers your score."
]

introduction = [
    "You've been stuck in war for ages, and have now decided to make a change, and become a tank commander!",
    "You never minded the smell of smoke and constantly being on the brink of death. You enlisted yourself and a few weeks later you were approved as a tank commander!"
]

# "He/She "
pow_desc = [
    "looks like they don't quite seem to know how to handle this situation.",
    "looks in shock as they break down on their knees.",
    "looks as if they were running from a slaver.",
    "throws their weapon to the ground and gives up.",
    "doesn't even seem to have a gun. They're just cannon-fodder."
]



# For testing if there are any errors
if __name__ == "__main__":
    print(locals())