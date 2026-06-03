# Copyright (C) 2026 Haencky
# SPDX-License-Identifier: GPL-3.0-or-later
from .models import Path, Item, ItemType, GachaType, Banner
from .const import LOST, SIZE, WIKI_URL, IMAGE_URL, GACHA_TYPES, SPECIALS, COUNT_4_S_C, FRIBBELS_DATA
from .serializers import *
import time
from urllib.parse import urlparse, urlunparse, urlencode, parse_qs
from django.utils.timezone import make_aware
from django.core.files.images import ImageFile
import requests
from datetime import datetime
from io import BytesIO
from .models import Warp as W
import pandas as pd
import numpy as np

class WarpAnalyser():
    def __init__(self, warps:list=None, index:list=None):
        self.df = pd.DataFrame(warps, index=index)
        self.df['item_id__image'] = self.df['item_id__image'].apply(lambda x: f'/media/{x}')
        self.data = {}

        for g in GachaType.objects.all():
            b_data = self.df[self.df['gacha_id__gacha_type'] == g.id]
            self.data[g.gacha_type] = self.process_banner(b_data, g)

    def process_banner(self, group: pd.DataFrame, g_id: GachaType):
        five_stars: pd.DataFrame = group[group['item_id__rarity'] == 5].copy()
        five_stars['is_loss'] = five_stars['item_id__item_id'].isin(LOST).astype(bool)
        w_n_l = []
        is_g = False

        for _, row in five_stars.iterrows():
            if not is_g:
                w_n_l.append(int(not row['is_loss']))
                if row['is_loss']:
                    is_g = True
            else:
                is_g = False
        wr = np.mean(w_n_l) if w_n_l else 0.5 # asume 50/50
        if g_id.gacha_type == 1 or g_id.gacha_type == 2:
            wins = five_stars
        else:
            wins = five_stars[five_stars['is_loss'] == False] if not five_stars.empty else None
        if wins is not None and not wins.empty:
            last_win = wins.iloc[-1]
        last_5s = five_stars.iloc[-1] if not five_stars.empty else None
        if last_5s is not None:
            pity = int(group[group['warp_id'] > last_5s['warp_id']].shape[0])
            warranted = bool(last_5s['is_loss'])
        else:
            pity = group.shape[0]
            warranted = False
        avg_pity = five_stars['pity'].median()
        avg_pity = avg_pity if not np.isnan(avg_pity) else 75

        return {
            'name': g_id.name,
            'limited': len(five_stars[five_stars['is_loss'] == False].value_counts()),
            'pity': pity,
            'gacha_type': g_id.gacha_type,
            'warranted': warranted,
            'wr': round(100 * wr, 2),
            'avg_pity': round(avg_pity, 1),
            'c': group.shape[0],
            'id': g_id.id,
            'last_win': last_win.to_dict() if last_5s is not None else None,
            'max_pity': g_id.max_pity,
        }
    
    def per_type(self):
        return [v for _,v in self.data.items()]
    
    def monte_carlo(self, targets: dict, available_pulls:int, collab:bool, fours:int):
        """
        Approximates the results of 100000 pulling characters and lcs

        Params:
            targets(dict): all infos including item and count
            available_pulls(int): amount of pulls available (at the beginning)
            collab(bool): based on collaboration data
            fours(int): amount of 4 star characters at max eidola
        """
        a = [key for key, value in targets.items() if value['copies'] < 1]
        if len(a) > 1 or available_pulls == 0:
            return None
        if not collab:
            start_pity = {
                "character": {
                    "pity_5": self.data[11]['pity'],
                    "guranteed": self.data[11]['warranted']
                }, "lightcone": {
                    "pity_5": self.data[12]['pity'],
                    "guranteed": self.data[12]['warranted']
                }
            }
        else:
            start_pity = {
                "character": {
                    "pity_5": self.data[21]['pity'],
                    "guranteed": self.data[21]['warranted']
                }, "lightcone": {
                    "pity_5": self.data[22]['pity'],
                    "guranteed": self.data[22]['warranted']
                }
            }

        banner_config = {
            "characters": {
                'base_rate': 0.006,
                'hard_pity': 90,
                'featured_rate': 0.5,
                'soft_pity_start': 74
            },
            "lightcones": {
                'base_rate': 0.008,
                'hard_pity': 80,
                'featured_rate': 0.75,
                'soft_pity_start': 66
            }
        }

        OWNED_4STAR_RATE = fours / COUNT_4_S_C
        BASE_4_RATE = 0.055
        HARD_PITY_4 = 10

        def five_star_rate(pity: int, config:dict):
            if pity < config['soft_pity_start']:
                return config['base_rate']
            extra = (pity - config['soft_pity_start'] + 1) * 0.06
            return min(config['base_rate']+extra, 1)
        
        def simulate_banner_pull(state:dict, config:dict):
            state['pity_5'] += 1
            state['pity_4'] += 1

            refunds = 0
            undying_starlight = 0
            featured = False

            rate_5 = five_star_rate(state['pity_5'], config)

            got_5 = state['pity_5'] >= config['hard_pity'] or np.random.random() < rate_5

            if got_5:
                state['pity_5'] = 0
                state['pity_4'] = 0

                if state['guranteed'] or np.random.random() < config['featured_rate']:
                    featured = True
                    state['guranteed'] = False
                else:
                    state['guranteed'] = True
                
                if np.random.random() < 0.3: # approx
                    refunds += 2
                    undying_starlight += 40
                return featured, refunds, undying_starlight
        
            got_4 = state['pity_4'] >= HARD_PITY_4 or np.random.random() < BASE_4_RATE

            if got_4:
                state['pity_4'] = 0
                is_character = np.random.random() < 0.5
                if is_character:
                    if np.random.random() < OWNED_4STAR_RATE:
                        refunds += 1
                        undying_starlight += 20
                    else:
                        refunds += 0.4
                        undying_starlight += 8
            return featured, refunds, undying_starlight

        def simulate_run():
            pulls = float(available_pulls)
            banner_states = {
                "characters": {
                    "pity_5": start_pity['character']['pity_5'],
                    "pity_4": 0,
                    "guranteed": start_pity['character']['guranteed']
                },
                "lightcones": {
                    "pity_5": start_pity['lightcone']['pity_5'],
                    "pity_4": 0,
                    "guranteed": start_pity['lightcone']['guranteed']
                }
            }

            obtained = {key: targets[key]['obtained'] for key in targets}
            undying_starlight = 0
            total_pulls = 0

            while int(pulls) > 0:
                remaining_targets = [key for key, value in targets.items() if obtained[key] < value['copies']]
                if not remaining_targets:
                    break
                current_target = remaining_targets[0]
                banner_type = targets[current_target]['banner']
                featured, refunds, gained_undying_starlight = simulate_banner_pull(banner_states[banner_type], banner_config[banner_type])
                pulls -= 1
                pulls += refunds
                total_pulls += 1
                undying_starlight += gained_undying_starlight

                if featured:
                    obtained[current_target] += 1
            result = {
                **obtained,
                "undying_starlight": undying_starlight,
                "total_pulls": total_pulls,
            }

            return result
        results = [simulate_run() for _ in range(10_000)]
        df = pd.DataFrame(results)
        return df

class Warp():
    """
    Support Class for information obtained from HSR API

    Args:
        uid(int): uid
        gacha_id(int): reference to banner
        item_id(int): item obtained
        item_type(str): LC or Character
        en_type(str): english name of type
        time(time): timestamp
        name(str): name of item
        en_name(str): english name of item
        rarity(int): rarity of item
        id(int): id of warp 
        gacha_type(int): gacha_type
        lang(str): language
    """

    def __init__(self,  item_id:int, name:int, rarity:int, en_name:int, lang:str, en_type:int, gacha_type:int,  uid:int = None, gacha_id:int = None, item_type:int=None, time:datetime.date=None, id:int=None):
        self.uid = uid
        self.gacha_id = gacha_id
        self.item_id = item_id
        self.item_type = item_type
        self.time = time
        self.name = name
        self.id = id
        self.rarity = rarity
        self.en_type = en_type
        self.en_name = en_name
        self.gacha_type = gacha_type
        self.lang = lang


    def __str__(self):
        return self.name

class _Item():
    """
    Supporting class for items
    """

    def __init__(self, id:int, name:str, type:str):
        self.id = id
        self.name = name
        self.type = type

    def __hash__(self):
        return self.id
    
    def __eq__(self, value):
        return self.id == value.id

def getSpecials():
    try:
        r = requests.get(SPECIALS)
    except requests.RequestException:
        print('Could not fetch Specials')
        return None
    if r.status_code == 200:
        data = r.json()
        return data
    else:
        print('invalid status code for specials')
        return None

def getData() -> dict:
    """
    Fetches all data from fribbles data.json
    """
    try:
        r = requests.get(FRIBBELS_DATA)
    except requests.RequestException:
        print('Could not fetch fribbles data')
        return None
    if r.status_code == 200:
        data = r.json()
        return data
    else:
        print("Invalid status code")
        return None

def fetch_info(url:str, gacha_type: int, data_fribbles: dict) -> dict:
    """
    Fetches info from HSR Api

    Params: 
        url(str): base url including authkey
        gacha_type(int): gacha type (e.g. 11 for event character)
        lcdata(dict): dictionary for all light cones
        special_data(dict): dictionary for all special written characters/lcs in prydwen
    """
    update_all()
    parsed = urlparse(url)
    query_dict = parse_qs(parsed.query)

    query_dict['gacha_type'] = [gacha_type] # set gacha type
    query_dict['size'] = [SIZE] # set size to SIZE
    new_query = urlencode(query_dict, doseq=True)
    url = urlunparse(parsed._replace(query=new_query))

    def _check_item(id:int):
        """
        Checks if item already exists
        """
        return Item.objects.filter(pk=id).exists()
    
    def _add_warp(warp: Warp, current_pity:int) -> bool:
        """
        Adds a new warp to the database

        Params:
            warp(Warp): warp obtained by the API
            current_pity(int): pity of last object of this banner

        Returns:
            True if current pull is 5 star; false else
        """

        # get gacha type or create
        gacha_type = warp.gacha_type
        if not GachaType.objects.filter(gacha_type=gacha_type).exists():
            try:
                name = GACHA_TYPES[warp.lang][gacha_type]
            except KeyError:
                name = GACHA_TYPES['en'][gacha_type]
            GachaType.objects.create(
                gacha_type=gacha_type,
                name=name
            )
        gacha_type = GachaType.objects.get(gacha_type=gacha_type)

        # get banner or create
        if not Banner.objects.filter(gacha_id=warp.gacha_id).exists():
            Banner.objects.create(
                gacha_id = warp.gacha_id,
                gacha_type=gacha_type,
            )
        banner_id = Banner.objects.get(gacha_id=warp.gacha_id)

        item = Item.objects.get(item_id=warp.item_id)

        W.objects.create(
            warp_id = warp.id,
            uid = warp.uid,
            gacha_id = banner_id,
            item_id = item,
            time=make_aware(datetime.strptime(warp.time, "%Y-%m-%d %H:%M:%S")),
            pity=current_pity,
        )
        if item.rarity == 5:
            return True
        return False
    
    def create_item(warp: Warp):
        """
        Creates a new entry in item model

        Params:
            warp(Warp): Warp with given information
        """

        def _scrape_info(name: str, type: str, id:int) -> dict:
            """
            Scrapes Honkai Starrail Wiki for images, infos and wiki link\n
            Download images if necessary\n
            Creates new entries for path model if necessary        

            Params:
                name(str): english name of item
                type(int): type of item; hsr wiki uses different classes for types
                id(int): item id

            Returns:
                ret(dict): dictionary with image path and foreign key to path (e.g. 1 for hunt)
            """
            img_name = ''

            if type == 'Light Cone':
                #img_name = 'light_cones/'
                path = data_fribbles['lightCones'][id]['path']
                img_link = IMAGE_URL + 'image/light_cone_'
            else:
                #img_name = 'characters/'
                path = data_fribbles['characters'][id]['path']
                img_link = IMAGE_URL + 'image/character_'
            
            # download image
            img_name += f'{name}.png'
            try:
                fetch_img = requests.get(f'{img_link}portrait/{id}.png') # fetch image
                if fetch_img.status_code == 200:
                    image_bytes = BytesIO(fetch_img.content) # save to byte stream
                    django_file = ImageFile(image_bytes, name=img_name)
                else:
                    print(f'Could not fetch image for {name}')
            except requests.RequestException:
                print(f'Could not fetch image for {name}')

            display_path = path 
            if path == 'Hunt':
                display_path = f'The {path}' # compatibility with current dbs

            # if path does not exist yet in db
            if not Path.objects.filter(name=display_path).exists():
                # Fetch image
                icon_url = f'{IMAGE_URL}icon/path/{path}.png'
                get_icon_req = requests.get(icon_url)

                path_bytes = BytesIO(get_icon_req.content)
                path_image_file = ImageFile(path_bytes, name=f'{path}.png')

                Path.objects.create(
                    name=display_path,
                    icon=path_image_file
                )
            path_id = Path.objects.filter(name=display_path).first()


            return {'image': django_file, 'path': path_id}

        def _create_itemtype(typname:str):
            ItemType.objects.create(
                name=typname
            )

        if not ItemType.objects.filter(name=warp.item_type).exists():
            _create_itemtype(typname=warp.item_type)

        item_type = ItemType.objects.filter(name=warp.item_type).first()
        scraped = _scrape_info(name=warp.en_name, type=warp.en_type, id=warp.item_id)
        path_fk = scraped['path']
        img_path = scraped['image']
        wiki_r = str(warp.en_name).replace(' ', '_')
        wiki = f'{WIKI_URL + wiki_r}'

        Item.objects.create(
            item_id = warp.item_id,
            name = warp.name,
            typ = item_type,
            image = img_path,
            path = path_fk,
            wiki = wiki,
            rarity = warp.rarity,
            eng_name = warp.en_name,
        )
        print(f'Created item {warp.item_id} - {warp.name}')

    def _fetch_en(url) -> dict:
        """
        Fetches english names and returns an dictionary

        Params:
            url(str): url to hsr api

        Returns:
            mapping(dict): a dictionary mapping item ids to engllish names and types
        """
        parsed = urlparse(url)
        query_dict = parse_qs(parsed.query)
        query_dict['lang'] = ['en'] # set language to english
        new_query = urlencode(query_dict, doseq=True)
        url = urlunparse(parsed._replace(query=new_query))

        warps = requests.get(url).json()['data']['list'] # request all warps

        items = []
        for warp in warps:
            items.append(_Item(int(warp['item_id']), warp['name'], warp['item_type']))

        _items = list(set(items))
        return {item.id: {'name': item.name, 'type': item.type} for item in _items}
    
    en_items = _fetch_en(url)
    try:
        last_warp = W.objects.filter(gacha_id__gacha_type__gacha_type=gacha_type).latest('warp_id')
    except:
        last_warp = None

    def _fetch(url):
        """
        Fetches all infos from given gacha_type

        Params:
            urL(str): url to HSR Api
        """
        counter = 0
        current_pity = last_warp.pity if last_warp else 0
        try:
            warps = requests.get(url).json()['data']['list'] # request all warps
        except (requests.RequestException, TypeError):
            warps = None
        if warps:
            l = W.objects.filter(uid=warps[0]['uid'], gacha_id__gacha_type__gacha_type=gacha_type).values_list('warp_id', flat=True)
            last = list(l)
            for warp in warps[::-1]:
                if int(warp['id']) in last:
                    continue
                item_id = int(warp['item_id'])
                w = Warp(
                    item_id=warp['item_id'],
                    name=warp['name'],
                    rarity=warp['rank_type'],
                    uid=warp['uid'],
                    gacha_id=warp['gacha_id'],
                    item_type=warp['item_type'],
                    en_type=en_items[item_id]['type'],
                    en_name=en_items[item_id]['name'],
                    time=warp['time'],
                    id=warp['id'],
                    gacha_type=gacha_type,
                    lang=warp['lang']
                )

                if not _check_item(item_id):
                    create_item(w)
                
                if int(w.id) not in last:
                    counter += 1
                    if _add_warp(w, current_pity): # returns True if last pull was a 5 star
                        current_pity = 0
                    current_pity+=1
                time.sleep(0.1)
            return counter
        else:
            return 0
    fetched = _fetch(url)
    return fetched

def check_banner():
    """
    Tries to match an item to a banner
    """
    for b in Banner.objects.exclude(item_id__isnull=False).exclude(gacha_type__gacha_type=1):
        w = W.objects.filter(gacha_id=b.id, item_id__rarity=5).exclude(item_id__in=LOST)
        if w:
            item = w[0].item_id
            b.item_id = item
            b.save()

def update_image(item: Item):
    item_id = item.item_id
    img_link = IMAGE_URL + 'image/light_cone_' if item_id >= 20_000 else IMAGE_URL + 'image/character_' # ids 20000+ are LCs
    img_name = f'{item.eng_name}.png'
    name = item.name

    try:
        fetch_img = requests.get(f'{img_link}portrait/{item_id}.png') # fetch image
        if fetch_img.status_code == 200:
            image_bytes = BytesIO(fetch_img.content) # save to byte stream
            django_file = ImageFile(image_bytes, name=img_name)
            item.image = django_file
            item.save()
        else:
            print(f'Could not fetch image for {name}')
    except requests.RequestException:
        print(f'Could not fetch image for {name}')

def update_all() -> list:
    """
    updates all images
    """
    missing = Item.objects.filter(image='')
    for x in missing:
        update_image(x)
    return [m.name for m in missing]