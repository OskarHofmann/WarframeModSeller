from dataclasses import dataclass
import asyncio, aiohttp
import parameters as params

@dataclass
class MarketItem:
    item_name: str = ""
    url_name: str = ""
    id: str = ""
    prices: list[int] = []

    def __post_init__(self) -> None:
        if self.item_name and not self.url_name:
            self._create_url_name()

    # create url name by replacing spaces with underscores and remove apostrophe
    def _create_url_name(self) -> None:
        self. url_name = self.item_name.replace(' ', '_').replace("'", "").lower()

    async def get_order_prices(self, session: aiohttp.ClientSession, n_tries: int = 20) -> None :
        api_url = params.MARKET_URL + f'/items/{self.url_name}/orders'

        # if item id is unknown ask API to also provide additional item information
        api_params = {}
        if not id:
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
    items: list[MarketItem] = []

    async def get_item_prices(self) -> None:
        async with aiohttp.ClientSession() as session:
            tasks = [item.get_order_prices(session, params.NUMBER_OF_API_CALL_RETRIES) for item in self.items]
            print('Gathering mod prices from WarframeMarket. Please wait.')
            asyncio.run(*tasks)          



    




