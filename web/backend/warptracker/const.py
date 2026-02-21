import environ
env = environ.Env()

WIKI_URL = 'https://honkai-star-rail.fandom.com/wiki/'
PRYDWEN_CHAR = 'https://www.prydwen.gg/page-data/star-rail/characters/'
PRYDWEN_LC = 'https://www.prydwen.gg/page-data/star-rail/light-cones/page-data.json'
IMAGE_URL = 'https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/'
ITEM_ID_URL = 'https://haencky.github.io/HSR-Warps/itemIDs.json'
SIZE = 10000

GACHA_TYPES = {
    "de": {
        1: "Stellar Warp",
        2: "Startwarp",
        11: "Figuren-Aktionswarp",
        12: "Lichtkegel-Aktionswarp",
        21: "Figuren-Kollaborationswarp",
        22: "Lichkegel-Kollabaritionswarp"
    },
    "en": {
        1: 'Stellar Warp',
        2: 'Departure Warp',
        11: 'Character Event Warp',
        12: 'Light Cone Event Warp',
        21: 'Character Collaboration Warp',
        22: 'Light Cone Collaboration Warp',
    },
}

# duplicate item names
DOUBLES = [
    'Amber', # also member of ten stonehearts and lc
    'Data Bank' # lc and reference to ingame database
]

LOST = [
    1003, # Himeko
    1004, # Welt
    1101, # Bronya
    1102, # Seele
    1104, # Gepard
    1107, # Clara
    1205, # Blade
    1208, # Fu Xuan
    1209, # Yanqing
    1211, # Bailu

    23000, # Night on the Milky Way
    23002, # Something Irreplaceable
    23003, # But the Battle Isn't Over
    23004, # In the Name of the World
    23012, # Sleep Like the Dead
    23013, # Time Waits for No One
]

ITEM_TYPES = {
    'en': ['Light Cone', 'Character'],
    'de': ['Lichtkegel', 'Figur'],
}

LANG = env.str('LANG', default='en')

PLURALS = [ # prydwen uses a plural on these light cones
    'Lingering Tear'
]

SPECIALS = { # items with different spelling in prydwen
    'Evernight': 'march-7th-evernight',
}