# For creating random characters in Kaladesh, Ravnica, or therosSets

import statics
from pick import pick
import random

# initialize all the variables!
class Character:
    home_plane = 0
    race = 0
    pronouns = 0
    type = 0
    location = 0
    tags = [kankfall_tag_id]

# Pronouns
pronouns = ("she/her","he/him","they/them")

# we're selecting which tables to use for creating a new random character
def chooseTable:
    tableDetermined = False
    while tableDetermined == False:
        print("I need to know a little bit more...")
        charType = "Is this an NPC or a contact? "
        typeOptions = ["NPC","Contact"]
        typeChoice, typeIndex = pick(typeOptions, charType)
        print(typeChoice)
        # I am adding a comment here because I'm not sure if I break the while loop with a line break
        charPlane = "And are they from Kaladesh, Ravnica, or Theros? "
        planeOptions = ["Kaladesh","Ravnica","Theros"]
        planeChoice, planeIndex = pick(planeOptions, charPlane)
        print(planeChoice)
        tableDetermined == True

def raceRolls:
    raceRoll = 0
    kaladesh_npc_table = ("Aetherborn","Construct","Dwarf","Elf","Human","Vedalken")
    kaladesh_npc_weights = [0.25,0.15,0.15,0.15,0.2,.15]
    #
    # kaladesh_contact_table

def gender_rolls:
    gender_roll = 0
    enby_races = ("Construct","Warforged")
    elfy_races = ("Elf","Half Elf","High Elf")
    if newChar.race in enby_races:
        newChar.pronouns = 2
    elif newChar.race in elfy_races:
        gender_roll = random.choice(range(1,3))
        new_char.pronouns = pronouns[genderRoll]
    else:
        boring_pronoun_weights = [0.45,0.45,0.1]
        genderRoll = random.choices(boring_pronoun_weights,pronouns,k=1)
        new_char.pronouns = pronouncs[gender_roll]
    continue
#    if newChar.type.lower() == "" or
