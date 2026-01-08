from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, JsonResponse
from django.contrib import messages
from django.db.models import Count, Max, Q, F
from django.core.files.images import ImageFile
from django.utils.safestring import mark_safe

from rest_framework.decorators import api_view
from rest_framework.response import Response
from  rest_framework import status
from .serializers import *

import json
import requests
from io import BytesIO
from Levenshtein import distance
import operator

from .utils import fetch_info, WarpAnalyser, check_banner
from .models import *
from .forms import *
from .const import LOST, ITEM_ID_URL, IMAGE_URL, WIKI_URL

types = [1, 2, 11, 12, 21, 22]

Analyser = WarpAnalyser()

def get_suggestion(input:str, correct:list, max_distance=3, top_n=5):
    distances = {}
    for n in correct:
        d = distance(input.lower(), n.lower())
        if d <= max_distance:
            distances[n] = d
    return sorted(distances.items(), key=operator.itemgetter(1))[:top_n]

# Create your views here
@api_view(['GET'])
def index_api(request):
    types = Analyser.warps_per_type()
    labels, data = [], []
    
    queryset = Warp.objects.select_related('item_id').values('item_id__rarity').annotate(count=Count('id')).order_by('item_id__rarity')
    for warp in queryset:
        labels.append(warp['item_id__rarity'])
        data.append(int(warp['count']))
 
    data = json.dumps(data)
    labels = json.dumps(labels)


    return Response({'types': types, 'history_data': data, 'history_labels': labels})

@api_view(['GET'])
def banners(request: HttpRequest):
    w_per_banner = Warp.objects.all().values('gacha_id', item=F('gacha_id__item_id__name'), item_image=F('gacha_id__item_id__image'), item_type=F('gacha_id__item_id__typ__name'), hsr_gacha_id=F('gacha_id__gacha_id')).annotate(count=Count('id'), obtained=Max('item_id__rarity', filter=~Q(item_id__item_id__in=LOST)), ff=Count('item_id__rarity', filter=Q(item_id__item_id__in=LOST))).order_by('-gacha_id')
    return Response(WarpsPerBannerSerializer(w_per_banner, many=True, context={'request': request}).data)

@api_view(['POST'])
def add_pulls(request:HttpRequest):
    url = request.data.get('url')
    if not url:
        return Response(
            {'error': 'No URL provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    results = [{str(GachaType.objects.filter(gacha_type=t).values_list('name', flat=True)[0]): fetch_info(url, t)} for t in types if GachaType.objects.filter(gacha_type=t).exists()]
    check_banner()
    return Response({
        'message': 'Imported Warps',
        'details': results
    })


def add_items_manual(request:HttpRequest):
    items = json.dumps(list(Item.objects.order_by('name').values('name', 'item_id', 'image', 'eng_name')))
    if request.method == 'POST':
        form = AddItemManual(request.POST)
        if form.is_valid():
            name:str = form.cleaned_data['eng_name']
            try:
                ids = requests.get(url=ITEM_ID_URL).json()
            except:
                messages.error(request, 'Error loading Item IDs Json File')
            try:
                wanted = ids[name]
                item_id = wanted
                img_url = f'{IMAGE_URL}{"character_" if item_id < 20_000 else "light_cone_"}portrait/{item_id}.png'
                img_name = f'{name}.png'
                fetch_img = requests.get(img_url) # fetch image
                image_bytes = BytesIO(fetch_img.content) # save to byte stream
                django_file = ImageFile(image_bytes, name=img_name)
                wiki = WIKI_URL + name.replace(' ', '_')
                if item_id in LOST: wiki += '_(Light_Cone)'
                rarity = 5 if item_id >= 23_000 else -1
                Item.objects.create(
                    item_id = item_id,
                    eng_name = name,
                    name = name,
                    wiki = wiki,
                    image = django_file,
                    rarity = rarity
                )
                return redirect(f'/admin/warps/item/{item_id}/change')
            except KeyError:
                suggestions = get_suggestion(name, list(ids.keys()))
                suggestion_list_html = '<br>'.join([
                    f'<strong>{s[0]}</strong>' 
                    for s in suggestions
                ])
                messages.error(request, mark_safe(f'Could not find id to given name: "{name}"!<br>Try:<br>{suggestion_list_html}'))
    else:
        form = AddItemManual()
    return render(request, 'add_item.html', {'form': form, 'items': items})

@api_view(['GET'])
def detail_item(request:HttpRequest, id:int):
    items = Item.objects.order_by('name')

    return Response(Analyser.details(id))

@api_view(['GET'])
def list_gacha_types(request):
    return Response(GachaTypeSerializer(GachaType.objects.all(), many=True).data)

@api_view(['GET'])
def item_types(request):
    return Response(ItemTypeSerializer(ItemType.objects.all(), many=True).data)

@api_view(['GET'])
def warps_per_item(request):
    warps_per_item = Warp.objects.all().values('item_id').annotate(item_image=F('item_id__image'), count=Count('item_id'), item_name=F('item_id__name'), item_type=F('item_id__typ__name'), item_rarity=F('item_id__rarity')).order_by('item_name')
    return Response(WarpsPerItemSerializer(warps_per_item, many=True, context={'request': request}).data)
