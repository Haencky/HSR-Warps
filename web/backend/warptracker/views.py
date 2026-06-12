# Copyright (C) 2026 Haencky
# SPDX-License-Identifier: GPL-3.0-or-later
from rest_framework.decorators import api_view
from django.db.models import F, Max, Q, Count
from rest_framework.response import Response
from rest_framework import status
from .const import LOST, IMAGE_URL, WIKI_URL, LIGHTCONE_NAMES
from Levenshtein import distance
from io import BytesIO
from django.core.files.images import ImageFile
import requests
from django.contrib import messages
from .utils import WarpAnalyser, fetch_info, check_banner, update_all, getData
from .serializers import *

types = [1, 2, 11, 12, 21, 22]

def get_analyser() -> WarpAnalyser:
    warps = all_warps = Warp.objects.all().select_related('item_id', 'gacha_id').order_by('warp_id').values('warp_id', 'pity', 'item_id__rarity', 'item_id__item_id', 'item_id__name', 'gacha_id__gacha_type', 'item_id__image')
    return WarpAnalyser(list(warps), all_warps.values_list('warp_id'))

def create_item_manually(item_id: int) -> dict:
    if Item.objects.filter(item_id=item_id).exists():
        return {'success': True, 'message': f'Item {item_id} already exists in the database.'}
    
    items = getData()
    try:
        item = items[f'{item_id}']
    except KeyError:
        print(f'Could not find item {item_id}.')
        return {'success': False, 'message': f'Could not find item {item_id}.'}
        
    name = item['name']
    rarity = item['rarity']
    path_name = item['path'] if item['path'] != 'Hunt' else f'The Hunt'
    path, created = Path.objects.get_or_create(name=path_name)

    if created:
        try:
            r = requests.get(f'{IMAGE_URL}icon/path/{item["path"]}.png')
            if r.status_code == 200:
                path_bytes = BytesIO(r.content)
                path_file = ImageFile(path_bytes, name=path_name)
                path.icon.save(path_name, path_file, save=True)
            else:
                print(f'Error loading path icon: {r.status_code}.')
                path.delete()
                return {'success': False, 'message': f'Could not fetch icon for path {path_name}'}
        except requests.RequestException as e:
            print(f'Error loading path icon: {e}')
            path.delete()
            return {'success': False, 'message': f'Could not fetch icon for path {path_name}'}
            
    img_url = f'{IMAGE_URL}image/{"character_" if item_id < 20_000 else "light_cone_"}portrait/{item_id}.png'
    img_name = f'{name}.png'
    try:
        fetch_img = requests.get(img_url)
        if fetch_img.status_code == 200:
            image_bytes = BytesIO(fetch_img.content)
            django_file = ImageFile(image_bytes, name=img_name)
        else:
            return {'success': False, 'message': f'Error loading image for {name}'}
    except requests.RequestException:
        return {'success': False, 'message': f'Error loading image for {name}'}
        
    wiki = WIKI_URL + name.replace(' ', '_')
    if item_id < 20_000:
        typ = ItemType.objects.exclude(name__in=LIGHTCONE_NAMES).first()
    else:
        typ = ItemType.objects.filter(name__in=LIGHTCONE_NAMES).first()
        
    if not typ:
        return {'success': False, 'message': 'Run a normal import first to create itemtypes in your database.'}
        
    Item.objects.create(
        item_id=item_id,
        eng_name=name,
        name=name,
        wiki=wiki,
        image=django_file,
        rarity=rarity,
        path=path,
        typ=typ
    )
    return {'success': True, 'message': f'Created item {name} in database.'}

# Create your views here.
@api_view(['GET'])
def index_api(request):
    return Response(get_analyser().per_type())

@api_view(['GET'])
def detail_type_api(request, gacha_id:int):
    ws = Warp.objects.filter(gacha_id__gacha_type=gacha_id).order_by('-warp_id')
    return Response({
        'warps': WarpSerializer(ws, many=True).data
    })

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
    data = getData()
    added = {t: fetch_info(url, t, data) for t in types}
    print(added)
    results = [{'name': str(GachaType.objects.filter(gacha_type=t).values_list('name', flat=True)[0]), 'count': added[t]} for t in types if added[t] > 0]
    check_banner()
    return Response({
        'message': 'Imported Warps',
        'details': results
    })

@api_view(['POST'])
def add_items_manual_api(request):
    try:
        item_id = int(request.data.get('item_id'))
    except (TypeError, ValueError):
        return Response({'message': 'Invalid item_id provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
    result = create_item_manually(item_id)
    return Response({'message': result['message']})

@api_view(['GET'])
def detail_item_api(request, id:int):
    return Response(ItemSerializer(Item.objects.get(item_id=id)).data)

@api_view(['GET'])
def list_gacha_types_api(request):
    return Response(GachaTypeSerializer(GachaType.objects.all(), many=True).data)

@api_view(['GET'])
def item_types_api(request):
    return Response(ItemTypeSerializer(ItemType.objects.all(), many=True).data)

# @api_view(['GET'])
# def warps_per_item_api(request):
#     warps_per_item = Warp.objects.all().values('item_id').annotate(item_image=F('item_id__image'), count=Count('item_id'), item_name=F('item_id__name'), item_type=F('item_id__typ__name'), item_rarity=F('item_id__rarity')).order_by('item_name')
#     return Response(WarpsPerItemSerializer(warps_per_item, many=True, context={'request': request}).data)

@api_view(['GET'])
def items_api(request):
    return Response(ItemSerializer(Item.objects.all().prefetch_related('warp_set').order_by('name'), many=True).data)

@api_view(['GET'])
def path_api(request):
    return Response(PathSerializer(Path.objects.all(), many=True).data)

@api_view(['GET', 'PATCH'])
def detail_banner_api(request, id:int):
    if request.method == 'PATCH':
        banner_obj = Banner.objects.get(id=id)
        item_id = request.data.get('item_id')
        if item_id is not None:
            item_id = int(item_id)
            if not Item.objects.filter(item_id=item_id).exists():
                result = create_item_manually(item_id)
                if not result['success']:
                    return Response({'error': result['message']}, status=status.HTTP_400_BAD_REQUEST)

        banner_obj.item_id_id = item_id
        banner_obj.save()
        return Response({'message': 'Banner updated successfully'}, status=status.HTTP_200_OK)
    else:
        b = BannerSerializer(Banner.objects.get(id=id)).data
        b_data = Warp.objects.filter(gacha_id=id)
        warps = WarpSerializer(b_data.annotate(rarity=F('item_id__rarity')), many=True).data
        items = b_data.values('item_id').annotate(count=Count('item_id'), name=F('item_id__name'), image=F('item_id__image'), rarity=F('item_id__rarity'))
        types = b_data.values('item_id__typ').annotate(count=Count('item_id__typ'), name=F('item_id__typ__name'))
        rarities = b_data.values('item_id__rarity').annotate(count=Count('item_id__rarity'))
        return Response({
            'b': b,
            'warps': warps,
            'items': items,
            'types': types,
            'rarities': rarities
        })

@api_view(['GET'])
def update_image_api(request):
   return Response({
       'updated': update_all()
   })

@api_view(['POST'])
def api_calc_possibilities(request):
    fours = Warp.objects.filter(item_id__rarity=4, item_id__lt=19999).values('item_id').annotate(total=Count('item_id')).filter(total__gte=7).count()
    try:
        pulls = request.data.get('pulls')
        characters = request.data.get('characters')
        lightcones = request.data.get('lightcones')
        c = request.data.get('character_id')
        l = request.data.get('lightcone_id')
    except:
        pulls = 0
        characters = 0
        lightcones = 0
        c = 1
        l = 2
    stats = get_analyser().monte_carlo(
        {
            c:
                {'copies': characters, 'banner': 'characters', 'obtained': Warp.objects.filter(item_id__item_id=c).count()},
            l: 
                {'copies': lightcones, 'banner': 'lightcones', 'obtained': Warp.objects.filter(item_id__item_id=l).count()}
        }, pulls, False, fours
    )

    if stats is not None:
        char = stats.columns[0]
        lc = stats.columns[1]
    
        char_data = stats[char]
        lc_data = stats[lc]
        prob_c = (char_data >= characters).sum() / len(stats)
        prob_lc = (lc_data >= lightcones).sum() / len(stats)
        prob = prob_c * prob_lc
        starlight = stats['undying_starlight'].mean()
        total_pulls = stats['total_pulls'].mean()
    else:
        prob = starlight = total_pulls = 0

    return Response({'percent': prob, 'starlight': starlight, 'total_pulls': total_pulls})