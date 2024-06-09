from market_items import MarketItem, ItemWithPrice
from sales_strategies import SalesStrategy
from abc import ABC, abstractmethod


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
    pass