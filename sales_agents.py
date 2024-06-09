from market_items import MarketItem
from sales_strategies import SalesStrategy
from abc import ABC, abstractmethod


class SalesAgent(ABC):
    
    @abstractmethod
    def sell_items(self, items_to_sell: list[tuple[MarketItem, int]]) -> None:
        pass


class ManualSales(SalesAgent):
    pass


class AutomaticSales(SalesAgent):
    pass