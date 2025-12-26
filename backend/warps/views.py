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


    return Response({'types': types, 'items': ItemSerializer(Item.objects.all(), many=True).data, 'history_data': data, 'history_labels': labels})

@api_view(['GET'])
def banners(request: HttpRequest):
    items = Item.objects.all().order_by('name')
    w_per_banner = Warp.objects.all().values('gacha_id', item=F('gacha_id__item_id__name'), item_image=F('gacha_id__item_id__image')).annotate(count=Count('id'), obtained=Max('item_id__rarity', filter=~Q(item_id__item_id__in=LOST)), ff=Count('item_id__rarity', filter=Q(item_id__item_id__in=LOST))).order_by('-gacha_id')
    return Response({'banner': WarpsPerBannerSerializer(w_per_banner, many=True, context={'request': request}).data, 'items': ItemSerializer(items, many=True).data})

@api_view(['POST'])
def add_pulls(request:HttpRequest):
    url = request.data.get('url')
    if not url:
        return Response(
            {'error': 'No URL provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    results = []
    for t in types:
        f = fetch_info(url, t)
        print(f)
        if f['new_warps'] > 0:
            results.append({
                'gacha_type': f['gacha_type'],
                'new_warps': f['new_warps']
            })
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

def list_characters(request: HttpRequest):
    characters = Analyser.characters()
    return render(request, 'characters.html', characters)

@api_view(['GET'])
def detail_item(request:HttpRequest, id:int):
    items = Item.objects.order_by('name')

    return Response({'ret': Analyser.details(id), 'items': ItemSerializer(items, many=True).data})

def detail_banner(request: HttpRequest, id:int):
    items = json.dumps(list(Item.objects.order_by('name').values('name', 'item_id', 'image', 'eng_name')))

    w_per_banner = list(Warp.objects.filter(gacha_id=id).values('item_id__rarity').annotate(count=Count('id')).order_by('item_id__rarity'))
    counts = [x['count'] for x in w_per_banner]
    labels = ['⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐']
    stats = {'labels': labels, 'counts': counts}
    banner_item = Banner.objects.get(gacha_id=id)

    return render(request, 'detail_banner.html', {'items': items})