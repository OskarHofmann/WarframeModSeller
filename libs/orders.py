from dataclasses import dataclass
from libs.authentification import WFMarketAuth
from libs.market_items import ItemWithPrice, MarketItem
import parameters as params
import requests, aiohttp, asyncio


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


def delete_order(order: MarketOrder, auth: WFMarketAuth) -> bool:

    api_url = api_url = params.MARKET_URL + "/profile/orders/" + order.id
    auth_header = auth.get_auth_header()

    response = requests.delete(api_url, headers=auth_header)

    if response.status_code == 200:
        return True
    else:
        return False


    
def create_order(item_with_price: ItemWithPrice, auth: WFMarketAuth, quantity: int = 1, rank: int = 0, verbose: bool = False) -> MarketOrder | None:
    item = item_with_price.item
    price = item_with_price.price

    api_params = {
        "item": item.id,
        "order_type": "sell",
        "platinum": price,
        "quantity": quantity,
        "visible": True,
        "rank": rank,
    }

    api_url = params.MARKET_URL + "/profile/orders"
    auth_header = auth.get_auth_header()

    response = requests.post(api_url, json=api_params, headers= auth_header)

    if response.status_code == 200:
        return MarketOrder(response.json()["payload"]["order"])
    
    if verbose:
        print(f'Creating order failed with response code: {response.status_code}')
    return None


async def create_order_async(session: aiohttp.ClientSession, n_tries: int, 
                             item_with_price: ItemWithPrice, auth: WFMarketAuth, 
                             quantity: int = 1, rank: int = 0) -> MarketOrder | None:
    item = item_with_price.item
    price = item_with_price.price

    api_params = {
        "item": item.id,
        "order_type": "sell",
        "platinum": price,
        "quantity": quantity,
        "visible": True,
        "rank": rank,
    }

    api_url = params.MARKET_URL + "/profile/orders"
    auth_header = auth.get_auth_header()

    for _ in range(n_tries):
        async with session.post(url=api_url, json=api_params, headers = auth_header) as response:
            if response.status != 200:
                await asyncio.sleep(1)
                continue
            response_json = await response.json(content_type=None)

        return MarketOrder(response_json['payload']['order'])
    else:
        return None

  




### Not currently supported by API V1
# def update_order(order: MarketOrder, auth: WFMarketAuth, new_price: int, new_quantity: int = 1, new_rank: int = 0, verbose: bool = False) -> MarketOrder | None:
    
#     if not order.item:
#         raise ValueError("Order to update must have a valid item")

#     api_params = {
#         "item": order.item.id,
#         "order_type": "sell",
#         "platinum": new_price,
#         "quantity": new_quantity,
#         "visible": True,
#         "rank": new_rank,
#     }
#     api_url = params.MARKET_URL + "/profile/orders" + order.id
#     auth_header = auth.get_auth_header()

#     response = requests.put(api_url, json=api_params, headers= auth_header)

#     if response.status_code == 200:
#         return MarketOrder(response.json()["payload"]["order"])
    
#     if verbose:
#         print(f'Updating order failed with response code: {response.status_code}')
#     return None