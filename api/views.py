from django.http import JsonResponse
from .services import fetch_matches, get_details, get_safe

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
    
    matches, puuid, game_name, rank = fetch_matches(game_name, tag_line)
    details = get_details(matches, puuid)

    return JsonResponse({
        "player": game_name,
        "rank": rank,
        "matches": details
    })