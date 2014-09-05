import cmd
import random

#globals
#costs in dollars
RENT = 250
GROCERIES = 50
#allowable time between events.
MEAL_INTERVAL = 6 #hours
SLEEP_INTERVAL = 16 #hours
EXERCISE_INTERVAL = 2 #days
SOCIAL_INTERVAL = 2 #days
CLEANING_INTERVAL = 2 #days
#Risks of death while out of control
SPEEDING_RISK = 0.2
ALCOHOL_POISONING_CHANCE = 0.2
#list of people you can call
CALL_DICT = {"parents": ("mom", "mother", "dad", "father", "parents"),\
        "friend": ("friend", "friends"),\
        "hospital": ("hospital", "police", "ambulance", "911"),\
        "doctor": ("doctor", "psychiatrist"),\
        "helpline": ("helpline", "suicide helpline", "hotline", "suicide hotline"),\
        "psychologist": ("therapist", "councellor", "psychologist")}
#side effects for medicated stages
LOW_ENERGY = {"MESSAGE": "You feel sluggish for some reason",\
        "PENALTY": 30}
LOW_CONCENTRATION = {"MESSAGE": "You're having a lot of trouble focusing right now",\
        "KEYS": ("WORK_FAILURE", "LEISURE_FAILURE"),\
        "PENALTY": 0.2}
POOR_APPETITE = {"MESSAGE": "You haven't seemed to have much of an appetite lately",\
        "KEYS": ("HUNGER_DELAY"),\
        "PENALTY": 2}
SHAKY_HANDS = {"MESSAGE": "Your hands have been shaking uncontrollably lately"}
POOR_MEMORY = {"MESSAGE": "You can't seem to remember the simplest things lately"}
NAUSEA = {"MESSAGE": "You keep feeling queasy lately",\
        "KEYS": ("EAT_FAILURE"),\
        "PENALTY": 0.2}
SIDE_EFFECTS = (LOW_ENERGY, LOW_CONCENTRATION, POOR_APPETITE, SHAKY_HANDS, POOR_MEMORY, NAUSEA)
SIDE_EFFECT = random.choice(SIDE_EFFECTS)
SIDE_EFFECT_FREQ = 2/24
#messages
NORMAL_THOUGHTS = ("You daydream about saving a baby from a fire",\
        "You imagine what you would do if you were fabulously wealthy",\
        "You fondly remember an old friend")
SUICIDAL_IDEATION_MINOR = ("You wonder how many advil you would have to take before you died",\
        "You wonder if your pen knife is sharp enough to cut your throat",\
        "You suddenly imagine shooting yourself")
SUICIDAL_IDEATION_MAJOR = ("You look up the LD50 of advil and figure out how much you'd need to kill yourself",\
        "You make a plan to kill yourself by cutting your throat in a running shower so there'd be no mess",\
        "You compose an email to the coroner so that no one you know would have to find your body")
SUICIDAL_IDEATION_EXTREME = ("You hold a pillow over your head until you pass out to see what suffocating is like",\
        "You summon the strength to buy a lethal dose of advil",\
        "You pack your things so they will be easier to take care of when you're gone")
MANIC_THOUGHTS = ("You plan a cross-country rail trip",\
        "You decide to landscape your back yard",\
        "You decide to learn to play an instrument")
HOSPITAL_THOUGHTS = ("You feel bored but safe",\
        "Everyone else in here seems crazy",\
        "You wonder why you don't miss home")
#disease stages
#Must have LENGTH, CAP, THOUGHTS, & THOUGHT_FREQ
MEDICATED_DEPRESSION = {}
MEDICATED = {"INTRO_MESSAGE": "You can feel things again",\
        "LENGTH": 21,\
        "NEXT_STAGE": MEDICATED_DEPRESSION,\
        "CAP": 100,\
        "THOUGHTS": NORMAL_THOUGHTS,\
        "THOUGHT_FREQ": 1/24,\
        "DOCTOR_MESSAGE": "Everything seems okay.  Some side effects are to be expected",\
        "EFFECT": SIDE_EFFECT}
MEDICATED_DEPRESSION = {"INTRO_MESSAGE": "You feel rough",\
        "LENGTH": 7,\
        "NEXT_STAGE": MEDICATED,\
        "CAP": 50,\
        "HUNGER_DELAY": 4,\
        "THOUGHTS": SUICIDAL_IDEATION_MINOR,\
        "THOUGHT_FREQ": 4/24,\
        "SOCIALIZE_FAILURE": 0.5,\
        "EAT_FAILURE": 0.2,\
        "WORK_FAILURE": 0.5,\
        "LEISURE_FAILURE": 0.2,\
        "WAKEUP_DELAY": 2,\
        "DOCTOR_MESSAGE": "Your symptoms haven't been going on long enough.  Come back in a week",\
        "PSYCHOLOGIST_MESSAGE": "The psychologist says to make sure you are eating, sleeping, and exercising",\
        "EFFECT": SIDE_EFFECT}
MANIA = {"INTRO_MESSAGE": "You feel good",\
        "LENGTH": 7,\
        "NEXT_STAGE": MEDICATED_DEPRESSION,\
        "CAP": 200,\
        "HUNGER_DELAY": 12,\
        "THOUGHTS": MANIC_THOUGHTS,\
        "THOUGHT_FREQ": 12/24,\
        "EAT_FAILURE": 0.5,\
        "WAGE_MULTIPLIER": 2,\
        "FOCUS_CHANCE": 0.5,\
        "LOSS_OF_CONTROL_CHANCE": 0.1,\
        "ACTIVITIES": ("SHOPPING", "DRIVING", "ART", "MUSIC"),\
        "SOCIALIZING_EFFECTS": ("DRUNK", "INAPPROPRIATE", "PROMISCUOUS"),\
        "SOCIALIZING_MULTIPLIER": 2,\
        "SLEEP_CAP": 4,\
        "SLEEP_ENERGY": 200,\
        "SOCIALIZING_CAP": 12,\
        "GAMING_CAP": 16,\
        "HOSPTIAL_MESSAGE": "The hosptial changes your medication plan to stabilize your mania",\
        "HOSPTIAL_STAGE": MEDICATED_DEPRESSION,\
        "DOCTOR_MESSAGE": "The doctor changes your medication plan to stabilize your mania",\
        "DOCTOR_STAGE": MEDICATED_DEPRESSION,\
        "PSYCHOLOGIST_MESSAGE": "The psychologist thinks you are manic and should see a doctor"}
INITIAL_MEDICATION = {"INTRO_MESSAGE": "You can feel things again",\
        "LENGTH": 3,\
        "NEXT_STAGE": MANIA,\
        "CAP": 80,\
        "HUNGER_DELAY": 2,\
        "THOUGHTS": NORMAL_THOUGHTS,\
        "THOUGHT_FREQ": 2/24,\
        "SOCIALIZE_FAILURE": 0.1,\
        "WORK_FAILURE": 0.2,\
        "LEISURE_FAILURE": 0.1,\
        "WAKEUP_DELAY": 1,\
        "DOCTOR_MESSAGE": "Give the medication some time to work",\
        "EFFECT": SIDE_EFFECT}
HOSPITALIZED = {"INTRO_MESSAGE": "You are now in the psych ward.  You feel safe.  You have your laptop",\
        "EXIT_MESSAGE": "You are discharged.  You don't feel ready",\
        "LENGTH": 2,\
        "TIME_WARP": 1,\
        "NEXT_STAGE": INITIAL_MEDICATION,\
        "CAP": 60,\
        "HUNGER_DELAY": 2,\
        "THOUGHTS": HOSPITAL_THOUGHTS,\
        "THOUGHT_FREQ": 4/24,\
        "MEAL_TIMES": (7, 12, 18),\
        "FREE_MEALS": True,\
        "HOSPITAL_ACTIVITIES": True,\
        "HOSPITAL_MESSAGE": "You are already in the hosptial",\
        "DOCTOR_MESSAGE": "The doctor will see you when you are discharged"} 
DEPRESSION3 = {"INTRO_MESSAGE": "You feel worse than you ever have before",\
        "LENGTH": 2,\
        "CAP": 30,\
        "HUNGER_DELAY": 24,\
        "THOUGHTS": SUICIDAL_IDEATION_EXTREME,\
        "THOUGHT_FREQ": 1,\
        "SOCIALIZE_FAILURE": 1,\
        "EAT_FAILURE": 0.5,\
        "WORK_FAILURE": 1,\
        "LEISURE_FAILURE": 1,\
        "WAKEUP_DELAY": 4,\
        "HOSPTIAL_MESSAGE": "You are admitted to the hosptial",\
        "HOSPTIAL_STAGE": HOSPITALIZED,\
        "DOCTOR_MESSAGE": "The doctor gets you admitted to the hosptial",\
        "DOCTOR_STAGE": HOSPITALIZED,\
        "PSYCHOLOGIST_MESSAGE": "The psychologist gets you admitted to the hospital",\
        "PSYCHOLOGIST_STAGE": HOSPITALIZED}
DEPRESSION2 = {"INTRO_MESSAGE": "You feel rough",\
        "LENGTH": 7,\
        "TIME_WARP": 6,\
        "NEXT_STAGE": DEPRESSION3,\
        "CAP": 40,\
        "HUNGER_DELAY": 8,\
        "THOUGHTS": SUICIDAL_IDEATION_MAJOR,\
        "THOUGHT_FREQ": 12/24,\
        "SOCIALIZE_FAILURE": 0.8,\
        "EAT_FAILURE": 0.1,\
        "WORK_FAILURE": 0.5,\
        "LEISURE_FAILURE": 0.3,\
        "WAKEUP_DELAY": 2,\
        "DOCTOR_MESSAGE": "The doctor puts you on medication for your depression",\
        "DOCTOR_STAGE": INITIAL_MEDICATION,\
        "PSYCHOLOGIST_MESSAGE": "The psychologist recommends you call a doctor and make sure you are staying healthy"}
DEPRESSION1 = {"INTRO_MESSAGE": "You feel a little off",\
        "LENGTH": 7,\
        "NEXT_STAGE": DEPRESSION2,\
        "CAP": 80,\
        "HUNGER_DELAY": 2,\
        "THOUGHTS": SUICIDAL_IDEATION_MINOR,\
        "THOUGHT_FREQ": 1/24,\
        "SOCIALIZE_FAILURE": 0.2,\
        "EAT_FAILURE": 0,\
        "WORK_FAILURE": 0.1,\
        "LEISURE_FAILURE": 0.1,\
        "WAKEUP_DELAY": 1,\
        "DOCTOR_MESSAGE": "Your symptoms haven't been going on for long enough.  Come back in a week",\
        "PSYCHOLOGIST_MESSAGE": "Make sure you are eating, sleeping, exercising, and staying social"}
NORMAL = {"LENGTH": 3,\
        "NEXT_STAGE": DEPRESSION1,\
        "CAP": 100,\
        "THOUGHTS": NORMAL_THOUGHTS,\
        "THOUGHT_FREQ": 1/24}

STAGES = (NORMAL, DEPRESSION1, DEPRESSION2, DEPRESSION3, HOSPITALIZED, INITIAL_MEDICATION, MANIA, MEDICATED, MEDICATED_DEPRESSION)
for stage in STAGES:
    if "EFFECT" in stage and "KEYS" in stage["EFFECT"]:
        for key in stage["EFFECT"]["KEYS"]:
            if key in stage:
                stage[key] += stage["EFFECT"]["PENALTY"]
            else:
                stage[key] = stage["EFFECT"]["PENALTY"]

class Character:
    def __init__(self):
        self.base_mood = 80
        self.base_energy = 80
        #In whole numbers of dollars
        self.money = 200
        #in hours
        self.last_meal = 14
        #in hours
        self.last_sleep = 0
        #in days
        self.last_exercise = 1
        #in days
        self.last_social = 1
        #in days
        self.last_cleaned = 1
        #number of meals
        self.groceries = 21
        self.hours_played = 8
        self.hours_gamed = 0
        self.hours_socialized = 0
        self.hours_read = 0
        self.hours_watched = 0
        self.called_parents = False
        self.called_friend = False
        self.disease_stage = NORMAL
        self.disease_days = 0
        self.dead = False

    def change_mood(self, diff):
        self.base_mood += diff
        if self.base_mood < 0:
            self.base_mood = 0
        elif self.base_mood > self.disease_stage["CAP"]:
            self.base_mood = self.disease_stage["CAP"]

    def change_energy(self, diff):
        self.base_energy += diff
        if self.base_energy < 0:
            self.base_energy = 0
        elif self.base_energy > self.disease_stage["CAP"]:
            self.base_energy = self.disease_stage["CAP"]

    def change_stage(self, stage):
        messages = []
        if "TIME_WARP" in self.disease_stage and stage == self.disease_stage["NEXT_STAGE"]:
            month_str = " months pass "
            if self.disease_stage["TIME_WARP"] == 1:
                month_str = " month passes "
            messages.append(str(self.disease_stage["TIME_WARP"]) + month_str + "this way")
            self.last_exercise = 7
            self.last_social = 7
            self.last_cleaned = 7
            self.hours_gamed = 0
            self.hours_socialized = 0
            self.hours_read = 0
            self.hours_watched = 0
            self.called_parents = False
            self.called_friend = False
            self.hours_played += (24 * 30 * self.disease_stage["TIME_WARP"])
        if "EXIT_MESSAGE" in self.disease_stage:
            messages.append(self.disease_stage["EXIT_MESSAGE"])
        self.disease_stage = stage
        self.change_energy(0)
        self.change_mood(0)
        self.disease_days = 0
        messages.append(self.disease_stage["INTRO_MESSAGE"])
        return messages

    def add_hours(self, hours):
        messages = []
        #if we crossed a day boundary
        if (self.hours_played // 24) < ((self.hours_played + hours) // 24):
            self.hours_gamed = 0
            self.hours_socialized = 0
            self.hours_read = 0
            self.hours_watched = 0
            self.called_parents = False
            self.called_friend = False
            self.last_exercise += 1
            self.last_social += 1
            self.last_cleaned += 1
            self.disease_days += 1
            if self.disease_days >= self.disease_stage["LENGTH"]:
                if "NEXT_STAGE" not in self.disease_stage:
                    self.dead = True
                    messages.append("You have committed suicide")
                    return messages
                messages.extend(self.change_stage(self.disease_stage["NEXT_STAGE"]))
            if ((self.hours_played + hours) // 24) % 7 == 0:
                self.money -= RENT
                messages.append("Rent and bills deducted.  You now have $" + str(self.money))
        self.last_meal += hours
        self.last_sleep += hours
        self.hours_played += hours
        if "EFFECT" in self.disease_stage and random.random() < SIDE_EFFECT_FREQ:
            messages.append(self.disease_stage["EFFECT"]["MESSAGE"])
        if random.random() < self.disease_stage["THOUGHT_FREQ"] * hours:
            messages.append(random.choice(self.disease_stage["THOUGHTS"]))
        if self.last_meal > 24 * 7:
            messages.append("You have starved to death")
            self.dead = True
        return messages

    def get_mood(self):
        mood = self.base_mood
        if self.last_meal > MEAL_INTERVAL:
            mood -= min(10 * (self.last_meal - MEAL_INTERVAL), 30)
        if self.last_exercise > EXERCISE_INTERVAL:
            mood -= min(5 * (self.last_exercise - EXERCISE_INTERVAL), 20)
        if self.last_social > SOCIAL_INTERVAL:
            mood -= min(5 * (self.last_social - SOCIAL_INTERVAL), 20)
        if self.last_cleaned > CLEANING_INTERVAL:
            mood -= 5
        if mood < 0:
            mood = 0
        elif mood > self.disease_stage["CAP"]:
            mood = self.disease_stage["CAP"]
        return mood

    def get_energy(self):
        energy = self.base_energy
        if self.last_meal > MEAL_INTERVAL:
            energy -= min(10 * (self.last_meal - MEAL_INTERVAL), 30)
        if self.last_sleep > SLEEP_INTERVAL:
            energy -= min(5 * (self.last_sleep - SLEEP_INTERVAL), 20)
        if self.last_exercise > EXERCISE_INTERVAL:
            energy -= min(5 * (self.last_exercise - EXERCISE_INTERVAL), 20)
        if "EFFECT" in self.disease_stage and self.disease_stage["EFFECT"] == LOW_ENERGY:
            energy -= self.disease_stage["EFFECT"]["PENALTY"]
        if energy < 0:
            energy = 0
        elif energy > self.disease_stage["CAP"]:
            energy = self.disease_stage["CAP"]
        return energy

    def clean(self):
        messages = self.add_hours(1)
        self.last_cleaned = 0
        return messages

    def work(self, hours):
        messages = self.add_hours(hours)
        wages = 10 * hours
        if "WAGE_MULTIPLIER" in self.disease_stage:
            wages *= self.disease_stage["WAGE_MULTIPLIER"]
        self.money += wages
        self.change_energy(-5 * hours)
        self.change_mood(-5 * hours)
        return messages

    def sleep(self, hours):
        messages = self.add_hours(hours)
        if hours < 4:
            return messages
        if hours > 8:
            hours = 8
        self.last_sleep = 0
        if "SLEEP_ENERGY" in self.disease_stage:
            self.base_energy = min(self.disease_stage["SLEEP_ENERGY"], self.disease_stage["CAP"])
            return messages
        self.base_energy = min((10 * hours), self.disease_stage["CAP"])
        if hours > 6:
            self.change_energy(20)
        return messages

    def eat(self):
        messages = self.add_hours(1)
        self.last_meal = 0
        if "FREE_MEALS" not in self.disease_stage:
            self.groceries -= 1
        return messages

    def exercise(self):
        messages = self.add_hours(1)
        self.last_exercise = 0
        self.change_mood(5)
        self.change_energy(-5)
        return messages

    def shopping(self):
        messages = self.add_hours(1)
        self.money -= GROCERIES
        self.groceries += 21
        if self.groceries > 42:
            self.groceries = 42
        return messages

    def game(self, hours):
        messages = self.add_hours(hours)
        daily_cap = 4
        if "GAMING_CAP" in self.disease_stage:
            daily_cap = self.disease_stage["GAMING_CAP"]
        hours = max(0, min(hours, daily_cap - self.hours_gamed))
        self.hours_gamed += hours
        self.change_mood(5 * hours)
        return messages

    def socialize(self, hours):
        messages = self.add_hours(hours)
        self.money -= 10 * hours
        self.change_energy(-5 * hours)
        daily_cap = 3
        if "SOCIALIZING_CAP" in self.disease_stage:
            daily_cap = self.disease_stage["SOCIALIZING_CAP"]
        hours = max(0, min(hours, daily_cap - self.hours_socialized))
        self.hours_socialized += hours
        mood_bonus = 10 * hours
        if "SOCIALIZING_MULTIPLIER" in self.disease_stage:
            mood_bonus *= self.disease_stage["SOCIALIZING_MULTIPLIER"]
        self.change_mood(mood_bonus)
        self.last_social = 0
        return messages

    def call(self, recipient):
        messages = self.add_hours(1)
        if recipient in CALL_DICT["parents"]:
            if not self.called_parents:
                self.change_mood(5)
                self.called_parents = True
            if self.get_mood() < 20:
                messages.append("Your parents notice how rough you're feeling and are worried")
            elif self.get_mood() < 50:
                messages.append("Your parents notice you're feeling down and try to cheer you up")
            elif self.get_mood() > 150:
                messages.append("Your parents can barely understand you.  They are seriously worried about you")
            else:
                messages.append("You have a lovely chat with your parents")
            if self.money < 0:
                self.money = 0
                messages.append("Your parents bail you out of your debt.  You feel guilty")
        elif recipient in CALL_DICT["friend"]:
            if not self.called_friend:
                self.change_mood(5)
                self.called_friend = True
            if self.get_mood() < 20:
                messages.append("Your friend notices how rough you're feeling and is worried")
            elif self.get_mood() < 50:
                messages.append("Your friend notices you're not very happy and tries to cheer you up")
            elif self.get_mood() > 150:
                messages.append("You seriously freak out your friend, who can barely get a word in edgewise")
            else:
                messages.append("You have a lovely chat with a friend")
        elif recipient in CALL_DICT["hospital"]:
            if "HOSPITAL_MESSAGE" in self.disease_stage:
                messages.append(self.disease_stage["HOSPTIAL_MESSAGE"])
            else:
                messages.append("You are turned away.  Try 'call doctor'")
            if "HOSPTIAL_STAGE"  in self.disease_stage:
                messages.extend(self.change_stage(self.disease_stage["HOSPTIAL_STAGE"]))
        elif recipient in CALL_DICT["doctor"]:
            if "DOCTOR_MESSAGE" in self.disease_stage:
                messages.append(self.disease_stage["DOCTOR_MESSAGE"])
            else:
                messages.append("You seem to be in fine health")
            if "DOCTOR_STAGE" in self.disease_stage:
                messages.extend(self.change_stage(self.disease_stage["DOCTOR_STAGE"]))
        elif recipient in CALL_DICT["helpline"]:
            messages.append("The helpline details resources available to you.  Try 'call psychologist', 'call doctor', or 'call hospital'")
        elif recipient in CALL_DICT["psychologist"]:
            if "PSYCHOLOGIST_MESSAGE" in self.disease_stage:
                messages.append(self.disease_stage["PSYCHOLOGIST_MESSAGE"])
            else:
                messages.append("They psychologist patiently listens to your problems")
            if "PSYCHOLOGIST_STAGE" in self.disease_stage:
                messages.extend(self.change_stage(self.disease_stage["PSYCHOLOGIST_STAGE"]))
        return messages

    def read(self, hours):
        messages = self.add_hours(hours)
        hours = max(0, min(hours, 4 - self.hours_read))
        self.hours_read += hours
        self.change_mood(5 * hours)
        return messages

    def watch(self, hours):
        messages = self.add_hours(hours)
        hours = max(0, min(hours, 4 - self.hours_watched))
        self.hours_watched += hours
        self.change_mood(5 * hours)
        return messages

class Sdabto_Cmd(cmd.Cmd):
    prompt = 'What would you like to do? '

    def __init__(self, character):
        super(Sdabto_Cmd, self).__init__()
        self.character = character
        self.bad_command = False

    def print_status(self):
        mood = self.character.get_mood()
        energy = self.character.get_energy()
        day = (self.character.hours_played // 24) + 1
        hour = self.character.hours_played % 24
        print("Day: " + str(day) + " Hour: " + str(hour) + " Mood: " + str(mood) +\
                " Energy: " + str(energy) + " Money: $" + str(self.character.money) +\
                " Food: " + str(self.character.groceries) + " meals")
        hunger_time = MEAL_INTERVAL
        if "HUNGER_DELAY" in self.character.disease_stage:
            hunger_time += self.character.disease_stage["HUNGER_DELAY"]
        if self.character.last_meal > hunger_time:
            print("You feel hungry")
        if self.character.last_sleep > SLEEP_INTERVAL:
            print("You feel sleepy")
        if self.character.last_exercise > EXERCISE_INTERVAL:
            print("You feel lethargic")
        if self.character.last_social > SOCIAL_INTERVAL:
            print("You feel lonely")
        if self.character.last_cleaned > CLEANING_INTERVAL:
            print("Your house is a mess")

    def preloop(self):
        print("Welcome to Some Days Are Better Than Others")
        print("Trigger Warning: Suicide")
        print("Type 'help' of '?' for some ideas of what to do")
        print()
        self.print_status()

    def postloop(self):
        print("Goodbye")

    def default(self, line):
        print("Sorry, that command is not recognized.  Try 'help' or '?' for suggestions")
        self.bad_command = True

    def precmd(self, line):
        if line.startswith("eval"):
            return line
        return line.lower()

    def postcmd(self, stop, line):
        if self.character.dead:
            print("You have died.  Game over")
            return True
        if not stop and not line.startswith("help") and not line.startswith("?") and not self.bad_command:
            if "LOSS_OF_CONTROL_CHANCE" in self.character.disease_stage and \
                    random.random() < self.character.disease_stage["LOSS_OF_CONTROL_CHANCE"]:
                print("You lose control for about 8 hours")
                messages = self.character.add_hours(8)
                activity = random.choice(self.character.disease_stage["ACTIVITIES"])
                if activity == "SHOPPING":
                    print("You go shopping and spend all of your money on home furnishings")
                    self.character.money = -200
                elif activity == "DRIVING":
                    print("You rent a car and go for a drive.  You find yourself driving much too fast")
                    if random.random() < SPEEDING_RISK:
                        print("You get into a terrible car accident.  You and the other driver are both killed")
                        print("Game over")
                        self.character.dead = True
                        return True
                elif activity == "ART":
                    print("You start creating a gorgeous calligraphy project")
                elif activity == "MUSIC":
                    print("You find yourself thinking in rhymes and start writing songs")
            self.print_status()
            print()
        self.bad_command = False
        return stop

    def get_sanitize_hour_str(self, hours):
        '''Given an int of hours, create the hour string the sanitize method needs'''
        hour_str = ""
        if hours == 1:
            hour_str = "after 1 hour "
        elif hours > 1:
            hour_str = "after " + str(hours) + " hours "
        return hour_str

    def sanitize(self, arg):
        try:
            hours = int(arg)
        except ValueError:
            print("This command requires a number of hours, as in 'sleep 8'")
            return None
        if "MEAL_TIMES" in self.character.disease_stage:
            if self.character.hours_played % 24 <= self.character.disease_stage["MEAL_TIMES"][0] and \
                    (self.character.hours_played % 24) + hours > self.character.disease_stage["MEAL_TIMES"][0]:
                hours = self.character.disease_stage["MEAL_TIMES"][0] - (self.character.hours_played % 24)
                hour_str = self.get_sanitize_hour_str(hours)
                print("A nurse stops you " + hour_str + "to tell you it is breakfast time")
            if self.character.hours_played % 24 <= self.character.disease_stage["MEAL_TIMES"][1] and \
                    (self.character.hours_played % 24) + hours > self.character.disease_stage["MEAL_TIMES"][1]:
                hours = self.character.disease_stage["MEAL_TIMES"][1] - (self.character.hours_played % 24)
                hour_str = self.get_sanitize_hour_str(hours)
                print("A nurse stops you " + hour_str + "to tell you it is lunch time")
            if self.character.hours_played % 24 <= self.character.disease_stage["MEAL_TIMES"][2] and \
                    (self.character.hours_played % 24) + hours > self.character.disease_stage["MEAL_TIMES"][2]:
                hours = self.character.disease_stage["MEAL_TIMES"][2] - (self.character.hours_played % 24)
                hour_str = self.get_sanitize_hour_str(hours)
                print("A nurse stops you " + hour_str + "to tell you it is dinner time")
        if hours == 0:
            return None
        return hours

    def do_eval(self, arg):
        '''for debugging only'''
        eval(arg)

    def do_exit(self, arg):
        '''Exit the program'''
        return True

    def do_quit(self, arg):
        '''Exit the program'''
        return True

    def do_clean(self, arg):
        '''Clean your house'''
        if "HOSPITAL_ACTIVITIES" in self.character.disease_stage:
            print("You're not at home right now")
            return
        if "WORK_FAILURE" in self.character.disease_stage and \
                random.random() < self.character.disease_stage["WORK_FAILURE"]:
            print("You can't be bothered to clean anything right now")
            return
        if self.character.get_energy() < 20:
            print("You're too tired to face cleaning right now")
            return
        messages = self.character.clean()
        print("You clean your house")
        for message in messages:
            print(message)

    def do_eat(self, arg):
        '''Eat a meal'''
        if "MEAL_TIMES" in self.character.disease_stage and \
                self.character.hours_played % 24 not in self.character.disease_stage["MEAL_TIMES"]:
            print("It is not meal time yet")
            return
        if self.character.last_meal < 4 or \
                ("EAT_FAILURE" in self.character.disease_stage and \
                random.random() < self.character.disease_stage["EAT_FAILURE"]):
            print("You don't feel like eating right now")
            return
        messages = self.character.eat()
        print("You eat a meal")
        for message in messages:
            print(message)

    def do_work(self, arg):
        '''Work to gain money.  Please supply a number of hours, as in 'work 4' '''
        hours = self.sanitize(arg)
        if hours is None:
            return
        if "HOSPITAL_ACTIVITIES" in self.character.disease_stage:
            print("Your doctor doesn't want you to work while you're in the hospital")
            return
        if "WORK_FAILURE" in self.character.disease_stage and \
                random.random() < self.character.disease_stage["WORK_FAILURE"]:
            print("You sit down to work but end up playing video games instead")
            self.do_game(hours)
            return
        if self.character.get_energy() < 20:
            print("You try to work but your eyes can't focus on the screen.")
            return
        if hours > 8:
            print("After 8 hours your mind starts to wander...")
            hours = 8
        if "FOCUS_CHANCE" in self.character.disease_stage and \
                random.random() < self.character.disease_stage["FOCUS_CHANCE"]:
            print("You get in the zone and loose track of time.  You work for 8 hours")
            hours = 8
        messages = self.character.work(hours)
        print("You go to your computer and work.  You now have $" + str(self.character.money))
        for message in messages:
            print(message)

    def do_sleep(self, arg):
        '''Sleep to get your energy back.  Please supply a number of hours, as in 'sleep 8' '''
        hours = self.sanitize(arg)
        if hours is None:
            return
        if "SLEEP_CAP" in self.character.disease_stage:
            if hours > self.character.disease_stage["SLEEP_CAP"]:
                print("You can't sleep.  You wake up early feeling fully rested")
                hours = self.character.disease_stage["SLEEP_CAP"]
        if hours > 12:
            print("After 12 hours you wake up.")
            hours = 12
        messages = self.character.sleep(hours)
        print("You sleep for " + str(hours) + " hours.  Your energy is now " + str(self.character.get_energy()))
        if "WAKEUP_DELAY" in self.character.disease_stage:
            hour_str = " hours"
            if self.character.disease_stage["WAKEUP_DELAY"] == 1:
                hour_str = " hour"
            print("You stay in bed for " + str(self.character.disease_stage["WAKEUP_DELAY"]) + hour_str)
            self.character.add_hours(self.character.disease_stage["WAKEUP_DELAY"])
        for message in messages:
            print(message)

    def do_exercise(self, arg):
        '''Go for a run'''
        if "HOSPITAL_ACTIVITIES"  in self.character.disease_stage:
            print("You're not allowed outside yet")
            return
        if "MEAL_TIMES" in self.character.disease_stage and \
                self.character.hours_played % 24 in self.character.disease_stage["MEAL_TIMES"]:
            print("A nurse stops you to tell you it is meal time")
            return
        if self.character.get_energy() < 20:
            print("Contemplating a run makes you feel exhausted.  Maybe tomorrow...")
            return
        print("You go for a run")
        for message in self.character.exercise():
            print(message)

    def do_shop(self, arg):
        '''Buy more groceries'''
        if "HOSPITAL_ACTIVITIES"  in self.character.disease_stage:
            print("You're not allowed outside yet")
            return
        if "MEAL_TIMES" in self.character.disease_stage and \
                self.character.hours_played % 24 in self.character.disease_stage["MEAL_TIMES"]:
            print("A nurse stops you to tell you it is meal time")
            return
        if self.character.get_energy() < 10:
            print("You're too tired to haul home food.  There must be something in the fridge...")
            return
        if self.character.hours_played % 24 < 8 or self.character.hours_played % 24 > 22:
            print("The grocery store is closed right now.")
            return
        if self.character.groceries > 21:
            print("Your fridge is too full for more groceries")
        else:
            print("You buy another week of groceries")
            for message in self.character.shopping():
                print(message)

    def do_game(self, arg):
        '''Play video games.  Please supply a number of hours, as in 'game 1' '''
        hours = self.sanitize(arg)
        if hours is None:
            return
        if hours > 8:
            print("After 8 hours you lose interest")
            hours = 8
        if "FOCUS_CHANCE" in self.character.disease_stage and \
                random.random() < self.character.disease_stage["FOCUS_CHANCE"]:
            print("You get in the zone and loose track of time.  You game for 8 hours")
            hours = 8
        messages = self.character.game(hours)
        print("You play on your computer.  Your mood is now " + str(self.character.get_mood()))
        for message in messages:
            print(message)

    def do_socialize(self, arg):
        '''Go out with friends.  Please supply a number of hours, as in 'socialize 2' '''
        if "HOSPITAL_ACTIVITIES"  in self.character.disease_stage:
            print("You're not allowed outside yet")
            return
        if self.character.get_energy() < 20:
            print("You can't summon the energy to face people right now.  How about a quiet night in?")
            return
        if "SOCIALIZE_FAILURE" in self.character.disease_stage and \
                random.random() < self.character.disease_stage["SOCIALIZE_FAILURE"]:
            print("You get too anxious thinking about people right now.  How about a quiet night in?")
            return
        hours = self.sanitize(arg)
        if hours is None:
            return
        if hours > 6:
            print("None of your friends are free for more than 6 hours")
            hours = 6
        if "FOCUS_CHANCE" in self.character.disease_stage and \
                random.random() < self.character.disease_stage["FOCUS_CHANCE"]:
            print("You lose track of time and stay out for 6 hours")
            hours = 6
            effect = random.choice(self.character.disease_stage["SOCIALIZING_EFFECTS"])
            if effect == "DRUNK":
                print("You have a drink, and then another and another and another.  You black out")
                if random.random() < ALCOHOL_POISONING_CHANCE:
                    print("You get severe alcohol poisoning")
                    self.character.dead = True
                    return True
                print("Later your friends, freaked out, tell you you thought you were a character from the last book you read")
            elif effect == "INAPPROPRIATE":
                print("You start making more and more inappropriate jokes.  Some people laugh riotously, but an old friend looks disgusted")
            elif effect == "PROMISCUOUS":
                print("You hook up with someone you just met")
        messages = self.character.socialize(hours)
        print("You hang out with friends.  You now have $" + str(self.character.money))
        for message in messages:
            print(message)

    def do_call(self, arg):
        '''Call someone on the phone, as in 'call mom' '''
        if "MEAL_TIMES" in self.character.disease_stage and \
                self.character.hours_played % 24 in self.character.disease_stage["MEAL_TIMES"]:
            print("A nurse stops you to tell you it is meal time")
            return
        caller_known = False
        for key, synonym_list in CALL_DICT.items():
            if arg in synonym_list:
                caller_known = True
                break
        if not caller_known:
            print("Sorry, recipient unknown")
            return
        for message in self.character.call(arg):
            print(message)

    def do_read(self, arg):
        '''Read a book.  Please supply a number of hours, as in 'read 4' '''
        hours = self.sanitize(arg)
        if hours is None:
            return
        if "LEISURE_FAILURE" in self.character.disease_stage and \
                random.random() < self.character.disease_stage["LEISURE_FAILURE"]:
            print("You try to read but the words swim on the page")
            return
        if hours > 4:
            hours = 4
            print("After 4 hours you lose interest")
        messages = self.character.read(hours)
        print("You read a book")
        for message in messages:
            print(message)

    def do_watch(self, arg):
        '''Watch tv or a movie for a number of hours, as in 'watch movie 4' '''
        args = arg.split()
        if len(args) < 2:
            print("Please pick tv or movie and give a number of hours, as in 'watch movie 4'")
            return
        if args[0] != "tv" and args[0] != "movie":
            print("You can watch tv or movies, as in 'watch movie 4'")
            return
        hours = self.sanitize(args[1])
        if hours is None:
            return
        if "LEISURE_FAILURE" in self.character.disease_stage and \
                random.random() < self.character.disease_stage["LEISURE_FAILURE"]:
            print("You try to watch something but you can't stay focused on the plot")
            return
        if hours > 4:
            hours = 4
            print("After 4 hours you lose interest")
        messages = self.character.watch(hours)
        article = ""
        if args[0] == "movie":
            article = "a "
        print("You watch " + article + args[0])
        for message in messages:
            print(message)

def main():
    Sdabto_Cmd(Character()).cmdloop()

if __name__ == '__main__':
    main()
