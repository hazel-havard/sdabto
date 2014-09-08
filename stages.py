import messages
import random

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
#disease stages
#Must have LENGTH, CAP, THOUGHTS, & THOUGHT_FREQ
MEDICATED_DEPRESSION = {}
MEDICATED = {"INTRO_MESSAGE": "You can feel things again",\
        "LENGTH": 21,\
        "NEXT_STAGE": MEDICATED_DEPRESSION,\
        "CAP": 100,\
        "THOUGHTS": messages.NORMAL_THOUGHTS,\
        "THOUGHT_FREQ": 1/24,\
        "DOCTOR_MESSAGE": "Everything seems okay.  Some side effects are to be expected",\
        "EFFECT": SIDE_EFFECT}
MEDICATED_DEPRESSION = {"INTRO_MESSAGE": "You feel rough",\
        "LENGTH": 7,\
        "NEXT_STAGE": MEDICATED,\
        "CAP": 50,\
        "HUNGER_DELAY": 4,\
        "THOUGHTS": messages.SUICIDAL_IDEATION_MINOR,\
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
        "THOUGHTS": messages.MANIC_THOUGHTS,\
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
        "THOUGHTS": messages.NORMAL_THOUGHTS,\
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
        "THOUGHTS": messages.HOSPITAL_THOUGHTS,\
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
        "THOUGHTS": messages.SUICIDAL_IDEATION_EXTREME,\
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
        "THOUGHTS": messages.SUICIDAL_IDEATION_MAJOR,\
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
        "THOUGHTS": messages.SUICIDAL_IDEATION_MINOR,\
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
        "THOUGHTS": messages.NORMAL_THOUGHTS,\
        "THOUGHT_FREQ": 1/24}

STAGES = (NORMAL, DEPRESSION1, DEPRESSION2, DEPRESSION3, HOSPITALIZED, INITIAL_MEDICATION, MANIA, MEDICATED, MEDICATED_DEPRESSION)
for stage in STAGES:
    if "EFFECT" in stage and "KEYS" in stage["EFFECT"]:
        for key in stage["EFFECT"]["KEYS"]:
            if key in stage:
                stage[key] += stage["EFFECT"]["PENALTY"]
            else:
                stage[key] = stage["EFFECT"]["PENALTY"]
