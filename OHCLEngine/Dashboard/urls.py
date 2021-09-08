from django.urls import path
from . import views

urlpatterns=[
    
    path('',views.MainPage, name='MainPage'),
    path('showstock/',views.ShowStock, name='ShowStock'),
]