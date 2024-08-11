from dataclasses import dataclass, field
import asyncio, aiohttp, requests
import parameters as params

@dataclass
class MarketItem:
    item_name: str = ""
    url_name: str = ""
    id: str = ""
    prices: list[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.item_name and not self.url_name:
            self._create_url_name()

    # create url name by replacing spaces with underscores and removing apostrophes
    def _create_url_name(self) -> None:
        self. url_name = self.item_name.replace(' ', '_').replace("'", "").lower()

    def look_up_id(self) -> None:
        api_url = params.MARKET_URL + f'/items/{self.url_name}'
        response = requests.get(api_url)
        self. id = response.json()["payload"]["item"]["id"]

    async def get_order_prices(self, session: aiohttp.ClientSession, n_tries: int = 20) -> None :
        api_url = params.MARKET_URL + f'/items/{self.url_name}/orders'

        # if item id is unknown ask API to also provide additional item information
        api_params = {}
        if not self.id:
            api_params = {'include': 'item'}

        # try n_tries times, before giving up
        for _ in range(n_tries):
            async with session.get(url=api_url, params=api_params) as response:
                if response.status != 200:
                    await asyncio.sleep(1)
                    continue
                response_json = await response.json(content_type=None)

            orders = response_json['payload']['orders']
            # if item has no id, additional item information was requested and should be provided under the 'include' key
            if 'include' in response_json:
                self.id = response_json['include']['item']['id']
            break
        else:
            print(f'API call for {self.item_name} failed.')

        available_orders = [order for order in orders if \
                            order['user']['status'] == 'ingame' and \
                            order['order_type'] == 'sell']
        prices = [order['platinum'] for order in available_orders]
        prices.sort()
        
        self.prices = prices
        


@dataclass
class MarketItems:
    items: list[MarketItem] = field(default_factory=list)

    def add_items_from_item_names(self, item_names: list[str]) -> None:
        new_items = [MarketItem(item_name=item_name) for item_name in item_names]
        self.items.extend(new_items)

    def get_item_prices(self) -> None:
        asyncio.run(self._get_item_prices_async())

    async def _get_item_prices_async(self) -> None:
        async with aiohttp.ClientSession() as session:
            tasks = [item.get_order_prices(session, params.NUMBER_OF_API_CALL_RETRIES) for item in self.items]
            print('Gathering mod prices from WarframeMarket. Please wait.')
            await asyncio.gather(*tasks)          



@dataclass
class ItemWithPrice:
    item: MarketItem
    price: int




