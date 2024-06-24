from dataclasses import dataclass
from libs.authentification import WFMarketAuth
from libs.market_items import MarketItem
import parameters as params
import requests


@dataclass
class MarketOrder():
    full_order_info: dict
    id: str = ""
    item: MarketItem | None = None

    # read out id and item info from full_order_info dict/json
    def __post_init__(self) -> None:
        pass



def get_current_user_sell_orders(auth: WFMarketAuth) -> list[dict]:
    api_url = params.MARKET_URL + f'/profile/{auth.user_name}/orders'
    header = auth.get_auth_header()

    response = requests.get(api_url, headers = header)
    return response.json()["payload"]["sell_orders"]


def delete_order(order: MarketOrder, auth: WFMarketAuth):
    pass
    

def create_order(item: MarketItem, auth: WFMarketAuth):
    pass

def update_order(order: MarketOrder, auth: WFMarketAuth, new_price: int):
    pass