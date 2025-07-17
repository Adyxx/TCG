
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('cards/', views.card_list_view, name='card_list'),
    path('cards/<int:pk>/', views.card_detail_view, name='card_detail'),
    path('characters/', views.character_list_view, name='character_list'),
    path('characters/<int:pk>/', views.character_detail_view, name='character_detail'),
    path('background/', views.background_view, name='background'),
    path('news/', views.news_view, name='news'),
]
