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
        if len(self.item_name) > 0 and self.url_name == "":
            self._create_url_name()

    # create url name by replacing spaces with underscores and remove apostrophe
    def _create_url_name(self) -> None:
        self. url_name = self.item_name.replace(' ', '_').replace("'", "").lower()

    async def get_order_prices(self, item_id: str, session: aiohttp.ClientSession, n_tries: int = 20) -> list[int] :
        api_url = params.MARKET_URL + f'/items/{item_id}/orders'
        # try n_tries times, before giving up
        for _ in range(n_tries):
            async with session.get(api_url) as response:
                if response.status != 200:
                    await asyncio.sleep(1)
                    continue
                response_json = await response.json(content_type=None)

            orders = response_json['payload']['orders']
            break
        else:
            print(f'API call for {item_id} failed.')
            return []

        available_orders = [order for order in orders if \
                            order['user']['status'] == 'ingame' and \
                            order['order_type'] == 'sell']
        prices = [order['platinum'] for order in available_orders]
        prices.sort()
        return prices
        


@dataclass
class MarketItems:
    items: list[MarketItem] = []

    # async def get_mod_prices(self, mods: list[str]) -> dict[str, list[int]]:
    #     mod_ids = mod_names_to_ids(mods)
    #     async with aiohttp.ClientSession() as session:
    #         tasks = [get_order_prices(mod_id, session) for mod_id in mod_ids]
    #         print('Gathering mod prices from WarframeMarket. Please wait.')
    #         results = await asyncio.gather(*tasks)          

    #     # gather returns in same order as in the task order (i.e. the same order as in mod_ids)
    #     return dict(zip(mod_ids, results))


    




