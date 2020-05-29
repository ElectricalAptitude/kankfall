# For creating random characters in Kaladesh, Ravnica, or therosSets

import statics
from pick import pick
import random

# initialize all the variables!
newChar = {
    "plane":0,
    "race":0,
    "pronouns":0,
    "type":0,
    }

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
    # kaladesh_NPC_table = ("Aetherborn","Construct","Dwarf","Elf","Human","Vedalken")
    #
    # kaladesh_contact_table

def genderRolls:
    genderRoll = 0
    enbyRaces = ("Construct","Warforged")
    elfyRaces = ("Elf","Half Elf","High Elf")
    if newChar.race in enbyRaces:
        newChar.pronouns = 0
    elif newChar.race in elfyRaces:
        genderRoll = random.choice(pronouns)
    else:
        genderRoll = roll(1d100)
        if genderRol1 in range(1-10):
            newChar.pronouns = 2
        elif genderRoll in range(11-55):
            newChar.pronouns = 0
        else:
            newChar.pronouns = 1
    continue
#    if newChar.type.lower() == "" or
