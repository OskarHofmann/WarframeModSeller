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
                             sell_at_highest: bool = True,
                             difference_to_highest: int = 0
                             ) -> list[tuple[MarketItem, int]]:
        
        if sell_at_highest:
            cheapest_offers = super(SellAllAtPrice, SellAllAtPrice).get_cheapest_offers(market_items) # two-argument super required due to acces to static method
            highest_price = max([price for _,price in cheapest_offers])
            price_to_sell_at = highest_price - difference_to_highest
            return [(item, price_to_sell_at) for item in market_items.items]

        elif sell_price > 0:
            return [(item, sell_price) for item in market_items.items]
        
        else:
            raise ValueError("sell_price must be > 0 or sell_at_highest must be set to True")


    #sell


class SellMostProfitable(SalesStrategy):
    
    @staticmethod
    def propose_mods_to_sell(market_items: MarketItems, 
                             difference_to_highest: int = 0, 
                             sell_below_current_cheapest: bool = False
                             ) -> list[tuple[MarketItem, int]]:
    
        cheapest_offers = super(SellAllAtPrice, SellAllAtPrice).get_cheapest_offers(market_items) # two-argument super required due to acces to static method
        highest_price = max([price for _,price in cheapest_offers])

        items_to_sell = [(item, price - 1 * sell_below_current_cheapest) 
                         for (item, price) in cheapest_offers 
                         if price >= (highest_price - difference_to_highest)]
        
        return items_to_sell

