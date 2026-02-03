<<<<<<< HEAD:hsr_pulls/urls.py
"""
URL configuration for hsr_pulls project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from warps.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('', index, name='home'),
    path('add/', add_pulls, name='add'),
    #path('characters/', list_characters, name='characters'),
    path('banners', banners, name='list_banners'),
    path('detail_banner/<int:id>/', detail_banner, name='detail_banner'),
    path('details/<int:id>/', detail_item, name='details'),
    path('add_item/', add_items_manual, name='add_item'),
    path('api/type/<int:type>/', api_types, name='api_types'),
    path('api/banner/<int:banner>', api_banner, name='api_banner'),
     path('api/dashboard', index_api),
    path('api/add', add_pulls_api),
    path('api/banners', banners_api),
    path('api/item_types', item_types_api),
    path('api/details/<int:id>', detail_item_api),
    path('api/add_item', add_items_manual_api),
    path('api/gacha_types', list_gacha_types_api),
    path('api/item_warps', warps_per_item_api),
    path('api/items', items_api)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
"""
URL configuration for hsr_pulls project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from warps.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/dashboard', index_api),
    path('api/add', add_pulls_api),
    path('api/banners', banners_api),
    path('api/item_types', item_types_api),
    path('api/details/<int:id>', detail_item_api),
    path('api/add_item', add_items_manual_api),
    path('api/gacha_types', list_gacha_types_api),
    path('api/item_warps', warps_per_item_api),
    path('api/items', items_api)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> app:backend/hsr_pulls/urls.py
