
from django.shortcuts import render, get_object_or_404
from .models import Card, Character

def home_view(request):
    return render(request, "dbbridge/home.html")

def card_list_view(request):
    cards = Card.objects.all()
    return render(request, "dbbridge/card_list.html", {"cards": cards})

def card_detail_view(request, pk):
    card = get_object_or_404(Card, pk=pk)
    return render(request, "dbbridge/card_detail.html", {"card": card})

def character_list_view(request):
    characters = Character.objects.all()
    return render(request, "dbbridge/character_list.html", {"characters": characters})

def character_detail_view(request, pk):
    character = get_object_or_404(Character, pk=pk)
    return render(request, "dbbridge/character_detail.html", {"character": character})
