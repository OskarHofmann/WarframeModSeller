import requests
import pandas as pd
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
    return [mod.replace(' ', '_').lower() for mod in mods]

def mod_ids_to_names(mods: list[str]) -> list[str]:
    return [mod.replace('_', ' ').title() for mod in mods]


def get_mod_prices(mods: list[str]) -> dict[str, int]:
    mod_prices = {}
    mod_ids = mod_names_to_ids(mods)
    for mod in mod_ids:
        #print(MARKET_URL + f'/items/{mod_url}')
        api_response = requests.get(MARKET_URL + f'/items/{mod}/orders')
        response_json = api_response.json()
        orders = response_json['payload']['orders']
        available_orders = [order for order in orders if \
                            order['user']['status'] == 'ingame' and \
                            order['order_type'] == 'sell']
        lowest_price = min(available_orders, key= lambda x: x['platinum'])['platinum']
        mod_prices[mod] = lowest_price
        break

    #TODO: use asyncio to make calls for all mods in list

    return mod_prices




if __name__ == '__main__':
    # load_dotenv()
    mods = get_augment_mods('Red Veil')
    print(get_mod_prices(mods))