from libs.authentification import WFMarketAuth
import parameters as params
import requests


def get_current_user_sell_orders(auth: WFMarketAuth) -> list[dict]:
    api_url = params.MARKET_URL + f'/profile/{auth.user_name}/orders'
    header = auth.get_auth_header()

    response = requests.get(api_url, headers = header)
    
    return response.json()["payload"]["sell_orders"]


def delete_order():
    pass
    
#TODO: Move functions to seperate class
def create_order():
    pass

def update_order():
    pass