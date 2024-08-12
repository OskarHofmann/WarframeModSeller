import parameters as params
from .authentification import WFMarketAuth
from .market_items import ItemWithPrice, MarketItems
from .orders import MarketOrder, create_order_async, delete_order_async, get_current_user_sell_orders
from abc import ABC, abstractmethod
import aiohttp, asyncio



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


    # delete old orders of possible candidates as they are either outdated or should not be sold currently at all
    def delete_other_orders(self, all_candidates: MarketItems):
        orders = get_current_user_sell_orders(self.auth)

        all_candidates_names = [market_item.item_name for market_item in all_candidates.items]
        orders_to_delete = []
        for order in orders:
            if order.item.item_name in all_candidates_names and not order in self.executed_orders: # type: ignore
                orders_to_delete.append(order)
        asyncio.run(self._delete_orders_async(orders_to_delete))

    
    async def _delete_orders_async(self, orders_to_delete: list[MarketOrder]):
        async with aiohttp.ClientSession() as session:
            tasks = [delete_order_async(session, params.NUMBER_OF_API_CALL_RETRIES, order, self.auth) for order in orders_to_delete]
            print('Deleting old orders. Please wait.')
            await asyncio.gather(*tasks)

