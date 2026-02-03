from rest_framework import serializers
from .models import *
from django.conf import settings

class PathSerializer(serializers.ModelSerializer):
    class Meta:
        model = Path
        fields = '__all__'

class ItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    typ_name = serializers.CharField(source='typ.name', read_only=True)
    path_name = serializers.CharField(source='path.name', read_only=True)
    path_icon = serializers.ImageField(source='path.icon', read_only=True)
    obtained = serializers.SerializerMethodField()
    class Meta:
        model = Item
        fields = '__all__'
    
    def get_obtained(self, obj):
        return obj.warp_set.exists()

class GachaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GachaType
        fields = '__all__'

class BannerSerializer(serializers.ModelSerializer):
    item_image = serializers.ImageField(source='item_id.image', read_only=True)
    item_name = serializers.CharField(source='item_id.name', read_only=True)
    class Meta:
        model = Banner
        fields = '__all__'

class WarpSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item_id.name', read_only=True)
    item_image = serializers.ImageField(source='item_id.image', read_only=True)
    class Meta:
        model = Warp
        fields = '__all__'

class WarpsPerBannerSerializer(serializers.Serializer):
    gacha_id = serializers.IntegerField()
    warp_id = serializers.IntegerField(required=False)
    item = serializers.CharField(required=False)
    item_image = serializers.SerializerMethodField()
    item_type = serializers.CharField(required=False)
    hsr_gacha_id = serializers.IntegerField(required=True)
    uid = serializers.IntegerField(required=False)
    item_id = serializers.IntegerField(required=False)
    time = serializers.DateTimeField(required=False)
    count = serializers.IntegerField()
    obtained = serializers.IntegerField(allow_null=True)
    ff = serializers.IntegerField()

    def get_item_image(self, obj):
        image_path = obj.get('item_image')
        if not image_path:
            return None
        request = self.context.get('request')
        if request is not None:
            return settings.MEDIA_URL + image_path
        return settings.MEDIA_URL + str(image_path)
    
class WarpsPerItemSerializer(serializers.Serializer):
    item_name = serializers.CharField(required=True)
    count = serializers.IntegerField(required=True)
    item_image = serializers.SerializerMethodField()
    item_type = serializers.CharField(required=True)
    item_rarity = serializers.IntegerField(required=True)

    def get_item_image(self, obj):
        image_path = obj.get('item_image')
        if not image_path:
            return None
        request = self.context.get('request')
        if request is not None:
            return settings.MEDIA_URL + image_path
        return settings.MEDIA_URL + str(image_path)