import pandas as pd
import asyncio, aiohttp
# from dotenv import load_dotenv
# import unicodedata

MARKET_URL = 'https://api.warframe.market/v1'


def get_augment_mods(syndicate: str | None = None, replace_special_whitespaces: bool = True) -> list[str]:
    url= 'https://warframe.fandom.com/wiki/Warframe_Augment_Mods/PvE'
    df = pd.read_html(url)[0]

    # the DataFrame contains all mods seperated by spaces (individual words of a mod are split via non-break space \xa0 ) 
    augment_mods = []
    for idx, row in df.iterrows():
        # check if row is for given syndicate (row contains name with non-break space \xa0)
        if syndicate and not (syndicate.replace(' ', '\xa0') in row['Favored Syndicates']):
            continue
        mod_words = row['Augment Mods'].split(' ')
        augment_mods.extend(mod_words)

    if replace_special_whitespaces:
        # replace non-break space with normal spaces (normalized equivalent)
        # augment_mods = [unicodedata.normalize('NFKD', mod) for mod in augment_mods]
        augment_mods = [mod.replace('\xa0', ' ') for mod in augment_mods]
    
    return augment_mods


def mod_names_to_ids(mods: list[str]) -> list[str]:
    return [mod.replace(' ', '_').replace("'", "").lower() for mod in mods]

# def mod_ids_to_names(mods: list[str]) -> list[str]:
#     return [mod.replace('_', ' ').title() for mod in mods]


async def get_order_prices(item_id: str, session: aiohttp.ClientSession, n_tries: int = 10) -> list[int] :
    api_url = MARKET_URL + f'/items/{item_id}/orders'
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


async def get_mod_prices(mods: list[str]) -> dict[str, list[int]]:
    mod_ids = mod_names_to_ids(mods)
    async with aiohttp.ClientSession() as session:
        tasks = [get_order_prices(mod_id, session) for mod_id in mod_ids]
        print('Gathering mod prices from WarframeMarket. Please wait.')
        results = await asyncio.gather(*tasks)          

    # gather returns in same order as in the task order (i.e. the same order as in mod_ids)
    return dict(zip(mod_ids, results))


if __name__ == '__main__':
    # load_dotenv()
    mods = get_augment_mods('Red Veil')
    mod_prices = asyncio.run(get_mod_prices(mods))