from django.contrib import admin
from .models import Banner, Path, Item, Warp, ItemType, GachaType

# Register your models here.
admin.site.register(Banner)
admin.site.register(Path)
admin.site.register(Item)
admin.site.register(Warp)
admin.site.register(ItemType)
admin.site.register(GachaType)