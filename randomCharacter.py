# For creating random characters in Kaladesh, Ravnica, or therosSets

import constants
from pick import pick
import random

# initialize all the variables!
class NewCharacter:
    plane = ""
    race = ""
    pronouns = ""
    type = ""
    gender = ""

new_character = NewCharacter()

# Pronouns
pronouns = ("she/her","he/him","they/them")
debug = True
weAreLive = True
# we're selecting which tables to use for creating a new random character
while True:
    def chooseTable():
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
        return planeChoice
    # planeChoice = "Kaladesh"

    def raceRolls():
        raceRoll = ""
        # if planeChoice == "Kaladesh":
        kaladesh_npc_table = ("Aetherborn","Construct","Dwarf","Elf","Human","Vedalken")
        kaladesh_npc_weights = [0.25,0.15,0.15,0.15,0.2,0.15]
        kaladesh_npc_race = random.choices(kaladesh_npc_table, kaladesh_npc_weights, k = 1)
        kaladesh_npc_race = str(kaladesh_npc_race[0])
        print(kaladesh_npc_race)
        return kaladesh_npc_race

    new_character.race = raceRolls()
    # continue
    # ravnica_contact_table = ()
    # ravnica_contact_weights []
    def genderRolls():
        gender_roll = ""
        enby_races = ("Construct","Warforged")
        elfy_races = ("Elf","Half Elf","High Elf")
        if new_character.race in enby_races:
            gender_roll = pronouns[2]
            print("Enby: "+gender_roll)
        elif new_character.race in elfy_races:
            gender_roll = random.choice(pronouns)
            print("Elfy: "+gender_roll)
        else:
            boring_gender_weights = [0.45,0.45,0.1]
            gender_roll = random.choices(pronouns,boring_gender_weights, k = 1)
            gender_roll = str(gender_roll[0])
        print(gender_roll)
        return gender_roll

    new_character.gender = genderRolls()
    # else:
    #    genderRoll = roll(1d100)
    #    if genderRol1 in range(1-10):
    #        newChar.pronouns = 2
    #    elif genderRoll in range(11-55):
    #        newChar.pronouns = 0
    #    else:
    #        newChar.pronouns = 1
    # continue
    print(new_character.race)
    print(new_character.gender)
    print("Your new character is a "+new_character.race+" whose pronouns are "+new_character.gender)
    quit()
#    if newChar.type.lower() == "" or
