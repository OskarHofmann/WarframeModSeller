from abc import ABC, abstractmethod
from market_items import MarketItem, MarketItems

class SalesStrategy(ABC):

    @staticmethod
    @abstractmethod
    def propose_mods_to_sell(market_items: MarketItems, **kwargs) -> list[tuple[MarketItem, int]]:
        pass

    @staticmethod
    def get_cheapest_offers(market_items: MarketItems) -> list[tuple[MarketItem, int]]:
        cheapest_offers = [(item, item.prices[0])
                            for item in market_items.items 
                            if len(item.prices) > 0]
        return cheapest_offers
    

class SellAllAtPrice(SalesStrategy):

    @staticmethod
    def propose_mods_to_sell(market_items: MarketItems, 
                             sell_price: int = 0, 
                             sell_at_highest = True,
                             difference_to_highest = 0
                             ) -> list[tuple[MarketItem, int]]:
        
        if sell_at_highest:
            cheapest_offers = super(SellAllAtPrice, SellAllAtPrice).get_cheapest_offers(market_items)
            highest_price = max([price for _,price in cheapest_offers])
            return [(item, highest_price) for item in market_items.items]

        elif sell_price > 0:
            return [(item, sell_price) for item in market_items.items]
        
        else:
            raise ValueError("sell_price must be > 0 or sell_at_highest must be set to True")


    #sell


class SellMostProfitable(SalesStrategy):
    pass