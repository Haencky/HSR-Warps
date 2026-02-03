from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Path(models.Model):
    """
    Path item is connected to

    Args:
        name(str): name of path (e.g. hunt)
        icon: icon of path
    """
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='paths/')

    def __str__(self):
        return self.name

class ItemType(models.Model):
    """
    Item Type (current only LC and Figure)

    Args:
        name(str): name of type 
    """
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name

class Item(models.Model):
    """
    Describes an Item

    Args:
        item_id(int): Item ID provided by honkai starrail
        name(str): name of item
        image: image of item
        wiki(str): link to hsr wiki fandom
        rarity(int): rarity of item
        path(int): reference to path   
        eng_name(str): english name of item  
    """
    item_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    typ = models.ForeignKey(ItemType, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='items/')
    wiki = models.URLField()
    rarity = models.IntegerField()
    path = models.ForeignKey(Path, on_delete=models.CASCADE, null=True)
    eng_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        
class GachaType(models.Model):
    """
    Gacha Type; e.g. 11 for Event-Warp

    Args:
        gacha_type(int): type; e.g. 11 for Character Event Warp
        name(str): given name of type
    """

    gacha_type = models.IntegerField(unique=True)
    name = models.CharField(unique=True, max_length=100)
    max_pity = models.IntegerField(default=90)

    def __str__(self):
        return f'{self.gacha_type}: {self.name}'

class Banner(models.Model):
    """
    Describes a banner

    Args:
        gacha_id(int): provided by honkai starrail
        gacha_type(int): reference to gacha type
        item_id(int): reference to item, which can be obtained in banner
    """
    gacha_id = models.IntegerField(unique=True)
    gacha_type = models.ForeignKey(GachaType, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.gacha_id}: {self.item_id if self.item_id else ''}'

class Warp(models.Model):
    """
    Describes an Warp-record

    Args:
        warp_id(int): id provided by honkai starrail
        uid(int): uid of user
        gacha_id(int): reference to banner
        item_id(int): reference to item
        time(datetime): timestamp of pull
        player(int): reference to player
    """
    warp_id = models.IntegerField(unique=True)
    uid = models.IntegerField()
    gacha_id = models.ForeignKey(Banner, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.id}: {self.gacha_id.item_id.name if self.gacha_id.item_id else self.gacha_id.gacha_id}; {self.item_id.name}; {self.time}"