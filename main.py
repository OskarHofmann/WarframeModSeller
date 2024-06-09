import parameters as params
import libs.augment_mods as augment_mods
from libs.market_items import MarketItem, MarketItems
from libs.sales_strategies import SellAllAtPrice, SellMostProfitable
from libs.sales_agents import ManualSales


if __name__ == '__main__':
    # load_dotenv()
    mods = augment_mods.get_augment_mods('Red Veil')
    market_items = MarketItems()
    market_items.add_items_from_item_names(mods)

    market_items.get_item_prices()

    # print(SellMostProfitable.propose_mods_to_sell(market_items, sell_below_current_cheapest= True))

    items_to_sell = SellMostProfitable.propose_mods_to_sell(market_items, sell_below_current_cheapest= True)
    ManualSales().sell_items(items_to_sell)

    # TODO automate sale