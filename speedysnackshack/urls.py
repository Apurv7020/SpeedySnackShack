"""
URL configuration for speedysnackshack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from food_web import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register),
    path('login/', views.ulogin),
    path('logout/', views.ulogout),
    path('dashboard/', views.dashboard),
    path('menu/', views.menu),
    path('details/<pid>', views.details),
    path('profile/', views.profile),
    path('edit/<eid>', views.editprofile,name="edit"),
    path('cart/', views.cart),
    path('delete/<did>', views.deleteprofile),
    path('category/<cid>', views.cat_filter),
    path('sort/<sid>', views.price_sort),
    path('addtocart/<aid>', views.addtocart),
    path('updateqty/<x>/<qid>', views.update_qty),
    path('feedback/', views.feedback),
    path('store/', views.store),
    path('contact/', views.contact),
    path('about/', views.about),
    path('placeorder/', views.placeorder),
    path('fetchorder/', views.fetchorder),
    path('makepayment/', views.makepayment),
    path('remove/<bid>', views.deleteitem),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)  