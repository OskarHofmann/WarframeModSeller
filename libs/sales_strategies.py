from abc import ABC, abstractmethod
from .market_items import MarketItems, ItemWithPrice

class SalesStrategy(ABC):

    @staticmethod
    @abstractmethod
    def propose_mods_to_sell(market_items: MarketItems, **kwargs) -> list[ItemWithPrice]:
        pass

    @staticmethod
    def get_cheapest_offers(market_items: MarketItems) -> list[ItemWithPrice]:
        cheapest_offers = [ItemWithPrice(item=item, price=item.prices[0])
                            for item in market_items.items 
                            if len(item.prices) > 0]
        return cheapest_offers
    

class SellAllAtPrice(SalesStrategy):

    @staticmethod
    def propose_mods_to_sell(market_items: MarketItems, 
                             sell_price: int = 0, 
                             sell_at_highest: bool = True,
                             difference_to_highest: int = 0
                             ) -> list[ItemWithPrice]:
        
        if sell_at_highest:
            cheapest_offers = super(SellAllAtPrice, SellAllAtPrice).get_cheapest_offers(market_items) # two-argument super required due to acces to static method
            highest_price = max([item.price for item in cheapest_offers])
            price_to_sell_at = highest_price - difference_to_highest
            return [ItemWithPrice(item=item, price=price_to_sell_at) for item in market_items.items]

        elif sell_price > 0:
            return [ItemWithPrice(item=item, price=sell_price) for item in market_items.items]
        
        else:
            raise ValueError("sell_price must be > 0 or sell_at_highest must be set to True")



class SellMostProfitable(SalesStrategy):
    
    @staticmethod
    def propose_mods_to_sell(market_items: MarketItems, 
                             difference_to_highest: int = 0, 
                             sell_below_current_cheapest: bool = False
                             ) -> list[ItemWithPrice]:
    
        cheapest_offers = super(SellAllAtPrice, SellAllAtPrice).get_cheapest_offers(market_items) # two-argument super required due to acces to static method
        highest_price = max([item.price for item in cheapest_offers])

        items_to_sell = [ItemWithPrice(item=item.item, price= (item.price - 1 * sell_below_current_cheapest) )  
                         for item in cheapest_offers 
                         if item.price >= (highest_price - difference_to_highest)]
        
        return items_to_sell

