from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new', views.new_search, name='new_search'),
    path('new_page',views.new_search,name='new_page')]