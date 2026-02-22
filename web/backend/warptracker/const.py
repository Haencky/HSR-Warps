import os

WIKI_URL = 'https://honkai-star-rail.fandom.com/wiki/'
PRYDWEN_CHAR = 'https://www.prydwen.gg/page-data/star-rail/characters/'
PRYDWEN_LC = 'https://www.prydwen.gg/page-data/star-rail/light-cones/page-data.json'
IMAGE_URL = 'https://raw.githubusercontent.com/Mar-7th/StarRailRes/master/'
ITEM_ID_URL = 'https://haencky.github.io/HSR-Warps/itemIDs.json'
SIZE = 10000

GACHA_TYPES = {
    "de-de": {
        1: "Stellarwarp",
        2: "Startwarp",
        11: "Figuren-Aktionswarp",
        12: "Lichtkegel-Aktionswarp",
        21: "Figuren-Kollaborationswarp",
        22: "Lichkegel-Kollabaritionswarp"
    },
    "en-us": {
        1: 'Stellar Warp',
        2: 'Departure Warp',
        11: 'Character Event Warp',
        12: 'Light Cone Event Warp',
        21: 'Character Collaboration Warp',
        22: 'Light Cone Collaboration Warp',
    },
    "fr-fr": {
        1: "Saut stellaire",
        2: "Saut hyperespace de départ",
        11: "Événement hyperespace de personnage",
        12: "Événement hyperespace de cône de lumière",
        21: "Saut de collaboration de personnage",
        22: "Saut de collaboration de cône de lumière"
    }, 
    "pt-pt": { # Portuguese
        1: "Salto Hiperespacial Estelar",
        2: "Salto Hiperespacial de Partida",
        11: "Salto Hiperespacial de Evento de Personagem",
        12: "Salto Hiperespacial de Evento de Cone de Luz",
        21: "Salto Hiperespacial de Colaboração de Personagem",
        22: "Salto Hiperespacial de Colaboração de Cone de Luz"
    }, 
    "es-es": {
        1: "Salto estelar",
        2: "Salto de partida",
        11: "Salto de evento de personaje",
        12: "Salto de evento de cono de luz",
        21: "Salto de colaboración de personaje",
        22: "Salto de colaboración de cono de luz"
    },
    "ru-ru": {
        1: "Звёздный прыжок",
        2: "Отправной прыжок",
        11: "Прыжок события: Персонаж",
        12: "Прыжок события: Световой конус",
        21: "Совместный Прыжок события: Персонаж",
        22: "Совместный Прыжок события: Световой конус"
    },
    "th-th": {
        1: "วาร์ปสู่ดวงดาว",
        2: "ก้าวแรกแห่งการวาร์ป",
        11: "กิจกรรมวาร์ปตัวละคร",
        12: "กิจกรรมวาร์ป Light Cone",
        21: "กิจกรรมวาร์ปตัวละครคอลแลบ",
        22: "กิจกรรมวาร์ป Light Cone คอลแลบ"
    },
    "vi-vn": {
        1: "Bước Nhảy Chòm Sao",
        2: "Bước Nhảy Đầu Tiên",
        11: "Bước Nhảy Sự Kiện Nhân Vật",
        12: "Bước Nhảy Sự Kiện Nón Ánh Sáng",
        21: "Bước Nhảy Nhân Vật Hợp Tác",
        22: "Bước Nhảy Nón Ánh Sáng Hợp Tác"
    },
    "id-id": {
        1: "Warp Bintang-Bintang",
        2: "Warp Keberangkatan",
        11: "Event Warp Karakter",
        12: "Event Warp Light Cone",
        21: "Warp Kolaborasi Karakter",
        22: "Warp Kolaborasi Light Cone"
    },
    "ja-jp": {
        1: "群星跳躍",
        2: "始発跳躍",
        11: "イベント跳躍・キャラクター",
        12: "イベント跳躍・光円錐",
        21: "コラボ跳躍・キャラクター",
        22: "コラボ跳躍・光円錐"
    },
    "ko-kr": {
        1: "뭇별의 워프",
        2: "초행길 워프",
        11: "캐릭터 이벤트 워프",
        12: "광추 이벤트 워프",
        21: "캐릭터 콜라보 워프",
        22: "광추 콜라보 워프"
    },
    "zh-tw": {  # chinese traditional writing
        1: "群星躍遷",
        2: "始發躍遷",
        11: "角色活動躍遷",
        12: "光錐活動躍遷",
        21: "角色聯動躍遷",
        22: "光錐聯動躍遷"
    },
    "zh-cn": {  # chinese simplified
        1: "群星跃迁",
        2: "始发跃迁",
        11: "角色活动跃迁",
        12: "光锥活动跃迁",
        21: "角色联动跃迁",
        22: "光锥联动跃迁"
    }
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

PLURALS = [ # prydwen uses a plural on these light cones
    'Lingering Tear'
]

SPECIALS = { # items with different spelling in prydwen
    'Evernight': 'march-7th-evernight',
}