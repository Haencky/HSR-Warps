from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, JsonResponse
from django.contrib import messages
from django.db.models import Count, Max, Q
from django.core.files.images import ImageFile
from django.utils.safestring import mark_safe
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

# Create your views here.
def index(request):
    types = Analyser.warps_per_type()
    items = json.dumps(list(Item.objects.order_by('name').values('name', 'item_id', 'image', 'eng_name')))

    labels, data = [], []
    
    queryset = Warp.objects.select_related('item_id').values('item_id__rarity').annotate(count=Count('id')).order_by('item_id__rarity')
    for warp in queryset:
        labels.append(warp['item_id__rarity'])
        data.append(int(warp['count']))

    labels = json.dumps(labels)
    data = json.dumps(data)

    return render(request, 'index.html', {'types': types, 'items': items, 'history_data': data, 'history_labels': labels})

def banners(request: HttpRequest):
    items = json.dumps(list(Item.objects.order_by('name').values('name', 'item_id', 'image', 'eng_name')))
    w_per_banner = Warp.objects.all().values('gacha_id', 'gacha_id__item_id__image', 'gacha_id__gacha_type__gacha_type').annotate(count=Count('id'), obtained=Max('item_id__rarity', filter=~Q(item_id__item_id__in=LOST)), ff=Count('item_id__rarity', filter=Q(item_id__item_id__in=LOST))).order_by('gacha_id__id')
    return render(request, 'banners.html', {'banner': w_per_banner, 'items': items})

#@login_required(login_url='/login')
def add_pulls(request:HttpRequest):
    if request.method == 'POST':
        form = AddPullsForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            for t in types:
                f = fetch_info(url, t)
                if f['new_warps'] > 0:
                    messages.success(request, f'{f['gacha_type']}: {f['new_warps']} Warps added!')
        check_banner()
            
    else:
        form = AddPullsForm()
    return render(request, 'add_pulls.html', {'form': form})

def add_items_manual(request:HttpRequest):
    items = json.dumps(list(Item.objects.order_by('name').values('name', 'item_id', 'image', 'eng_name')))
    if request.method == 'POST':
        form = AddItemManual(request.POST)
        if form.is_valid():
            name = form.cleaned_data['eng_name']
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
                wiki = WIKI_URL + name
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
def login_view(request):
    """
    Login View
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            form.add_error(None, 'Login failed')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def list_characters(request: HttpRequest):
    characters = Analyser.characters()
    return render(request, 'characters.html', characters)

def detail_item(request:HttpRequest, id:int):
    items = json.dumps(list(Item.objects.order_by('name').values('name', 'item_id', 'image', 'eng_name')))

    return render(request, 'details.html', {'ret': Analyser.details(id), 'items': items})

def detail_banner(request: HttpRequest, id:int):
    items = json.dumps(list(Item.objects.order_by('name').values('name', 'item_id', 'image', 'eng_name')))

    w_per_banner = list(Warp.objects.filter(gacha_id=id).values('item_id__rarity').annotate(count=Count('id')).order_by('item_id__rarity'))
    counts = [x['count'] for x in w_per_banner]
    labels = ['⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐']
    stats = {'labels': labels, 'counts': counts}
    banner_item = Banner.objects.get(gacha_id=id)


    return render(request, 'detail_banner.html', {'items': items})

def api_types(request:HttpRequest, type:int) -> JsonResponse:
    w_per_type = list(Warp.objects.filter(gacha_id__gacha_type=type).values('item_id__rarity').annotate(count=Count('id')).order_by('item_id__rarity'))
    counts = [x['count'] for x in w_per_type]
    labels = ['⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐']

    return JsonResponse({
        'labels': labels,
        'data': counts,
        'title': 'Pulls nach Rarity'
    })

def api_banner(request: HttpRequest, banner: int) -> JsonResponse:
    w_per_banner = list(Warp.objects.filter(gacha_id=banner).values('item_id__rarity').annotate(count=Count('id')).order_by('item_id__rarity'))
    counts = [x['count'] for x in w_per_banner]
    labels = ['⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐']

    return JsonResponse({
        'labels': labels,
        'data': counts,
        'title': 'Pulls per Rarity' 
    })