import cmd

#globals
#costs in dollars
rent = 150
groceries = 50
#allowable time between events.
meal_interval = 6 #hours
sleep_interval = 16 #hours
exercise_interval = 2 #days
social_interval = 2 #days

class Character:
    def __init__(self):
        #out of 100
        self.base_mood = 80
        #out of 100
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

    def change_mood(self, diff):
        self.base_mood = self.base_mood + diff
        if self.base_mood < 0:
            self.base_mood = 0
        elif self.base_mood > 100:
            self.base_mood = 100

    def change_energy(self, diff):
        self.base_energy = self.base_energy + diff
        if self.base_energy < 0:
            self.base_energy = 0
        elif self.base_energy > 100:
            self.base_energy = 100

    def add_hours(self, hours):
        #if we crossed a day boundary
        if (self.hours_played // 24) < ((self.hours_played + hours) // 24):
            self.last_exercise = self.last_exercise + 1
            self.last_social = self.last_social + 1
        self.last_meal = self.last_meal + hours
        self.last_sleep = self.last_sleep + hours
        self.hours_played = self.hours_played + hours

    def get_mood(self):
        mood = self.base_mood
        if self.last_meal > meal_interval:
            mood = mood - 10 * (self.last_meal - meal_interval)
        if self.last_exercise > exercise_interval:
            mood = mood - 10 * (self.last_exercise - exercise_interval)
        if self.last_social > social_interval:
            mood = mood - 10 * (self.last_social - social_interval)
        if mood < 0:
            mood = 0
        elif mood > 100:
            mood = 100
        return mood

    def get_energy(self):
        energy = self.base_energy
        if self.last_meal > meal_interval:
            energy = energy - 10 * (self.last_meal - meal_interval)
        if self.last_sleep > sleep_interval:
            energy = energy - 10 * (self.last_sleep - sleep_interval)
        if self.last_exercise > exercise_interval:
            energy = energy - 10 * (self.last_exercise - exercise_interval)
        if energy < 0:
            energy = 0
        elif energy > 100:
            energy = 100
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
        self.base_energy = 10 * hours
        if hours > 6:
            self.base_energy = self.base_energy + 20

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
        self.money = self.money - 50
        self.groceries = self.groceries + 21
        if self.groceries > 42:
            self.groceries = 42

    def game(self, hours):
        self.add_hours(hours)
        #fix this later to track hours spent gaming per day
        if hours > 4:
            hours = 4
        self.change_mood(5 * hours)

    def socialize(self, hours):
        self.add_hours(hours)
        self.money = self.money - 10 * hours
        self.change_energy(-5 * hours)
        if hours > 3:
            hours = 3
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
        if not stop:
            if self.character.last_meal > meal_interval:
                print("You feel hungry")
            if self.character.last_sleep > sleep_interval:
                print("You feel sleepy")
            if self.character.last_exercise > exercise_interval:
                print("You feel lethargic")
            if self.character.last_social > social_interval:
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
        self.character.eat()
        print("You eat a meal.  You now have " + str(self.character.groceries) + " meals left")

    def do_work(self, arg):
        '''Work to gain money.  Please supply a number of hours, as in 'work 4' '''
        hours = self.sanitize(arg)
        if hours is None:
            return
        self.character.work(hours)
        print("You go to your computer and work.  You now have $" + str(self.character.money))

    def do_sleep(self, arg):
        '''Sleep to get your energy back.  Please supply a number of hours, as in 'sleep 8' '''
        hours = self.sanitize(arg)
        if hours is None:
            return
        self.character.sleep(hours)
        print("You sleep for " + str(hours) + " hours.  Your energy is now " + str(self.character.get_energy()))

    def do_exercise(self, arg):
        '''Go for a run'''
        self.character.exercise()
        print("You go for a run")

    def do_shop(self, arg):
        '''Buy more groceries'''
        self.character.shopping()
        print("You buy another week of groceries")
        if self.character.groceries == 42:
            print("Your fridge is full")

    def do_game(self, arg):
        '''Play video games.  Please supply a number of hours, as in 'game 1' '''
        hours = self.sanitize(arg)
        if hours is None:
            return
        self.character.game(hours)
        print("You play on your computer.  Your mood is now " + str(self.character.get_mood()))

    def do_socialize(self, arg):
        '''Go out with friends.  Please supply a number of hours, as in 'socialize 2' '''
        hours = self.sanitize(arg)
        if hours is None:
            return
        self.character.socialize(hours)
        print("You hang out with friends.  You now have $" + str(self.character.money))


def main():
    Sdabto_Cmd(Character()).cmdloop()

if __name__ == '__main__':
    main()
