'''
A Python script that uses data from Scryfall to automatically import MtG cards into Kanka.io. (Trademarks belong to their respective owners; see accompanying documentation for more detail.)

Credit for "do you even POST, bro?" goes to https://www.w3schools.com/python/ref_requests_post.asp 
@author: ElectricalAptitude
@author: SirTechSpec

@created 2020.05.27
@change 2020.05.27 sts ported from https://repl.it/@ElectricalAptit/kankfall#main.py so as to test Kanka interactions without making the API key quite so public.
@change 2020.05.27 sts fixed git nonsense; set to UTF-8; adjustments to pull from constants.py

'''

from builtins import int
import requests
import constants


# import other stuff??
# test cases: gibberish, forest, Arcbound Ravager, Baral, snow-covered swamp, Armor of Faith, Kaervek's Torch
#set program constants
debug = False
weAreLive = True

#import program constants from backup constants file
SCRYFALL_URL = constants.SCRYFALL_URL
RAVNICA_SETS = constants.RAVNICA_SETS
KALADESH_SETS = constants.KALADESH_SETS
THEROS_SETS = constants.THEROS_SETS

KANKA_CHAR_URL = constants.KANKA_CHAR_URL
KANKA_ITEM_URL = constants.KANKA_ITEM_URL
KANKA_LOC_URL = constants.KANKA_LOC_URL
#TODO: read from cfg if available, inc. which sets/locations to use
#TODO: use parameters if available

#don't do magic numbers kids they're bad for you
#TODO: get location IDs straight from Kanka
kaladeshLocationID = 174953
ravnicaLocationID = 174971
therosLocationID = 176830
#TODO: get tag IDs straight from Kanka
kaladeshTagID = 54084
ravnicaTagID = 54085
therosTagID = 54177
kankfallTagID = 55903
#TODO: get race IDs straight from Kanka
raceIDs = {"Aetherborn":67177, "Centaur":67037, "Construct":68699, "Dwarf":67077, "Elf":67493, "Goblin":66961, "Human":66977, "Vedalken":66954}


myToken = "abc123"
with open("cfg/token.auth") as tokenFile:
    myToken = tokenFile.read()
kankaHeaders={"Authorization":"Bearer "+myToken, "Content-type":"application/json"}

while True:
    #run program
    #initialize variables at the start of each run
    cardName = cardSet = cardArtist = cardImgurl = cardFlavor = cardTypeLine = cardTypeParts = cardType = cardSubtype = kankaType = ""
    selectedCard = {}
    planeLocationID = 0
    entryLocation = 0
    tags = []
    kanka_request_URL = ""
    kankaPayload = {}
    postResult = ""

    desiredCardName = input("Type in the name of the card: ") # in python 3, input gives us a str automatically
    desiredCardName = desiredCardName.replace(" ", "+")
    scry_URL = SCRYFALL_URL+desiredCardName+"&unique=prints"

    scry_result = requests.get(scry_URL) #returns a dict with one entry, 'data', whose data is an array of dicts, each of which is one card.
    if scry_result.ok==False:
        print(str(scry_result.status_code)+": "+scry_result.reason)
        continue
    resultJson=scry_result.json()["data"] #so resultJson is an array of dicts (cards)
    print("Cards were found from the following sets:")
    currentCardIndex = 0
    for card in resultJson: #card here is now an actual card
        thisCardSet = card["set_name"]
        print("["+str(currentCardIndex)+"]: "+thisCardSet)
        if thisCardSet in RAVNICA_SETS or thisCardSet in KALADESH_SETS or thisCardSet in THEROS_SETS:
            selectedCard = card
            break
        currentCardIndex += 1
    if selectedCard == {}: continue #if no matches, try again
    print("Selected card number "+str(currentCardIndex))
    cardName = selectedCard["name"]
    cardSet = selectedCard["set_name"]
    cardImgurl = selectedCard["image_uris"]["art_crop"]
    if "flavor_text" in selectedCard:
        cardFlavor = selectedCard["flavor_text"]
    if "artist" in selectedCard:
        cardArtist = selectedCard["artist"]
    cardTypeLine = selectedCard["type_line"]
    cardTypeParts = cardTypeLine.split("—")
    cardType = cardTypeParts[0].strip()
    if len(cardTypeParts) > 1:
        cardSubtype = cardTypeParts[1].strip()

    #let's do a quick check
    print("Name: " + cardName)
    print("Set: " + cardSet)
    print("Imgurl: " + cardImgurl)
    print("Flavor: " + cardFlavor)
    print("Type: " + cardType) #somewhat optimistic
    print("Subtype: " + cardSubtype) #should be empty string if n/a
    print("Does this look right?")
    shallIContinue = input("N for no, otherwise hit Enter: ")
    if shallIContinue.lower() == "n" or shallIContinue.lower() == "no":
        continue #this means don't continue, start over

    #Card input's all finished, woo! Now to some sorting and preparing for output.

    #what manner of beastie are you
    if cardType == "Artifact" or cardType == "Legendary Artifact":
        if cardSubtype == "Vehicle":
            kankaType = "Location"
        else:
            kankaType = "Item"
    if "Creature" in cardType: #could be Artifact Creature, Legendary Creature, Enchantment Creature, or who knows what
        kankaType = "Character"
    if "Land" in cardType :
        kankaType = "Location"
    #quick sanity check
    if kankaType == "":
        print("Not sure what to do with this. The type came in as \"" + cardTypeLine + "\", which failed to parse.")
        continue

    # For all cards, a valid question is: which setting?
    if cardSet in KALADESH_SETS:
        planeLocationID = kaladeshLocationID
        tags.append(kaladeshTagID)
    #TODO: there are quite a few more Ravnica ones
    elif cardSet in (RAVNICA_SETS):
        planeLocationID = ravnicaLocationID
        tags.append(ravnicaTagID)
    elif cardSet in THEROS_SETS:
        planeLocationID = therosLocationID
        tags.append(therosTagID)
    # turns out you can't do if statements inside a constructor, which means this field needs to be validated up here
    if planeLocationID == 0:
        print("Onoez! This card from set "+cardSet+" doesn't seem to match any of the locations on file!")
        continue

    # Having set/acquired all the information we're going to feed to our functions, let's define them.
    #now if we were really doing the thing properly, we'd always have our constructors take arguments and use those arguments in the constructors. right now, we're using global variables, which is a no-no. but I'm not in the mood to do all that typing right now.

    #INFO: the only REQUIRED field for any of these is "name". So, let's not include any fields we're not specifying in the constructor.

    # turns out locationID isn't the same for each entity type, though, so we need to define figuring that out first
    def determineEntryLocation():
        locationDetermined = False
        while locationDetermined == False:
            print("Include a location?")
            locationAnswer = input("Input location ID for custom, Y to use the default location for the plane the card was found on, or N for no location: ")
            locationDetermined = True #give them the benefit of the doubt
            if locationAnswer.lower() == "n":
                print("Understood. No location will be specified.")
                chosenLocation = 0
            elif locationAnswer.lower() == "y":
                chosenLocation = planeLocationID
            elif locationAnswer.isdecimal():
                chosenLocation = int(locationAnswer)
            else:
                print("That wasn't one of the options. Maybe you made a typo or something?")
                locationDetermined = False #this will cause the While loop to restart

        return chosenLocation

    def createKankaCharacter():
        # these need to be initialized every time, hence them being defined here
        # incoming data includes: tags[], cardName, cardFlavor, cardImgurl, cardSubtype
        personalityName=["Attitude", "Values", "Accent", "Renown"] #we might want to change that per-card later
        personalityEntry=["Unknown", "Unknown", "Unknown", "Unknown"] #ditto
        race=""
        raceID = 0
        charTitle = ""  # @UnusedVariable (not really, I just don't trust it to re-initialize properly otherwise)
        charType = ""

        # The first word of the creature subtype has a decent chance of being the race, with one exception
        if cardType == "Artifact Creature":
            raceCandidate = "Construct"
        else:
            raceCandidate = cardSubtype.split(" ")[0]
        if raceCandidate == "Elven":
            raceCandidate = "Elf"
        if raceCandidate in raceIDs: #else leave both race and raceID empty
            race = raceCandidate
            raceID = raceIDs[race]

        # replacing "" with "" should be no problem if we didn't find a race
        charTitle = cardSubtype.replace(race, "", 1).strip()
        if debug:
            print(cardType)
            print(cardSubtype, "-->", raceCandidate, "-->", race, ": ", raceID)
            print(charTitle)
            input()

        while charType == "":
            charTypeResponse = input("Character type? M for Model, I for Individual (awaiting customization), anything else will be input directly: ")
            if charTypeResponse.lower() == "m":
                charType = "Model"
            elif charTypeResponse.lower() == "i":
                charType = "Individual"
            #elif charTypeResponse.lower() == "p": charType = "NPC"
            #else: print("seriously it really has to be m or i")
            else:
                charType = charTypeResponse
            # end loop - successfully setting charType moves on

        kankaCharacter = {
            "name" : cardName,
            "title": charTitle,
        #    "age" : "",
        #    "sex" : "",
            "entry" : cardFlavor + "<p>Behavior so far: None</p><br><br><small>Artist Credit: "+cardArtist+"</small>",
            "type" : charType,
        #    "family_id" : "",
            "tags" : tags,
            "is_dead" : False,
            "is_private" : False,
            "image_url" : cardImgurl,
            "personalityName" : personalityName,
            "personalityEntry" : personalityEntry
            }
        if raceID > 0:
            kankaCharacter.update({"race_id" : raceID})
        entryLocation = determineEntryLocation()
        if entryLocation > 0:
            kankaCharacter.update({"location_id":entryLocation})
        return kankaCharacter

    # now on to items

    def createKankaItem():
        kankaItem = {
            "name" : cardName,
            "entry" : cardFlavor + "<br><br><small>Artist Credit: "+cardArtist+"</small>",
        #    "character_id" : , # int - the item's owner
            "tags" : tags,
            "is_private" : False,
            "image_url" : cardImgurl
            }
        if cardSubtype != "":
            kankaItem.update({"type":cardSubtype})
        entryLocation = determineEntryLocation()
        if entryLocation > 0:
            kankaItem.update({"location_id":entryLocation})
        return kankaItem

    def createKankaLocation():
        kankaLocation = {
            "name" : cardName,
            "entry" : cardFlavor + "<br><br><small>Artist Credit: "+cardArtist+"</small>",
            "tags" : tags,
            "is_private" : False,
            "image_url" : cardImgurl,
            }
        if cardSubtype != "":
            kankaLocation.update({"type":cardSubtype})
        entryLocation = determineEntryLocation()
        if entryLocation > 0:
            kankaLocation.update({"parent_location_id":entryLocation})
        return kankaLocation

    #let's call some functions
    if kankaType == "Character":
        kankaPayload = createKankaCharacter()
        kanka_request_URL = KANKA_CHAR_URL
    elif kankaType == "Location":
        kankaPayload = createKankaLocation()
        kanka_request_URL = KANKA_LOC_URL
    elif kankaType == "Item":
        kankaPayload = createKankaItem()
        kanka_request_URL = KANKA_ITEM_URL
    

    # PUSH THE BIG RED BUTTON
    if weAreLive: #I'm gone, baby, solid gone.
        print("Submitting...") #acknowledge slight delay
        postResult = requests.post(kanka_request_URL, headers=kankaHeaders, json=kankaPayload)
        # So, how did it gooooooooo?
        print(postResult.status_code, postResult.reason)
        if postResult.ok:
            print(postResult.text)
    else: # NOT YET BALOO
        print(kanka_request_URL)
        print(kankaHeaders)
        print(kankaPayload)
#        kankaJSON = kankaResult.json()
#        kankaContents = kankaJSON["data"]
#        for x in kankaContents:
#            print(x, kankaContents[x])
    #wheee! let's do it again!
    continue
    # TODO: some kind of condition for not doing it again I guess
    # break
    #end of program main loop
