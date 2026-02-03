<<<<<<< HEAD:warps/utils.py
from django.db.models import Q, Max
from datetime import datetime
from time import sleep
import requests
from bs4 import BeautifulSoup
from django.utils.timezone import make_aware
from django.core.files.images import ImageFile
from io import BytesIO
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from .const import *
from collections import Counter
import time

from .models import *
from .serializers import *
from .models import Warp as W

"""
Utils for Warps
"""

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
            url = WIKI_URL + name
            if name in DOUBLES:
                url += "_(Light_Cone)"
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')

            img_name = ''

            if type == 'Light Cone':
                #img_name = 'light_cones/'
                path = soup.find('div', attrs={'class': 'pi-item pi-data pi-item-spacing pi-border-color', 'data-source': 'effect_path'}).find('div', attrs={'class': 'pi-data-value pi-font'}).find('a').text
                img_link = IMAGE_URL + 'light_cone_'
            else:
                #img_name = 'characters/'
                path = soup.find('div', attrs={'class': 'pi-item pi-data pi-item-spacing pi-border-color', 'data-source': 'path'}).find('div', attrs={'class': 'pi-data-value pi-font'}).find('a')['title']
                img_link = IMAGE_URL + 'character_'

            # download image
            img_name += f'{name}.png'
            fetch_img = requests.get(f'{img_link}portrait/{id}.png') # fetch image

            image_bytes = BytesIO(fetch_img.content) # save to byte stream
            django_file = ImageFile(image_bytes, name=img_name)

            # if path does not exist yet in db
            if not Path.objects.filter(name=path).exists():
                # Fetch image
                path_response = requests.get(f'{WIKI_URL + path}')
                path_soup = BeautifulSoup(path_response.content, 'html.parser')

                icon_image_link = path_soup.find('figure', attrs={'data-source': 'image', 'class': 'pi-item pi-image'}).find('a')['href']
                icon_image_name = icon_image_link.split('/')[7]
                get_icon_req = requests.get(icon_image_link)

                path_bytes = BytesIO(get_icon_req.content)
                path_image_file = ImageFile(path_bytes, name=icon_image_name)

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

class WarpAnalyser():
    """
    Analyse all warps
    """
    @staticmethod  
    def warps_per_type(is_api: bool) -> dict:
        """
        Returns amount of warps for all gacha_types

        Returns:
            types(dict): mapping of each type to amount of warps
        """
        types = {}
        for g_id in GachaType.objects.all():
            max_pity = g_id.max_pity
            filtered = W.objects.filter(gacha_id__gacha_type=g_id.id)
            amount = filtered.count()
            jade = amount * 160 # 160 jade = 1 Warp
            euro = round(amount * 2.64, 2) # 2.64€ per warp
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

            if is_api:
                types[f'{g_id.name}'] = {'pity': pity, 'warranted': warranted, 'wr': winrate, 'c': amount, 'last_win': WarpSerializer(last_win).data if last_win else None, 'max_pity': max_pity, 'jade': jade, 'euro': euro, 'id': g_id.id}
            else:
                types[f'{g_id.name}'] = {'pity': pity, 'warranted': warranted, 'wr': winrate, 'c': amount, 'last_win': last_win, 'max_pity': max_pity, 'jade': jade, 'euro': euro, 'id': g_id}
        return types

    def warps_per_banner(self) -> dict:
        """
        Returns amount of warps for each banner

        Returns:
            banner(dict): mapping of each banner to amount of warps
        """
        banners = {}
        for b in Banner.objects.all():
            items = W.objects.filter(gacha_id=b.id)
            
            banners[f'{b.item_id}'] = {'warps': items}
        return banners

    def characters(self) -> dict:
        """
        Maps amount of characters for idola information
        """
        character_id = ItemType.objects.filter(name=ITEM_TYPES[f'{LANG}'][1]).first() # get name of item type for character
        filtered = W.objects.filter(item_id__typ=character_id.id)

        eidola = Counter(f.item_id for f in filtered)
        characters = {}
        for c in eidola.keys():
           characters[str(c)] = {'count': eidola[c], 'items': filtered.filter(item_id__name=c).all()}
        return characters
    
    def details(self, id: int) -> dict:
        """
        Returns a detailed info to an specified id

        Params:
            id(int): id of item
        """

        items = W.objects.filter(item_id=id)
        count = items.count()
        item = Item.objects.get(item_id=id)

        return {'item': item, 'count': count}
    
    def type_detail(self, type:int) -> dict:
        items_per_types = W.objects.filter(gacha_id__gacha_type=type)
        banners = Banner.objects.filter(gacha_type=type)
        

=======
from django.db.models import Q, Max
from datetime import datetime
from time import sleep
import requests
from bs4 import BeautifulSoup
from django.utils.timezone import make_aware
from django.core.files.images import ImageFile
from io import BytesIO
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from .const import *
from .serializers import *
from collections import Counter
import time

from .models import *
from .models import Warp as W

"""
Utils for Warps
"""

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

def fetch_info(url:str, gacha_type: int) -> int:
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
            url = WIKI_URL + name
            if name in DOUBLES:
                url += "_(Light_Cone)"
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')

            img_name = ''

            if type == 'Light Cone':
                #img_name = 'light_cones/'
                path = soup.find('div', attrs={'class': 'pi-item pi-data pi-item-spacing pi-border-color', 'data-source': 'effect_path'}).find('div', attrs={'class': 'pi-data-value pi-font'}).find('a').text
                img_link = IMAGE_URL + 'light_cone_'
            else:
                #img_name = 'characters/'
                path = soup.find('div', attrs={'class': 'pi-item pi-data pi-item-spacing pi-border-color', 'data-source': 'path'}).find('div', attrs={'class': 'pi-data-value pi-font'}).find('a')['title']
                img_link = IMAGE_URL + 'character_'

            # download image
            img_name += f'{name}.png'
            fetch_img = requests.get(f'{img_link}portrait/{id}.png') # fetch image

            image_bytes = BytesIO(fetch_img.content) # save to byte stream
            django_file = ImageFile(image_bytes, name=img_name)

            # if path does not exist yet in db
            if not Path.objects.filter(name=path).exists():
                # Fetch image
                path_response = requests.get(f'{WIKI_URL + path}')
                path_soup = BeautifulSoup(path_response.content, 'html.parser')

                icon_image_link = path_soup.find('figure', attrs={'data-source': 'image', 'class': 'pi-item pi-image'}).find('a')['href']
                icon_image_name = icon_image_link.split('/')[7]
                get_icon_req = requests.get(icon_image_link)

                path_bytes = BytesIO(get_icon_req.content)
                path_image_file = ImageFile(path_bytes, name=icon_image_name)

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

class WarpAnalyser():
    """
    Analyse all warps
    """
        
    def warps_per_type(self) -> dict:
        """
        Returns amount of warps for all gacha_types

        Returns:
            types(dict): mapping of each type to amount of warps
        """
        types = {}
        for g_id in GachaType.objects.all():
            max_pity = g_id.max_pity
            filtered = W.objects.filter(gacha_id__gacha_type=g_id.id)
            amount = filtered.count()
            jade = amount * 160 # 160 jade = 1 Warp
            euro = round(amount * 2.64, 2) # 2.64€ per warp
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

            types[f'{g_id.name}'] = {'pity': pity, 'warranted': warranted, 'wr': winrate, 'c': amount, 'last_win': WarpSerializer(last_win).data if last_win else None, 'max_pity': max_pity, 'jade': jade, 'euro': euro, 'id': g_id.id}
        return types

    def warps_per_banner(self) -> dict:
        """
        Returns amount of warps for each banner

        Returns:
            banner(dict): mapping of each banner to amount of warps
        """
        banners = {}
        for b in Banner.objects.all():
            items = W.objects.filter(gacha_id=b.id)
            
            banners[f'{b.item_id}'] = {'warps': items}
        return banners

    def characters(self) -> dict:
        """
        Maps amount of characters for idola information
        """
        character_id = ItemType.objects.filter(name=ITEM_TYPES[f'{LANG}'][1]).first() # get name of item type for character
        filtered = W.objects.filter(item_id__typ=character_id.id)

        eidola = Counter(f.item_id for f in filtered)
        characters = {}
        for c in eidola.keys():
           characters[str(c)] = {'count': eidola[c], 'items': filtered.filter(item_id__name=c).all()}
        return characters
    
    def details(self, id: int) -> dict:
        """
        Returns a detailed info to an specified id

        Params:
            id(int): id of item
        """

        items = W.objects.filter(item_id=id)
        count = items.count()
        item = ItemSerializer(Item.objects.get(item_id=id)).data

        return {'item': item, 'count': count}
    
    def type_detail(self, type:int) -> dict:
        items_per_types = W.objects.filter(gacha_id__gacha_type=type)
        banners = Banner.objects.filter(gacha_type=type)
        

>>>>>>> app:backend/warps/utils.py
        return {'i_types': items_per_types, 'banners': banners}