from .models import Path, Item, ItemType, GachaType, Banner
from .const import LOST, SIZE, WIKI_URL, IMAGE_URL, DOUBLES, GACHA_TYPES, PRYDWEN_CHAR, PRYDWEN_LC, PLURALS ,SPECIALS
from .serializers import *
import time
from urllib.parse import urlparse, urlunparse, urlencode, parse_qs
from django.utils.timezone import make_aware
from django.core.files.images import ImageFile
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django.db.models import Max
from io import BytesIO
from collections import Counter
from .models import Warp as W

class WarpAnalyser():
    @staticmethod
    def warps_per_type():
        types = []
        for g_id in GachaType.objects.all():
            max_pity = g_id.max_pity
            filtered = W.objects.filter(gacha_id__gacha_type=g_id.id)
            amount = filtered.count()
            jade = amount * 160 # 160 jade = 1 Warp
            five_stars = filtered.filter(item_id__rarity=5)
            wins = five_stars.exclude(item_id__item_id__in=LOST)
            last = five_stars.latest('warp_id')
            pity = filtered.filter(warp_id__gt=last.warp_id).count()
            warranted = last.item_id.item_id in LOST # last 5⭐ pull was a 50/50 lost
            winrate = round(wins.count() / five_stars.count(), 2) * 100 # if never lost lost rate would be 1, modulo 1 to remove this
            try:
                last_win = wins.latest('warp_id')
            except:
                pass

            if g_id.gacha_type in (1,2):
                warranted = True
                winrate = None
                last_win = filtered.filter(item_id__item_id__in=LOST).latest('item_id')
            types.append({'name': g_id.name, 'pity': pity, 'warranted': warranted, 'wr': winrate, 'c': amount, 'last_win': WarpSerializer(last_win).data if last_win else None, 'max_pity': max_pity, 'jade': jade, 'id': g_id.id})
        return types
    
    @staticmethod
    def details(id:int) -> dict:
        """
        Returns a detailed info to an specified id

        Params:
            id(int): id of item
        """
        return ItemSerializer(Item.objects.get(item_id=id)).data
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
        self.lang = lang.split("-")[0]


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

def getLCPath(name: str):
    """
    Returns the path of a Light Cone

    Params:
        name(str): name of light cone
    
    Returns:
        path(str): name of Path
    """

    try:
        r = requests.get(PRYDWEN_LC)
    except requests.RequestException:
        print('Could not connect to LCs')
        return None
    if r.status_code == 200:
        data = r.json()['result']['data']['allCharacters']['nodes']
        for lc in data:
            if name in PLURALS:
                if lc['name'].lower() == f'{name}s'.lower():
                    path = lc['path']
                    return path
            else: 
                if lc['name'].lower() == name.lower():
                    path = lc['path']
                    return path

    else:
        print('Invalid status code')
    return None

def fetch_info(url:str, gacha_type: int) -> dict:
    """
    Fetches info from HSR Api

    Params: 
        url(str): base url including authkey
        gacha_type(int): gacha type (e.g. 11 for event character)
        last_id(int): last id pulled
    """
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
    
    def _add_warp(warp: Warp):
        """
        Adds a new warp to the database

        Params:
            warp(Warp): warp obtained by the API
            userid(int): ID of User
        """

        # get gacha type or create
        gacha_type = warp.gacha_type
        if not GachaType.objects.filter(gacha_type=gacha_type).exists():
            GachaType.objects.create(
                gacha_type=gacha_type,
                name=GACHA_TYPES[warp.lang][gacha_type]
            )
        gacha_type = GachaType.objects.get(gacha_type=gacha_type)

        # get banner or create
        if not Banner.objects.filter(gacha_id=warp.gacha_id).exists():
            Banner.objects.create(
                gacha_id = warp.gacha_id,
                gacha_type=gacha_type,
            )
        banner_id = Banner.objects.get(gacha_id=warp.gacha_id)

        W.objects.create(
            warp_id = warp.id,
            uid = warp.uid,
            gacha_id = banner_id,
            item_id = Item.objects.get(item_id=warp.item_id),
            time=make_aware(datetime.strptime(warp.time, "%Y-%m-%d %H:%M:%S")),

        )
    
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
                path = getLCPath(name)
                img_link = IMAGE_URL + 'image/light_cone_'
            else:
                #img_name = 'characters/'
                try:
                    if name in SPECIALS:
                        name = SPECIALS[name]
                    r = requests.get(f'{PRYDWEN_CHAR}{name.replace(' ', '-').lower()}/page-data.json')
                except requests.RequestException:
                    print(f'Error fetching data for {name}')
                if r.status_code == 200:
                    path = r.json()['result']['data']['currentUnit']['nodes'][0]['path']
                img_link = IMAGE_URL + 'image/character_'
            
            # download image
            img_name += f'{name}.png'
            fetch_img = requests.get(f'{img_link}portrait/{id}.png') # fetch image

            image_bytes = BytesIO(fetch_img.content) # save to byte stream
            django_file = ImageFile(image_bytes, name=img_name)

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
                    name=path,
                    icon=path_image_file
                )
            path_id = Path.objects.filter(name=path).first()


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
        wiki = f'{WIKI_URL + warp.en_name}'

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

    def _fetch_uid(url:str):
        for t in GACHA_TYPES['en'].keys():
            parsed = urlparse(url)
            query_dict = parse_qs(parsed.query)
            query_dict['gacha_type'] = [t] # set language to english
            query_dict['size'] = [1]
            new_query = urlencode(query_dict, doseq=True)
            url = urlunparse(parsed._replace(query=new_query))

            r = requests.get(url)
            if r.status_code == 200:
                id = r.json()
                try:
                    id = id['data']['list'][0]['uid']
                except:
                    pass
            time.sleep(0.1)
            return id    

    def _fetch(url):
        """
        Fetches all infos from given gacha_type

        Params:
            urL(str): url to HSR Api
        """
        last = 0
        l = W.objects.filter(uid=_fetch_uid(url), gacha_id__gacha_type__gacha_type=gacha_type).aggregate(last=Max('warp_id'))
        last_ = l.get('last')
        last = last_ if last_ is not None else 0

        counter = 0

        warps = requests.get(url).json()['data']['list'] # request all warps
        for warp in warps:
            if int(warp['id']) < last: # break loop if nothing new is added
                return 0
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
            
            if int(w.id) > last:
                counter += 1
                _add_warp(w)
            time.sleep(0.1)
        return counter
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