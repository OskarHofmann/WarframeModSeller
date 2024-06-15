from dataclasses import dataclass

@dataclass
class WFMarketUser():
    email: str = ""
    password: str = ""
    name: str = ""
    id: str = ""

class WFMarketAuth():
    pass


# for testing
if __name__ == '__main__':
    import sys
    sys.path.insert(0, '.')
    
    import parameters as params
    import os
    from dotenv import load_dotenv
    import requests

    load_dotenv()
    wf_market_email = os.environ['WFM_EMAIL']
    wf_market_password = os.environ['WFM_PASSWORD']

    api_url = params.MARKET_URL + '/auth/signin'

    jwt_request = requests.get(api_url)
    jwt = jwt_request.cookies["JWT"]


    data = {
        "auth_type": "header",
        "email": wf_market_email,
        "password": wf_market_password
        }
    header = {
        "Authorization": jwt
    }
    
    response = requests.post(api_url, json=data, headers=header)
    print(response.text)