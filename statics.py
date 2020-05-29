''' we got a whole bunch of static ids up in here...why not do the thing up right?

Riffing on the suggestions from https://www.programiz.com/python-programming/variables-constants-literals

ATM, this module is proposed, and not in production
'''

# API URLs
KANKA_URL = "https://kanka.io/api/1.0/campaigns/24183/"
SCRYFALL_URL = "https://api.scryfall.com/cards/search?q="

KANKA_CHAR_URL = KANKA_URL+"characters" #no slash, cap'n
KANKA_ITEM_URL = KANKA_URL+"items"
KANKA_LOC_URL = KANKA_URL+"locations"

# Locations
KALADESH_LOC = 174953
RAVNICA_LOC = 174971
THEROS_LOC = 176830

# Tags
KALADESH_TAG = 54084
RAVNICA_TAG = 54085
THEROS_TAG = 54177
KANKFALL_TAG = 55903

# Races
RACES = {"Aetherborn":67177, "Centaur":67037, "Construct":68699, "Dwarf":67077, "Elf":67493, "Goblin":66961, "Human":66977, "Vedalken":66954}

# Card sets
RAVNICA_SETS = ("Ravnica: City of Guilds", "Guildpact", "Dissension", "Return to Ravnica", "Guilds of Ravnica", "Ravnica Allegiance", "War of the Spark", "Gatecrash", "Dragon’s Maze", "Duel Decks: Izzet vs. Golgari", "Guilds of Ravnica Mythic Edition", "Ravnica Allegiance Mythic Edition", "War of the Spark Mythic Edition", "Guilds of Ravnica Guild Kits", "Ravnica Allegiance Guild Kits")
KALADESH_SETS = ("Kaladesh", "Aether Revolt", "Masterpiece Series: Kaladesh Inventions")
THEROS_SETS = ("Theros", "Born of the Gods", "Journey into Nyx", "Theros Beyond Death")

# Pronouns
PRONOUNS = ("they/them","she/her","he/him","it/its")
