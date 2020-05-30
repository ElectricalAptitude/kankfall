''' 
we got a whole bunch of static ids up in here...why not do the thing up right?

Riffing on the suggestions from https://www.programiz.com/python-programming/variables-constants-literals

@created 2020.05.27 by ElectricAptitude
@change 2020.05.30 SirTechSpec renamed from statics.py to constants.py, set file encoding to UTF-8

'''

# API URLs
SCRYFALL_URL = "https://api.scryfall.com/cards/search?q="
# Ultimately, this one will probably *have* to come from either .cfg or parameters, and the app will fail to load if it can't find it
KANKA_URL = "https://kanka.io/api/1.0/campaigns/24183/"
# These ones should be consistent across user environments, though
KANKA_CHAR_URL = KANKA_URL+"characters" #no slash, cap'n
KANKA_ITEM_URL = KANKA_URL+"items"
KANKA_LOC_URL = KANKA_URL+"locations"

# Locations, tags, and races will be pulled live

# Sets
RAVNICA_SETS = ("Ravnica: City of Guilds", "Guildpact", "Dissension", "Return to Ravnica", "Guilds of Ravnica", "Ravnica Allegiance", "War of the Spark", "Gatecrash", "Dragon's Maze", "Duel Decks: Izzet vs. Golgari", "Guilds of Ravnica Mythic Edition", "Ravnica Allegiance Mythic Edition", "War of the Spark Mythic Edition", "Guilds of Ravnica Guild Kits", "Ravnica Allegiance Guild Kits")
KALADESH_SETS = ("Kaladesh", "Aether Revolt", "Masterpiece Series: Kaladesh Inventions")
THEROS_SETS = ("Theros", "Born of the Gods", "Journey into Nyx", "Theros Beyond Death")
