from libs.authentification import WFMarketAuth
import parameters as params
import requests


def get_current_user_sell_orders(self, auth: WFMarketAuth) -> list[dict]:
    api_url = params.MARKET_URL + f'/profile/{auth.user_name}/orders'
    header = auth.get_auth_header()

    response = requests.get(api_url, headers = header)
    
    return response.json()["payload"]["sell_orders"]


# delete old orders that are not set/updated to new prices
def delete_other_orders(self, item_to_sell: list[ItemWithPrice], all_items: MarketItems):
    pass
    
#TODO: Move functions to seperate class
def create_order(self):
    pass

def update_order(self):
    pass