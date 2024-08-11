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
        self.id = self.full_order_info['id']
        item = MarketItem(
            item_name= self.full_order_info['item']['en']['item_name'],
            url_name=  self.full_order_info['item']['url_name'],
            id=        self.full_order_info['item']['id']
        )
        self.item = item



def get_current_user_sell_orders(auth: WFMarketAuth) -> list[MarketOrder]:
    api_url = params.MARKET_URL + f'/profile/{auth.user_name}/orders'
    header = auth.get_auth_header()

    response = requests.get(api_url, headers = header)
    orders_json = response.json()["payload"]["sell_orders"]

    orders = []
    for order in orders_json:
        orders.append(MarketOrder(order))
    return orders


def delete_order(order: MarketOrder, auth: WFMarketAuth):
    pass
    

def create_order(item: MarketItem, auth: WFMarketAuth):
    pass

def update_order(order: MarketOrder, auth: WFMarketAuth, new_price: int):
    pass