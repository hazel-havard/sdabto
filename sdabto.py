import cmd
import random

#globals
#costs in dollars
RENT = 150
GROCERIES = 50
#allowable time between events.
MEAL_INTERVAL = 6 #hours
SLEEP_INTERVAL = 16 #hours
EXERCISE_INTERVAL = 2 #days
SOCIAL_INTERVAL = 2 #days
#messages
NORMAL_THOUGHTS = ["You daydream about saving a baby from a fire",\
        "You imagine what you would do if you were fabulously wealthy",\
        "You fondly remember an old friend"]
SUICIDAL_IDEATION_MINOR = ["You wonder how many advil you would have to take before you died",\
        "You wonder if your pen knife is sharp enough to cut your throat",\
        "You suddenly imagine shooting yourself"]
SUICIDAL_IDEATION_MAJOR = ["You look up the LD50 of advil and figure out how much you'd need to kill yourself",\
        "You make a plan to kill yourself by cutting your throat in a running shower so there'd be no mess",\
        "You compose an email to the coroner so that no one you know would have to find your body"]
SUICIDAL_IDEATION_EXTREME = ["You hold a pillow over your head until you pass out to see what suffocating is like,"\
        "You summon the strength to buy a lethal dose of advil",\
        "You pack your things so they will be easier to take care of when you're gone"]
#disease stages
DEPRESSION3 = {"INTRO_MESSAGE": "You feel worse than you ever have before",\
        "LENGTH": 2,\
        "NEXT_STAGE": None,\
        "CAP": 10,\
        "HUNGER_DELAY": 24,\
        "THOUGHTS": SUICIDAL_IDEATION_EXTREME,\
        "THOUGHT_FREQ": 1,\
        "SOCIALIZE_FAILURE": 1,\
        "WAKEUP_DELAY": 4}
DEPRESSION2 = {"INTRO_MESSAGE": "You feel rough",\
        "LENGTH": 7,\
        "NEXT_STAGE": DEPRESSION3,\
        "CAP": 40,\
        "HUNGER_DELAY": 8,\
        "THOUGHTS": SUICIDAL_IDEATION_MAJOR,\
        "THOUGHT_FREQ": 12/24,\
        "SOCIALIZE_FAILURE": 0.8,\
        "WAKEUP_DELAY": 2}
DEPRESSION1 = {"INTRO_MESSAGE": "You feel a little off",\
        "LENGTH": 7,\
        "NEXT_STAGE": DEPRESSION2,\
        "CAP": 80,\
        "HUNGER_DELAY": 2,\
        "THOUGHTS": SUICIDAL_IDEATION_MINOR,\
        "THOUGHT_FREQ": 1/24,\
        "SOCIALIZE_FAILURE": 0.2,\
        "WAKEUP_DELAY": 1}
NORMAL = {"INTRO_MESSAGE": None,\
        "LENGTH": 7,\
        "NEXT_STAGE": DEPRESSION1,\
        "CAP": 100,\
        "HUNGER_DELAY": 0,\
        "THOUGHTS": NORMAL_THOUGHTS,\
        "THOUGHT_FREQ": 1/24,\
        "SOCIALIZE_FAILURE": 0,\
        "WAKEUP_DELAY": 0}

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
        #number of meals
        self.groceries = 21
        self.hours_played = 8
        self.hours_gamed = 0
        self.hours_socialized = 0
        self.disease_stage = NORMAL
        self.disease_days = 0
        self.dead = False

    def change_mood(self, diff):
        self.base_mood = self.base_mood + diff
        if self.base_mood < 0:
            self.base_mood = 0
        elif self.base_mood > self.disease_stage["CAP"]:
            self.base_mood = self.disease_stage["CAP"]

    def change_energy(self, diff):
        self.base_energy = self.base_energy + diff
        if self.base_energy < 0:
            self.base_energy = 0
        elif self.base_energy > self.disease_stage["CAP"]:
            self.base_energy = self.disease_stage["CAP"]

    def add_hours(self, hours):
        #if we crossed a day boundary
        if (self.hours_played // 24) < ((self.hours_played + hours) // 24):
            self.hours_gamed = 0
            self.hours_socialized = 0
            self.last_exercise = self.last_exercise + 1
            self.last_social = self.last_social + 1
            self.disease_days = self.disease_days + 1
            if self.disease_days >= self.disease_stage["LENGTH"]:
                if self.disease_stage["NEXT_STAGE"] is None:
                    self.dead = True
                    return
                if self.disease_stage == DEPRESSION2:
                    print("6 months pass this way, playing video games and barely scraping by")
                    self.money = 0
                    self.last_exercise = 7
                    self.last_social = 7
                    self.hours_gamed = 0
                    self.hours_socialized = 0
                    self.hours_played = self.hours_played + (24 * 30 * 6)
                self.disease_stage = self.disease_stage["NEXT_STAGE"]
                self.disease_days = 0
                print(self.disease_stage["INTRO_MESSAGE"])
            if ((self.hours_played + hours) // 24) % 7 == 0:
                self.money = self.money - RENT
                print("Rent deducted.  You now have $" + str(self.money))
        self.last_meal = self.last_meal + hours
        self.last_sleep = self.last_sleep + hours
        self.hours_played = self.hours_played + hours
        if random.random() < self.disease_stage["THOUGHT_FREQ"] * hours:
            print(random.choice(self.disease_stage["THOUGHTS"]))
        if self.last_meal > 24 * 7:
            self.dead = True

    def get_mood(self):
        mood = self.base_mood
        if self.last_meal > MEAL_INTERVAL:
            mood = mood - min(10 * (self.last_meal - MEAL_INTERVAL), 30)
        if self.last_exercise > EXERCISE_INTERVAL:
            mood = mood - min(5 * (self.last_exercise - EXERCISE_INTERVAL), 20)
        if self.last_social > SOCIAL_INTERVAL:
            mood = mood - min(5 * (self.last_social - SOCIAL_INTERVAL), 20)
        if mood < 0:
            mood = 0
        elif mood > self.disease_stage["CAP"]:
            mood = self.disease_stage["CAP"]
        return mood

    def get_energy(self):
        energy = self.base_energy
        if self.last_meal > MEAL_INTERVAL:
            energy = energy - min(10 * (self.last_meal - MEAL_INTERVAL), 30)
        if self.last_sleep > SLEEP_INTERVAL:
            energy = energy - min(5 * (self.last_sleep - SLEEP_INTERVAL), 20)
        if self.last_exercise > EXERCISE_INTERVAL:
            energy = energy - min(5 * (self.last_exercise - EXERCISE_INTERVAL), 20)
        if energy < 0:
            energy = 0
        elif energy > self.disease_stage["CAP"]:
            energy = self.disease_stage["CAP"]
        return energy

    def work(self, hours):
        self.add_hours(hours)
        self.money = self.money + 10 * hours
        self.change_energy(-5 * hours)
        self.change_mood(-5 * hours)

    def sleep(self, hours):
        self.add_hours(hours)
        if hours < 4:
            return
        if hours > 8:
            hours = 8
        self.last_sleep = 0
        self.base_energy = min((10 * hours), self.disease_stage["CAP"])
        if hours > 6:
            self.change_energy(20)

    def eat(self):
        self.add_hours(1)
        self.last_meal = 0
        self.groceries = self.groceries - 1

    def exercise(self):
        self.add_hours(1)
        self.last_exercise = 0
        self.change_mood(5)
        self.change_energy(-5)

    def shopping(self):
        self.add_hours(1)
        self.money = self.money - GROCERIES
        self.groceries = self.groceries + 21
        if self.groceries > 42:
            self.groceries = 42

    def game(self, hours):
        self.add_hours(hours)
        hours = max(0, min(hours, 4 - self.hours_gamed))
        self.hours_gamed = self.hours_gamed + hours
        self.change_mood(5 * hours)

    def socialize(self, hours):
        self.add_hours(hours)
        self.money = self.money - 10 * hours
        self.change_energy(-5 * hours)
        hours = max(0, min(hours, 3 - self.hours_socialized))
        self.hours_socialized = self.hours_socialized + hours
        self.change_mood(10 * hours)
        self.last_social = 0

class Sdabto_Cmd(cmd.Cmd):
    intro = '''Welcome to Some Days Are Better Than Others
Trigger Warning: Suicide
Type 'help' or '?' for some suggestions of what to do.\n'''
    prompt = 'What would you like to do? '

    def __init__(self, character):
        super(Sdabto_Cmd, self).__init__()
        self.character = character

    def postloop(self):
        print("Goodbye")

    def default(self, line):
        print("Sorry, that command is not recognized.  Try 'help' or '?' for suggestions")

    def postcmd(self, stop, line):
        if self.character.dead:
            print("You have died.  Game over")
            return True
        if not stop:
            if self.character.last_meal > MEAL_INTERVAL + self.character.disease_stage["HUNGER_DELAY"]:
                print("You feel hungry")
            if self.character.last_sleep > SLEEP_INTERVAL:
                print("You feel sleepy")
            if self.character.last_exercise > EXERCISE_INTERVAL:
                print("You feel lethargic")
            if self.character.last_social > SOCIAL_INTERVAL:
                print("You feel lonely")
        return stop

    def sanitize(self, arg):
        try:
            hours = int(arg)
        except ValueError:
            print("This command requires a number of hours, as in 'sleep 8'")
            return None
        return hours

    def do_exit(self, arg):
        '''Exit the program'''
        return True

    def do_quit(self, arg):
        '''Exit the program'''
        return True

    def do_status(self, arg):
        '''Return your vital statistics'''
        mood = self.character.get_mood()
        energy = self.character.get_energy()
        day = (self.character.hours_played // 24) + 1
        hour = self.character.hours_played % 24
        print("Day: " + str(day) + " Hour: " + str(hour) + " Mood: " + str(mood) +\
                " Energy: " + str(energy) + " Money: $" + str(self.character.money) +\
                " Food: " + str(self.character.groceries) + " meals")
        #for debugging
        print("last_meal: "  + str(self.character.last_meal))
        print("last_sleep: "  + str(self.character.last_sleep))
        print("last_exercise: "  + str(self.character.last_exercise))
        print("last_social: "  + str(self.character.last_social))

    def do_eat(self, arg):
        '''Eat a meal'''
        if self.character.last_meal < 4:
            print("You're not hungry right now")
            return
        self.character.eat()
        print("You eat a meal.  You now have " + str(self.character.groceries) + " meals left")

    def do_work(self, arg):
        '''Work to gain money.  Please supply a number of hours, as in 'work 4' '''
        if self.character.get_energy() < 20:
            print("You try to work but your eyes can't focus on the screen.")
            return
        hours = self.sanitize(arg)
        if hours is None:
            return
        if hours > 8:
            print("After 8 hours your mind starts to wander...")
            hours = 8
        self.character.work(hours)
        print("You go to your computer and work.  You now have $" + str(self.character.money))

    def do_sleep(self, arg):
        '''Sleep to get your energy back.  Please supply a number of hours, as in 'sleep 8' '''
        hours = self.sanitize(arg)
        if hours is None:
            return
        if hours > 12:
            print("After 12 hours you wake up.")
            hours = 12
        self.character.sleep(hours)
        print("You sleep for " + str(hours) + " hours.  Your energy is now " + str(self.character.get_energy()))
        if self.character.disease_stage["WAKEUP_DELAY"] > 0:
            hour_str = " hours"
            if self.character.disease_stage["WAKEUP_DELAY"] == 1:
                hour_str = " hour"
            print("You stay in bed for " + str(self.character.disease_stage["WAKEUP_DELAY"]) + hour_str)
            self.character.add_hours(self.character.disease_stage["WAKEUP_DELAY"])

    def do_exercise(self, arg):
        '''Go for a run'''
        if self.character.get_energy() < 20:
            print("Contemplating a run makes you feel exhausted.  Maybe tomorrow...")
            return
        self.character.exercise()
        print("You go for a run")

    def do_shop(self, arg):
        '''Buy more groceries'''
        if self.character.get_energy() < 10:
            print("You're too tired to haul home food.  There must be something in the fridge...")
            return
        if self.character.hours_played % 24 < 8 or self.character.hours_played % 24 > 22:
            print("The grocery store is closed right now.")
            return
        if self.character.groceries > 21:
            print("Your fridge is too full for more groceries")
        else:
            self.character.shopping()
            print("You buy another week of groceries")

    def do_game(self, arg):
        '''Play video games.  Please supply a number of hours, as in 'game 1' '''
        hours = self.sanitize(arg)
        if hours is None:
            return
        if hours > 8:
            print("After 8 hours you lose interest")
            hours = 8
        self.character.game(hours)
        print("You play on your computer.  Your mood is now " + str(self.character.get_mood()))

    def do_socialize(self, arg):
        '''Go out with friends.  Please supply a number of hours, as in 'socialize 2' '''
        if self.character.get_energy() < 20:
            print("You can't summon the energy to face people right now.  How about a quiet night in?")
            return
        if random.random() < self.character.disease_stage["SOCIALIZE_FAILURE"]:
            print("You get too anxious thinking about people right now.  How about a quiet night in?")
            return
        hours = self.sanitize(arg)
        if hours is None:
            return
        if hours > 6:
            print("None of your friends are free for more than 6 hours")
            hours = 6
        self.character.socialize(hours)
        print("You hang out with friends.  You now have $" + str(self.character.money))


def main():
    Sdabto_Cmd(Character()).cmdloop()

if __name__ == '__main__':
    main()
