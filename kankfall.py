'''
Created on May 27, 2020

@author: ElectricalAptitude
@author: zschuetz

@change 2020.05.27 zschuetz ported from https://repl.it/@ElectricalAptit/kankfall#main.py so as to test Kanka interactions without making the API key quite so public.
# credit for "do you even POST, bro?" goes to https://www.w3schools.com/python/ref_requests_post.asp
'''

import requests
from builtins import int
# import other stuff??

# important test cases: gibberish, forest, Arcbound Ravager, Baral, snow-covered swamp, Armor of Faith, Kaervek's Torch
# bluh bluh python doesn't support multiline comments

#set program constants
debug = True
weAreLive = True
kankaURL = "https://kanka.io/api/1.0/campaigns/24183/"
scryfallURL = "https://api.scryfall.com/cards/"
#don't do magic numbers kids they're bad for you
kaladeshLocationID = 174953
ravnicaLocationID = 174971
therosLocationID = 176830
kaladeshTagID = 54084
ravnicaTagID = 54085
therosTagID = 54177
kankfallTagID = 55903
raceIDs = {"Aetherborn":67177, "Construct":68699, "Dwarf":67077, "Elf":67493, "Human":66977, "Vedalken":66954}
#TODO: moar races!

ravnicaSets = ("Ravnica: City of Guilds", "Guildpact", "Dissension", "Return to Ravnica", "Guilds of Ravnica", "Ravnica Allegiance", "War of the Spark", "Gatecrash", "Dragon’s Maze", "Duel Decks: Izzet vs. Golgari", "Guilds of Ravnica Mythic Edition", "Ravnica Allegiance Mythic Edition", "War of the Spark Mythic Edition", "Guilds of Ravnica Guild Kits", "Ravnica Allegiance Guild Kits")
kaladeshSets = ("Kaladesh", "Aether Revolt", "Masterpiece Series: Kaladesh Inventions")
therosSets = ("Theros", "Born of the Gods", "Journey into Nyx", "Theros Beyond Death")

kankaCharacterURL = kankaURL+"characters" #no slash, cap'n
kankaItemURL = kankaURL+"items"
kankaLocationURL = kankaURL+"locations"

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
    tags = [kankfallTagID]
    thisURL = ""
    kankaPayload = {}
    postResult = ""

    desiredCardName = input("Type in the name of the card: ") # in python 3, input gives us a str automatically
    desiredCardName = desiredCardName.replace(" ", "+")
    desiredURL = "https://api.scryfall.com/cards/search?q="+desiredCardName+"&unique=prints"

    httpResult = requests.get(desiredURL) #returns a dict with one entry, 'data', whose data is an array of dicts, each of which is one card.
    if httpResult.ok==False:
        print(str(httpResult.status_code)+": "+httpResult.reason)
        continue
    resultJson=httpResult.json()['data'] #so resultJson is an array of some number of dicts
    print("Cards were found from the following sets:")
    currentCardIndex = 0
    for card in resultJson: #card here is now an actual card
        thisCardSet = card["set_name"]
        print("["+str(currentCardIndex)+"]: "+thisCardSet)
        if thisCardSet in ravnicaSets or thisCardSet in kaladeshSets or thisCardSet in therosSets:
            selectedCard = card
            break
        currentCardIndex += 1
    if selectedCard == {}: continue #if no matches, try again
    print("Selected card number "+str(currentCardIndex))
    cardName = selectedCard['name']
    cardSet = selectedCard['set_name']
    cardImgurl = selectedCard['image_uris']['art_crop']
    if "flavor_text" in selectedCard:
        cardFlavor = selectedCard['flavor_text']
    if "artist" in selectedCard:
        cardArtist = selectedCard['artist']
    cardTypeLine = selectedCard['type_line']
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

    #Input's all finished, woo! Now to some business logic, starting with sorting.

    #what manner of beastie are you
    if cardType == "Artifact":
        if cardSubtype == "Vehicle":
            kankaType = "Location"
        else:
            kankaType = "Item"
    if "Creature" in cardType:
        kankaType = "Character"
    if "Land" in cardType :
        kankaType = "Location"
    #quick sanity check
    if kankaType == "":
        print("Not sure what to do with this. The type came in as \"" + cardTypeLine + "\", which failed to parse.")
        continue

    # For all cards, a valid question is: which setting?
    if cardSet in kaladeshSets:
        planeLocationID = kaladeshLocationID
        tags.append(kaladeshTagID)
    #TODO: there are quite a few more Ravnica ones
    elif cardSet in (ravnicaSets):
        planeLocationID = ravnicaLocationID
        tags.append(ravnicaTagID)
    elif cardSet in therosSets:
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
        personalityName=['Attitude', 'Values', 'Accent', 'Renown'] #we might want to change that per-card later
        personalityEntry=['Unknown', 'Unknown', 'Unknown', 'Unknown'] #ditto
        race=""
        raceID = 0
        charTitle = ""
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
            'name' : cardName,
            'title': charTitle,
        #    'age' : '',
        #    'sex' : '',
            'entry' : cardFlavor + "<p>Behavior so far: None</p><br><br><small>Artist Credit: "+cardArtist+"</small>",
            'type' : charType,
        #    'family_id' : '',
            'tags' : tags,
            'is_dead' : False,
            'is_private' : False,
            'image_url' : cardImgurl,
            'personalityName' : personalityName,
            'personalityEntry' : personalityEntry
            }
        if raceID > 0:
            kankaCharacter.update({'race_id' : raceID})
        entryLocation = determineEntryLocation()
        if entryLocation > 0:
            kankaCharacter.update({"location_id":entryLocation})
        return kankaCharacter

    # now on to items


    def createKankaItem():
        kankaItem = {
            'name' : cardName,
            'entry' : cardFlavor + "<br><br><small>Artist Credit: "+cardArtist+"</small>",
        #    'character_id' : , # int - the item's owner
            'tags' : tags,
            'is_private' : False,
            'image_url' : cardImgurl
            }
        if cardSubtype != "":
            kankaItem.update({"type":cardSubtype})
        entryLocation = determineEntryLocation()
        if entryLocation > 0:
            kankaItem.update({"location_id":entryLocation})
        return kankaItem

    def createKankaLocation():
        kankaLocation = {
            'name' : cardName,
            'entry' : cardFlavor + "<br><br><small>Artist Credit: "+cardArtist+"</small>",
            'tags' : tags,
            'is_private' : False,
            'image_url' : cardImgurl,
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
        thisURL = kankaCharacterURL
    elif kankaType == "Location":
        kankaPayload = createKankaLocation()
        thisURL = kankaLocationURL
    elif kankaType == "Item":
        kankaPayload = createKankaItem()
        thisURL = kankaItemURL


    # PUSH THE BIG RED BUTTON
    if weAreLive: #I'm gone, baby, solid gone.
        print("Submitting...")
        postResult = requests.post(thisURL, headers=kankaHeaders, json=kankaPayload)
        # So, how did it gooooooooo?
        print(postResult.status_code, postResult.reason)
        if postResult.ok:
            print(postResult.text)
    else: # NOT YET BALOO
        print(thisURL)
        print(kankaHeaders)
        print(kankaPayload)
#        kankaResult = requests.get(kankaCharacterURL+"/182217", headers=kankaHeaders)
#        print(str(kankaResult.status_code)+": "+kankaResult.reason)
#        kankaJSON = kankaResult.json()
#        kankaContents = kankaJSON["data"]
#        for x in kankaContents:
#            print(x, kankaContents[x])
    #wheee! let's do it again!
    continue
    # TODO: some kind of condition for not doing it again I guess
    # break
    #end of program main loop
