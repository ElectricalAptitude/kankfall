# For creating random characters in Kaladesh, Ravnica, or therosSets

from pick import pick
from random import randint

# initialize all the variables!
newChar = {
    "plane":0,
    "race":0,
    "pronouns":0,
    "type":0
    }

pronouns = 

def roll(roll):

    rolling = []

    try:
        for x in range(int(roll.split('d')[0])):
            rolling.append(randint(1,int(roll.split('d')[1])))
    except Exception as err:
        print(f'I got bungled @_@ \n Error: {err}')

    print(f'You rolled {" ".join(str(x) for x in rolling)} which has a total'
          f' of {sum(rolling)}')

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


def genderRolls:
    if newChar.race == :
        newChar.gender = 1
    elif newChar in elf and newChar !in drow:
        roll 1d3
1 - male
2 - female
3 - enby
else:
roll 1d100
1-45 - female
45-90 - male
91-100 - enby



    if newChar.type.lower() == "" or
