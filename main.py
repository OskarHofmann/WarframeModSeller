import asyncio, aiohttp
# from dotenv import load_dotenv
# import unicodedata

import parameters as params
import augment_mods
from market_items import MarketItem, MarketItems
from sales_strategies import SellAllAtPrice, SellMostProfitable


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

    print(SellAllAtPrice.propose_mods_to_sell(market_items, sell_at_highest=True))

    # TODO: move above sales strategy to own class/function
    # TODO automate sale