from django.test import TestCase
from warptracker.models import *

class TestPath(TestCase):
    def setUp(self):
        self.p1 = Path(name="Nihility", icon='media/path')

    def test_string(self):
        self.assertEqual(str(self.p1), 'Nihility')
    
class TestItemType(TestCase):
    def setUp(self):
        self.it = ItemType(name='Character')

    def test_string(self):
        self.assertEqual(str(self.it), 'Character')

class TestItem(TestCase):
    def setUp(self):
        self.typ = ItemType(name='Character')
        self.path = Path(name='Preservation', icon='media/path/preservation.png')
        self.i = Item(
            item_id=1001,
            name='March 7th',
            typ=self.typ,
            image='media/items/March_7th',
            wiki='https://hsr.wiki.com/march_7th',
            rarity=4,
            path=self.path,
            eng_name='March 7th'
        )

    def test_str(self):
        self.assertEqual('March 7th', str(self.i))
    
    def test_typ(self):
        self.assertEqual('Character', self.i.typ.name)
    
    def test_path(self):
        self.assertEqual('Preservation', self.i.path.name)
        self.assertEqual('media/path/preservation.png', self.i.path.icon)
    
class TestGachaType(TestCase):
    def setUp(self):
        self.gt = GachaType(gacha_type=11, name='Character Event Warp', max_pity=90)

    def test_string(self):
        self.assertEqual('11: Character Event Warp', str(self.gt))

class TestBanner(TestCase):
    def setUp(self):
        self.gt = GachaType(gacha_type=11, name='Character Event Warp', max_pity=90)
        self.typ = ItemType(name='Character')
        self.path = Path(name='Preservation', icon='media/path/preservation.png')
        self.i1 = Item(
            item_id=1001,
            name='March 7th',
            typ=self.typ,
            image='media/items/March_7th',
            wiki='https://hsr.wiki.com/march_7th',
            rarity=4,
            path=self.path,
            eng_name='March 7th'
        )
        self.b1 = Banner(gacha_id=1001, gacha_type=self.gt, item_id=self.i1)
        self.b2 = Banner(gacha_id=1001, gacha_type=self.gt, item_id=None)
    
    def test_string(self):
        self.assertEqual('1001: March 7th', str(self.b1))
        self.assertEqual('1001: ', str(self.b2))

class TestWarp(TestCase):
    def setUp(self):
        self.gt = GachaType(gacha_type=11, name='Character Event Warp', max_pity=90)
        self.typ = ItemType(name='Character')
        self.path = Path(name='Preservation', icon='media/path/preservation.png')
        self.i1 = Item(
            item_id=1001,
            name='March 7th',
            typ=self.typ,
            image='media/items/March_7th',
            wiki='https://hsr.wiki.com/march_7th',
            rarity=4,
            path=self.path,
            eng_name='March 7th'
        )
        self.b1 = Banner(gacha_id=1001, gacha_type=self.gt, item_id=self.i1)
        self.b2 = Banner(gacha_id=1001, gacha_type=self.gt, item_id=None)

        self.w1 = Warp(
            id=1,
            warp_id=1,
            uid=1234,
            gacha_id=self.b1,
            item_id =self.i1,
            time='2026-01-01 00:00:00',
            pity=1
        )
        self.w2 = Warp(
            id=2,
            warp_id=1,
            uid=1234,
            gacha_id=self.b2,
            item_id =self.i1,
            time='2026-01-01 00:00:00',
            pity=1
        )

    def test_string(self):
        self.assertEqual('1: March 7th; March 7th; 2026-01-01 00:00:00', str(self.w1))
        self.assertEqual('2: 1001; March 7th; 2026-01-01 00:00:00', str(self.w2))