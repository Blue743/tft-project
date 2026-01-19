from django.http import JsonResponse
from .services import fetch_matches, get_details, get_safe, set_search, tft_assets
from django.shortcuts import render

def health_check(request):
    return JsonResponse({
        "status": "ok",
        "message": "API is running"
    })


def get_game(request):
    game_name = request.GET.get("gameName")
    tag_line = request.GET.get("tagLine")

    if not game_name or not tag_line:
        return JsonResponse({
            "error" : "Game name and TagLine are required."},
            status = 400
        )
        
    result = fetch_matches()
    player = result["player"]
    matches = result["matches"]
    puuid = player["puuid"]
    rank = player["rank"]

    return JsonResponse({
        "player": game_name,
        "rank": rank,
        "matches": details
    })

def champion_view(request):
    name = request.GET.get("name", "Lux")

    assets = tft_assets()
    set_data = assets["setData"]

    champion_data = None

    for set_ in set_data:
        if set_["name"] == "Set16":
            for champ in set_["champions"]:
                if champ["name"].lower() == name.lower():
                    champion_data = champ
                    break

    if not champion_data:
        return render(request, "champion.html", {
            "name": "Champion not found",
            "cost": "-",
            "traits": [],
            "image": ""
        })
    print(champion_data["icon"])


    icon_path = champion_data.get("icon", "")

    if icon_path:
        image_url = "https://raw.communitydragon.org/latest" + icon_path
    else:
        image_url = ""


    return render(request, "champion.html", {
        "name": champion_data["name"],
        "cost": champion_data.get("cost"),
        "traits": champion_data.get("traits", []),
        "image": image_url
    })