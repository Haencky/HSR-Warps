from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from warptracker.models import *

class BaseTestClass(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.itc = ItemType.objects.create(
            name='Character'
        )

        cls.itl = ItemType.objects.create(
            name='Lightcone'
        )

        cls.gt1 = GachaType.objects.create(
            gacha_type=1,
            name='Stellar Warp',
            max_pity=90
        )

        cls.gt11 = GachaType.objects.create(
            gacha_type=11,
            name= 'Character Event Warp',
            max_pity=90
        )

        cls.gt12 = GachaType.objects.create(
            gacha_type=12,
            name='Lightcone Event Warp',
            max_pity=80
        )

        cls.p = Path.objects.create(
            name='Preservation',
            icon='path/preservation.png'
        )

        cls.i_c4 = Item.objects.create(
            item_id=1001,
            name='March 7th',
            typ=cls.itc,
            image='items/march_7th.png',
            wiki='https://wiki.com',
            rarity=4,
            path=cls.p,
            eng_name='March 7th'
        )

        cls.i_c5 = Item.objects.create(
            item_id=1304,
            name='Aventurine',
            typ=cls.itc,
            image='items/aventurine.png',
            wiki='https://wiki.com',
            rarity=5,
            path=cls.p,
            eng_name='Aventurine'
        )

        cls.i_l4 = Item.objects.create(
            item_id=21030,
            name='This Is Me!',
            typ=cls.itl,
            image='items/this_is_me.png',
            wiki='https://wiki.com',
            rarity=4,
            path=cls.p,
            eng_name='This Is Me!'
        )

        cls.i_l5 = Item.objects.create(
            item_id=23023,
            name='Inherently Unjust Destiny',
            typ=cls.itl,
            image='items/inherently_unjust_destiny.png',
            wiki='https://wiki.com',
            rarity=5,
            path=cls.p,
            eng_name='Inherently Unjust Destiny'
        )

        cls.i_c5_l = Item.objects.create(
            item_id=1104,
            name='Gepard',
            typ=cls.itc,
            image='items/gepard.png',
            wiki='https://wiki.com',
            rarity=5,
            path=cls.p,
            eng_name='Gepard'
        )

        cls.i_l5_l = Item.objects.create(
            item_id=23005,
            name='Moment of Victory',
            typ=cls.itl,
            image='items/moment_of_victory.png',
            rarity=5,
            path=cls.p,
            eng_name='Moment of Victory'
        )

        cls.b1 = Banner.objects.create(
            gacha_id=1001,
            gacha_type=cls.gt1,
            item_id=cls.i_c4
        )

        cls.b2 = Banner.objects.create(
            gacha_id=2002,
            gacha_type=cls.gt11,
            item_id=cls.i_c5
        )

        cls.b3 = Banner.objects.create(
            gacha_id=3002,
            gacha_type=cls.gt12,
            item_id=cls.i_l5
        )

        cls.w1_1 = Warp.objects.create(
            warp_id=1,
            uid=123,
            gacha_id=cls.b1,
            item_id=cls.i_c4,
            time='2026-01-01 00:00:00',
            pity=1
        )
        cls.w1_2 = Warp.objects.create(
            warp_id=2,
            uid=123,
            gacha_id=cls.b1,
            item_id=cls.i_c5_l,
            time='2026-01-01 00:00:00',
            pity=2
        )

        cls.w2_1 = Warp.objects.create(
            warp_id=3,
            uid=123,
            gacha_id=cls.b2,
            item_id=cls.i_c4,
            time='2026-01-01 00:00:00',
            pity=1
        )

        cls.w2_2 = Warp.objects.create(
            warp_id=4,
            uid=123,
            gacha_id=cls.b2,
            item_id=cls.i_c5,
            time='2026-01-01 00:00:00',
            pity=2
        )

        cls.w2_3 = Warp.objects.create(
            warp_id=5,
            uid=123,
            gacha_id=cls.b2,
            item_id=cls.i_c5_l,
            time='2026-01-01 00:00:00',
            pity=1
        )

        cls.w3_1 = Warp.objects.create(
            warp_id=6,
            uid=123,
            gacha_id=cls.b3,
            item_id=cls.i_l4,
            time='2026-01-01 00:00:00',
            pity=1
        )

        cls.w3_2 = Warp.objects.create(
            warp_id=7,
            uid=123,
            gacha_id=cls.b3,
            item_id=cls.i_l5,
            time='2026-01-01 00:00:00',
            pity=2,
        )

        cls.w3_3 = Warp.objects.create(
            warp_id=8,
            uid=123,
            gacha_id=cls.b3,
            item_id=cls.i_l5_l,
            time='2026-01-01 00:00:00',
            pity=1
        )

class TestIndex(BaseTestClass):
    def setUp(self):
        self.url = reverse('dashboard')
        self.response = self.client.get(self.url)
        self.stellar_warp = self.response.json()[0]
        self.c_warp = self.response.json()[1]
        self.l_warp = self.response.json()[2]

    def test_name(self):
        self.assertEqual('Stellar Warp', self.stellar_warp['name'])
        self.assertEqual('Character Event Warp', self.c_warp['name'])
        self.assertEqual('Lightcone Event Warp', self.l_warp['name'])

    def test_limited(self):
        self.assertEqual(0, self.stellar_warp['limited'])
        self.assertEqual(1, self.c_warp['limited'])
        self.assertEqual(1, self.l_warp['limited'])

    def test_ptiy(self):
        self.assertEqual(0, self.stellar_warp['pity'])
        self.assertEqual(0, self.c_warp['pity'])
        self.assertEqual(0, self.l_warp['pity'])

        Warp.objects.create(
            warp_id=100,
            uid=123,
            gacha_id=self.b2,
            item_id=self.i_c4,
            time='2026-01-01 00:00:00',
            pity=4
        )

        Warp.objects.create(
            warp_id=101,
            uid=123,
            gacha_id=self.b3,
            item_id=self.i_c4,
            time='2026-01-01 00:00:00',
            pity=4
        )

        response = self.client.get(self.url)
        c_warp = response.json()[1]
        l_warp = response.json()[2]

        self.assertEqual(1, c_warp['pity'])
        self.assertEqual(1, l_warp['pity'])

    def test_warranted(self):
        self.assertEqual(True, self.stellar_warp['warranted'])
        self.assertEqual(True, self.c_warp['warranted'])
        self.assertEqual(True, self.l_warp['warranted'])

    def test_wr(self):
        self.assertEqual(0, self.stellar_warp['wr'])
        self.assertEqual(50, self.c_warp['wr'])
        self.assertEqual(50, self.l_warp['wr'])

        Warp.objects.create(
            warp_id=102,
            uid=123,
            gacha_id=self.b2,
            item_id=self.i_c5,
            time='2026-01-01 00:00:00',
            pity=5
        )

        Warp.objects.create(
            warp_id=101,
            uid=123,
            gacha_id=self.b3,
            item_id=self.i_l5,
            time='2026-01-01 00:00:00',
            pity=5
        )

        response = self.client.get(self.url)
        c_warp = response.json()[1]
        l_warp = response.json()[2]

        self.assertEqual(50, c_warp['wr'])
        self.assertEqual(50, l_warp['wr'])

    def test_avg_pity(self):
        self.assertEqual(2, self.stellar_warp['avg_pity'])
        self.assertEqual(1.5, self.c_warp['avg_pity'])
        self.assertEqual(1.5, self.l_warp['avg_pity'])

    def test_c(self):
        self.assertEqual(2, self.stellar_warp['c'])
        self.assertEqual(3, self.c_warp['c'])
        self.assertEqual(3, self.l_warp['c'])
    
    def test_last_win(self):
        self.assertEqual('Gepard', self.stellar_warp['last_win']['item_id__name'])
        self.assertEqual('Aventurine', self.c_warp['last_win']['item_id__name'])
        self.assertEqual('Inherently Unjust Destiny', self.l_warp['last_win']['item_id__name'])

    def test_max_pity(self):
        self.assertEqual(90, self.stellar_warp['max_pity'])
        self.assertEqual(90, self.c_warp['max_pity'])
        self.assertEqual(80, self.l_warp['max_pity'])

class TestDetailType(BaseTestClass):
    def setUp(self):
        self.url = reverse('detail-types', args=[1])
        self.response = self.client.get(self.url).json()

    def test_len(self):
        self.assertEqual(2, len(self.response['warps']))

    def test_order(self):
        self.assertEqual('Gepard', self.response['warps'][0]['item_name'])
        self.assertEqual('March 7th', self.response['warps'][1]['item_name'])

class TestBanners(BaseTestClass):
    def setUp(self):
        self.url = reverse('banners')
        self.response = self.client.get(self.url).json()

    def test_len(self):
        self.assertEqual(3, len(self.response))
    
    def test_item(self):
        self.assertEqual('March 7th', self.response[-1]['item']) # createt first, last in order
        self.assertEqual('Aventurine', self.response[1]['item']) # created second, second in order
        self.assertEqual('Inherently Unjust Destiny', self.response[0]['item']) # created last, first in order

    def test_ff(self):
        self.assertEqual(1, self.response[2]['ff'])
        self.assertEqual(1, self.response[1]['ff'])
        self.assertEqual(1, self.response[0]['ff'])

    def test_gacha_type(self):
        self.assertEqual(1, self.response[2]['gacha_type'])
        self.assertEqual(11, self.response[1]['gacha_type'])
        self.assertEqual(12, self.response[0]['gacha_type'])

    def test_count(self):
        self.assertEqual(2, self.response[2]['count'])
        self.assertEqual(3, self.response[1]['count'])
        self.assertEqual(3, self.response[0]['count'])

    def test_obtained(self):
        self.assertEqual(4, self.response[2]['obtained']) # obtained is highest rarity item not in LOST
        self.assertEqual(5, self.response[1]['obtained'])
        self.assertEqual(5, self.response[0]['obtained'])

        s5 = Warp.objects.get(warp_id=self.w2_2.warp_id) # remove won item
        s5.delete()

        r = self.client.get(self.url).json()
        b = r[1]

        self.assertEqual(4, b['obtained']) # highest non lost item is now the 4 star item

class TestDetailItem(BaseTestClass):
    def setUp(self):
        self.url = reverse('details', args=[1001])
        self.response = self.client.get(self.url).json()

    def test_obtained(self):
        self.assertEqual(2, self.response['obtained'])
    
    def test_typ_name(self):
        self.assertEqual('Character', self.response['typ_name'])
        
    def test_path(self):
        self.assertEqual('Preservation', self.response['path_name'])
        self.assertEqual('/media/path/preservation.png', self.response['path_icon'])

    def test_rarity(self):
        self.assertEqual(4, self.response['rarity'])

    def test_name(self):
        self.assertEqual('March 7th', self.response['name'])
        self.assertEqual('March 7th', self.response['eng_name'])

    def test_image(self):
        self.assertEqual('/media/items/march_7th.png', self.response['image'])

class TestListGachaTypes(BaseTestClass):
    def setUp(self):
        self.url = reverse('gacha_types')
        self.r = self.client.get(self.url).json()

    def test_len(self):
        self.assertEqual(3, len(self.r))
    
    def test_name(self):
        self.assertEqual('Stellar Warp', self.r[0]['name'])
        self.assertEqual('Character Event Warp', self.r[1]['name'])
        self.assertEqual('Lightcone Event Warp', self.r[2]['name'])
    
    def test_max_pity(self):
        self.assertEqual(90, self.r[0]['max_pity'])
        self.assertEqual(90, self.r[1]['max_pity'])
        self.assertEqual(80, self.r[2]['max_pity'])

    def test_type(self):
        self.assertEqual(1, self.r[0]['gacha_type'])
        self.assertEqual(11, self.r[1]['gacha_type'])
        self.assertEqual(12, self.r[2]['gacha_type'])
    
class TestItems(BaseTestClass):
    def setUp(self):
        self.url = reverse('items')
        self.r = self.client.get(self.url).json()

    def test_len(self):
        self.assertEqual(6, len(self.r))

    def test_obtained(self):
        self.assertEqual(1, self.r[0]['obtained'])
    
    def test_item_type(self):
        self.assertEqual('Character', self.r[0]['typ_name'])
    
    def test_image(self):
        self.assertEqual('/media/items/aventurine.png', self.r[0]['image'])

    def test_name(self):
        self.assertEqual('Aventurine', self.r[0]['name'])
        self.assertEqual('Aventurine', self.r[0]['eng_name'])

class TestPaths(BaseTestClass):
    def setUp(self):
        self.url = reverse('paths')
        self.r = self.client.get(self.url).json()

    def test_len(self):
        self.assertEqual(1, len(self.r))

    def test_name(self):
        self.assertEqual('Preservation', self.r[0]['name'])

    def test_icon(self):
        self.assertEqual('/media/path/preservation.png', self.r[0]['icon'])

class TestDetailBanner(BaseTestClass):
    def setUp(self):
        self.url = reverse('banner', args=[2])
        self.r = self.client.get(self.url).json()

    def test_b(self):
        self.assertEqual('Aventurine' ,self.r['b']['item_name'])
        self.assertEqual('/media/items/aventurine.png', self.r['b']['item_image'])

    def test_warps(self):
        w = self.r['warps']
        self.assertEqual(3, len(w))
        self.assertEqual(1001, w[0]['item_id'])

    def test_types(self):
        t = self.r['types']
        self.assertEqual(1, len(t))
        self.assertEqual('Character', t[0]['name'])
        self.assertEqual(3, t[0]['count'])

    def test_items(self):
        i = self.r['items']
        self.assertEqual(3, len(i))
        self.assertEqual(1, i[0]['count'])
        self.assertEqual(1001, i[0]['item_id'])
    
    def test_rarities(self):
        r = self.r['rarities']
        self.assertEqual(2, len(r))
        self.assertEqual(1, r[0]['count'])