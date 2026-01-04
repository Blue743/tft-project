import os
import requests
from requests.exceptions import RequestException, Timeout


api_key = os.getenv("RIOT_API_KEY")
player_url = os.getenv("URL")
player_puuid = os.getenv("PUUID_URL")
match_url = os.getenv("MATCH_URL")
rank = os.getenv("TFT_RANK")




def get_safe(url, timeout=20):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    
    except Timeout:
        return {
        "error": "timeout",
        "url": url
        }
    except RequestException as e:
        return {
        "error": "request_error",
        "details": str(e),
        "url": url
        }
    
def data_validation(x, y):
    if x not in y:
        return
    
def fetch_matches(gameName:str , tagLine:str):

    player_url_edited = player_url.format(
        gameName = gameName,
        tagLine = tagLine,
        api_key = api_key
    )

    response_puuid = get_safe(player_url_edited)
    
    if "error" in response_puuid:
        return {
            "error" : "Account not found",
            "stage" : "riot_account_v1",
            "details" : response_puuid
        }

    puuid = response_puuid["puuid"]

    player_tft = player_puuid.format(puuid=puuid, api_key=api_key)

    response_tft = get_safe(player_tft)

    if "error" in response_tft:
        return {
            "error" : "tft_data_error",
            "stage" : "player_lookup_error",
            "details" : response_tft
        }

    match_url_edited = match_url.format(puuid=puuid, api_key=api_key)
    response_match = get_safe(match_url_edited)

    if "error" in response_match:
        return {
            "error" : "match_lookup_error",
            "stage" : "tft_matches_v1",
            "details" : response_match
        }
    
    rank_edited = rank.format(puuid=puuid, api_key=api_key)

    response_rank = get_safe(rank_edited)

    if "error" in response_rank:
        return {
            "error" : "rank_lookup_failed",
            "stage" : "tft_league_v1",
            "details" : response_rank
        }

    all_matches = []

    match_details = os.getenv('MATCH_DETS')

    for match_id in response_match:
        match_url_formatted = match_details.format(
            match_id=match_id,
            api_key=api_key
        )

        match_data = get_safe(match_url_formatted)

        if "error" not in match_data:
            all_matches.append(match_data)


    return all_matches, puuid, gameName, response_rank

    



def get_details(matches, my_puuid):
    details = []

    for match in matches:
        for player in match['info']['participants']:
            if player['puuid'] == my_puuid:
                
                placements = player['placement']
                companion = player['companion']

                details.append({
                    'placement': player['placement'],
                    'companion': player['companion'],
                    })
                break

    return details

    

