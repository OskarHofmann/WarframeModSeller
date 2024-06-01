import parameters as params
import pandas as pd

# gets all the augmentation mods for a given syndicate from the Warframe wiki
def get_augment_mods(syndicate: str | None = None, replace_special_whitespaces: bool = True) -> list[str]:
    df = pd.read_html(params.AUGMENT_MODS_URL)[0]

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