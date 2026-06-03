"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from warptracker.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api/dashboard', index_api, name='dashboard'),
    path('api/add', add_pulls_api, name='add'),
    path('api/banners', banners_api, name='banners'),
    path('api/item_types', item_types_api, name='item_types'),
    path('api/details/<int:id>', detail_item_api, name='details'),
    path('api/add_item', add_items_manual_api, name='add_item'),
    path('api/gacha_types', list_gacha_types_api, name='gacha_types'),
    #path('api/item_warps', warps_per_item_api, name='item_warps'),
    path('api/items', items_api, name='items'),
    path('api/paths', path_api, name='paths'),
    path('api/banner/<int:id>', detail_banner_api, name='banner'),
    path('api/update', update_image_api),
    path('api/detail-types/<int:gacha_id>', detail_type_api, name='detail-types'),
    path('api/calculator', api_calc_possibilities, name='calculator'),
    #path('api/edit/banner/<int:banner_id>', name='edit_banner')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)