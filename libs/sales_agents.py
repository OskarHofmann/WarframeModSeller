from libs.authentification import WFMarketAuth
from .market_items import MarketItem, ItemWithPrice, MarketItems
from abc import ABC, abstractmethod
import aiohttp, asyncio
from .orders import create_order_async
import parameters as params



class SalesAgent(ABC):
    
    @abstractmethod
    def sell_items(self, items_to_sell: list[ItemWithPrice]) -> None:
        pass


# just prettifies the items and prices for easier manual sales
class ManualSales(SalesAgent):

    def sell_items(self, items_to_sell: list[ItemWithPrice]) -> None:
        length_of_longest_item_name = max([len(item_to_sell.item.item_name)
                                            for item_to_sell in items_to_sell])
        sales_suggestion = "Sell\n"
        for item_with_price in items_to_sell:
            item_name = item_with_price.item.item_name
            price = item_with_price.price
            sales_suggestion += f"{item_name:<{length_of_longest_item_name}} at {price}\n"

        print(sales_suggestion)


class AutomaticSales(SalesAgent):
    
    def __init__(self, auth: WFMarketAuth) -> None:
        self.auth = auth
        self.executed_orders = []

    def sell_items(self, items_to_sell: list[ItemWithPrice]) -> None:
        asyncio.run(self._sell_items_async(items_to_sell))

    async def _sell_items_async(self, items_to_sell: list[ItemWithPrice]) -> None:
        async with aiohttp.ClientSession() as session:
            tasks = [create_order_async(session, params.NUMBER_OF_API_CALL_RETRIES, item, self.auth) for item in items_to_sell]
            print('Creating sell orders on WarframeMarket. Please wait.')
            excuted_orders = await asyncio.gather(*tasks)
            self.executed_orders.extend(excuted_orders)

    # delete old orders that are not set/updated to new prices
    def delete_other_orders(self, item_to_sell: list[ItemWithPrice], all_items: MarketItems):
        pass
    

