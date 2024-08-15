from libs.authentification import WFMarketAuth
from dotenv import load_dotenv
import os
import libs.augment_mods as augment_mods
from libs.market_items import MarketItems
from libs.sales_strategies import SellMostProfitable
from libs.sales_agents import AutomaticSales, ManualSales


if __name__ == '__main__':

    mods = augment_mods.get_augment_mods('Red Veil')
    market_items = MarketItems()
    market_items.add_items_from_item_names(mods)

    market_items.get_item_prices()

    items_to_sell = SellMostProfitable.propose_mods_to_sell(market_items, difference_to_highest=0, sell_below_current_cheapest= False)

    # print most profitable mods with price    
    ManualSales().sell_items(items_to_sell)

    # automatic sell most profitable mods at best price
    auth = WFMarketAuth()
    load_dotenv()
    wfm_mail = os.environ.get('WFM_MAIL')
    wfm_password = os.environ.get('WFM_PASSWORD')
    if wfm_mail and wfm_password:
        auth.login_user(wfm_mail, wfm_password)
    else:
        print('Please set "WFM_MAIL" and "WFM_PASSWORD" in the .env file.')
        exit()

    agent = AutomaticSales(auth)
    agent.sell_items(items_to_sell)

    agent.delete_other_orders(market_items)




