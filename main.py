import asyncio, aiohttp
# from dotenv import load_dotenv
# import unicodedata

import parameters as params
import augment_mods
from market_items import MarketItem, MarketItems
from sales_strategies import SellAllAtPrice, SellMostProfitable



def mod_names_to_ids(mods: list[str]) -> list[str]:
    return [mod.replace(' ', '_').replace("'", "").lower() for mod in mods]

# def mod_ids_to_names(mods: list[str]) -> list[str]:
#     return [mod.replace('_', ' ').title() for mod in mods]


async def get_order_prices(item_id: str, session: aiohttp.ClientSession, n_tries: int = 20) -> list[int] :
    api_url = params.MARKET_URL + f'/items/{item_id}/orders'
    # try n_tries times, before giving up
    for _ in range(n_tries):
        async with session.get(api_url) as response:
            if response.status != 200:
                await asyncio.sleep(1)
                continue
            response_json = await response.json(content_type=None)

        orders = response_json['payload']['orders']
        break
    else:
        print(f'API call for {item_id} failed.')
        return []

    available_orders = [order for order in orders if \
                        order['user']['status'] == 'ingame' and \
                        order['order_type'] == 'sell']
    prices = [order['platinum'] for order in available_orders]
    prices.sort()
    return prices


async def get_mod_prices(mods: list[str]) -> dict[str, list[int]]:
    mod_ids = mod_names_to_ids(mods)
    async with aiohttp.ClientSession() as session:
        tasks = [get_order_prices(mod_id, session) for mod_id in mod_ids]
        print('Gathering mod prices from WarframeMarket. Please wait.')
        results = await asyncio.gather(*tasks)          

    # gather returns in same order as in the task order (i.e. the same order as in mod_ids)
    return dict(zip(mod_ids, results))


if __name__ == '__main__':
    # load_dotenv()
    mods = augment_mods.get_augment_mods('Red Veil')
    market_items = MarketItems()
    market_items.add_items_from_item_names(mods)

    market_items.get_item_prices()

    cheapest_offers = {item.item_name: item.prices[0] 
                       for item in market_items.items 
                       if len(item.prices) > 0}
    optimal_sell_price = max(cheapest_offers.values())
    mods_to_sell = [k for k,v in cheapest_offers.items() if v == optimal_sell_price]

    mods_to_sell_prettified = "\n".join(mods_to_sell)

    print(f'\nSell \n{mods_to_sell_prettified}\nat {optimal_sell_price - 1} platinum!')

    print(SellAllAtPrice.propose_mods_to_sell(market_items))

    # TODO: move above sales strategy to own class/function
    # TODO automate sale