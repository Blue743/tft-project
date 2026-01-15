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


    return  {
    "player": {
        "gameName": gameName,
        "puuid": puuid,
        "rank": response_rank
    },
    "matches": all_matches
}

    


def get_details(matches, my_puuid):
    details = []
    champion_ids = []

    for match in matches:
        for player in match['info']['participants']:

            
            if player['puuid'] == my_puuid:

                details.append({
                    'placement': player['placement'],
                    'companion': player['companion'],
                    'gold_left': player['gold_left'],
                    'last_round': player['last_round']
                })

                
                units = player['units']
                for unit in units:
                    champion_ids.append(unit['character_id'])

                break

    return details, champion_ids
    

def build_player_view(gameName, tagLine):

    result = fetch_matches(gameName, tagLine)

    if isinstance(result, dict) and "error" in result:
        return  result


    
    player = result["player"]
    matches = result["matches"]
    puuid = player["puuid"]
    gameName = player["gameName"]
    rank = player["rank"]

    details = get_details(matches, puuid)

    return {
        "player": {
            "game_name": gameName,
            "rank": rank
        },
        "matches": details
    }

cache_cdragon = None #variavel vazia para armazenar o json

cdragon_url = "https://raw.communitydragon.org/latest/cdragon/tft/pt_br.json"

def tft_assets():
    global cache_cdragon     # declara ela como global, pra ser reconhecida dentro da função
    if cache_cdragon:     # esse if verifica se ela ainda é NONE. se for NONE = Lança a request. Se já existir info aqui,ignora e apenas retorna a info que já existe;
        return cache_cdragon     # auto explicativo.

    else:
        try:
            response = requests.get(cdragon_url) 
            response.raise_for_status()     #Esse modulo levanta erros HTTP para retornos ruins, ex: 4xx 5xx ...
            cache_cdragon = response.json()     # armazena o Json do community dragon na variavel vazia.
        except requests.exceptions.RequestException as e:     # esse modulo captura TODOS os erros que podem acontecer com o REQUESTS. importante se lembrar de usar.
            return {
                "error" : e
            }
    print(cache_cdragon.keys())
    return cache_cdragon # retorna a info.


assets = tft_assets() 


def set_search():
    set_data = assets['setData']
    print(assets['setData'][0].keys())
    for i in set_data:
        if i["name"] == "Set16":
            set16 = i
            for champ in set16["champions"]:
                if champ["name"] == "Lux":
                    print(champ['name'], champ['cost'], champ['role'], champ['traits'])
set_search()


#acessa o banco de dados do CD usando a funçao.
#itera sobre cada set data, pra poder fazer a comparação.
#compara se o iterável['nome'] tem o mesmo nome do Set que voce quer.
# resultado : o iterável recebe o set16
# agora itera sobre a chave set['champions']
# faz outra comparação, se i é igual ao nome que foi passado:sucesso
# printa o nome custo e traits. 





















    
