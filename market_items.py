from dataclasses import dataclass

@dataclass
class MarketItem:
    item_name: str = ""
    url_name: str = ""
    id: str = ""
    prices: list[int] = []

    def __post_init__(self) -> None:
        if len(self.item_name) > 0 and self.url_name == "":
            self._create_url_name()

    # create url name by replacing spaces with underscores and remove apostrophe
    def _create_url_name(self) -> None:
        self. url_name = self.item_name.replace(' ', '_').replace("'", "").lower()

    def get_market_prices(self):
        pass
        


@dataclass
class MarketItems:
    items: list[MarketItem] = []


    




