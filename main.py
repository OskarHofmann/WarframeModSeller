import requests
import pandas as pd
# from dotenv import load_dotenv
# import unicodedata


def get_augment_mods(syndicate = None, replace_special_whitespaces = True) -> list[str]:
    url= 'https://warframe.fandom.com/wiki/Warframe_Augment_Mods/PvE'
    html = requests.get(url).content
    df = pd.read_html(html)[0]

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




if __name__ == '__main__':
    # load_dotenv()
    print(get_augment_mods('Red Veil'))