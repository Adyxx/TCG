
from django.shortcuts import render, get_object_or_404
from .models import Card, Character

def home_view(request):
    return render(request, "dbbridge/home.html")

from django.shortcuts import render
from .models import Card, Faction, Character

from django.shortcuts import render
from dbbridge.models import Card, Faction, Character
from django.db.models import Q, Case, When, IntegerField
from django.core.paginator import Paginator

def card_list_view(request):
    query = request.GET.get("name", "").strip()
    rarity = request.GET.get("rarity")
    card_type = request.GET.get("card_type")
    faction = request.GET.get("faction")
    character = request.GET.get("character")
    cost_filter = request.GET.get("cost")

    cards = Card.objects.all()

    if query:
        cards = cards.filter(Q(name__icontains=query) | Q(text__icontains=query)).annotate(
            name_match=Case(
                When(name__icontains=query, then=0),
                default=1,
                output_field=IntegerField(),
            )
        )
    else:
        cards = cards.annotate(name_match=Case(default=1, output_field=IntegerField()))

    if rarity:
        cards = cards.filter(rarity=rarity)
    if card_type:
        cards = cards.filter(card_type=card_type)
    if faction:
        cards = cards.filter(faction_id=faction)
    if character:
        cards = cards.filter(character_id=character)

    if cost_filter:
        if cost_filter == "7+":
            cards = cards.filter(cost__gte=7)
        else:
            try:
                cost_val = int(cost_filter)
                cards = cards.filter(cost=cost_val)
            except ValueError:
                pass

    cards = cards.order_by("cost", "name_match")

    paginator = Paginator(cards, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "rarity_choices": Card.RARITY_CHOICES,
        "type_choices": Card.CARD_TYPE_CHOICES,
        "factions": Faction.objects.all(),
        "characters": Character.objects.all(),
        "selected_cost": cost_filter or "",
    }
    return render(request, "dbbridge/card_list.html", context)


def card_detail_view(request, pk):
    card = get_object_or_404(Card, id=pk)
    return render(request, "dbbridge/card_detail.html", {"card": card})

def character_list_view(request):
    characters = Character.objects.all()
    return render(request, "dbbridge/character_list.html", {"characters": characters})

def character_detail_view(request, pk):
    character = get_object_or_404(Character, pk=pk)
    return render(request, "dbbridge/character_detail.html", {"character": character})

def news_view(request):
    return render(request, "dbbridge/news.html")

def background_view(request):
    return render(request, "dbbridge/background.html")
