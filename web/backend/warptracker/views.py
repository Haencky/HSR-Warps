from rest_framework.decorators import api_view
from django.db.models import F, Max, Q, Count
from rest_framework.response import Response
from rest_framework import status
from .const import LOST, ITEM_ID_URL, IMAGE_URL, WIKI_URL, DOUBLES
from Levenshtein import distance
from io import BytesIO
from django.core.files.images import ImageFile
import requests
from django.contrib import messages
from .utils import WarpAnalyser, fetch_info, check_banner, getLCPath
from .serializers import *
import operator
import json

types = [1, 2, 11, 12, 21, 22]

def get_suggestion(input:str, correct:list, max_distance=3, top_n=5):
    distances = []
    for n in correct:
        d = distance(input.lower(), n.lower())
        if d <= max_distance:
            distances.append({'item': n, 'distance': d})
    return sorted(distances, key=lambda x: x['distance'])[:top_n]

# Create your views here.
@api_view(['GET'])
def index_api(request):
    return Response(WarpAnalyser.warps_per_type())

@api_view(['GET'])
def banners_api(request):
    w_per_banner = Warp.objects.all().values('gacha_id', item=F('gacha_id__item_id__name'), item_image=F('gacha_id__item_id__image'), item_type=F('gacha_id__item_id__typ__name'), hsr_gacha_id=F('gacha_id__gacha_id'), gacha_type=F('gacha_id__gacha_type__gacha_type')).annotate(count=Count('id'), obtained=Max('item_id__rarity', filter=~Q(item_id__item_id__in=LOST)), ff=Count('item_id__rarity', filter=Q(item_id__item_id__in=LOST))).order_by('-gacha_id')
    return Response(WarpsPerBannerSerializer(w_per_banner, many=True, context={'request': request}).data)

@api_view(['POST'])
def add_pulls_api(request):
    url = request.data.get('url')
    if not url:
        return Response(
            {'error': 'No URL provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    added = {t: fetch_info(url, t) for t in types}
    print(added)
    results = [{'name': str(GachaType.objects.filter(gacha_type=t).values_list('name', flat=True)[0]), 'count': added[t]} for t in types if added[t] > 0]
    check_banner()
    return Response({
        'message': 'Imported Warps',
        'details': results
    })

@api_view(['POST'])
def add_items_manual_api(request):
    name:str = request.data.get('eng_name')
    suggestions = []
    item_id = 0
    msg = ""
    try:
        ids = requests.get(ITEM_ID_URL).json()
        wanted = ids[name]
        item_id = wanted
        img_url = f'{IMAGE_URL}image/{"character_" if item_id < 20_000 else "light_cone_"}portrait/{item_id}.png'
        img_name = f'{name}.png'
        fetch_img = requests.get(img_url) # fetch image
        image_bytes = BytesIO(fetch_img.content) # save to byte stream
        django_file = ImageFile(image_bytes, name=img_name)
        wiki = WIKI_URL + name.replace(' ', '_')
        if item_id in DOUBLES: wiki += '_(Light_Cone)'
        rarity = 5 if item_id >= 23_000 else -1
        Item.objects.create(
            item_id = item_id,
            eng_name = name,
            name = name,
            wiki = wiki,
            image = django_file,
            rarity = rarity
        )
    except requests.RequestException:
        messages.error(request, 'Error loading Item IDs Json File')
    except KeyError:
        suggestions = get_suggestion(name, list(ids.keys()))
        msg = f"Could not find '{name}'"
    return Response({'message': msg if msg else f'Added item {name}','id': item_id, 'suggestions': suggestions})

@api_view(['GET'])
def detail_item_api(request, id:int):
    return Response(WarpAnalyser.details(id))

@api_view(['GET'])
def list_gacha_types_api(request):
    return Response(GachaTypeSerializer(GachaType.objects.all(), many=True).data)

@api_view(['GET'])
def item_types_api(request):
    return Response(ItemTypeSerializer(ItemType.objects.all(), many=True).data)

@api_view(['GET'])
def warps_per_item_api(request):
    warps_per_item = Warp.objects.all().values('item_id').annotate(item_image=F('item_id__image'), count=Count('item_id'), item_name=F('item_id__name'), item_type=F('item_id__typ__name'), item_rarity=F('item_id__rarity')).order_by('item_name')
    return Response(WarpsPerItemSerializer(warps_per_item, many=True, context={'request': request}).data)

@api_view(['GET'])
def items_api(request):
    return Response(ItemSerializer(Item.objects.all().prefetch_related('warp_set').order_by('name'), many=True).data)

@api_view(['GET'])
def path_api(request):
    return Response(PathSerializer(Path.objects.all(), many=True).data)