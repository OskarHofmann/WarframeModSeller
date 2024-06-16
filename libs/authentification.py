import parameters as params
import requests


class WFMarketAuth():
    
    def __init__(self) -> None:
        #get JSON web token (JWT) from WarframeMarket for API calls that require user authentification
        jwt_request = requests.get(params.MARKET_URL)
        self.jwt = jwt_request.cookies["JWT"]


    def login_user(self, email: str, password:str) -> None:
        signin_url = params.MARKET_URL + '/auth/signin'
        login_data = {
            "auth_type": "header",
            "email": email,
            "password": password
        }
        login_header = {"Authorization": self.jwt}

        response = requests.post(signin_url, json=login_data, headers=login_header)
        
        if response.status_code != 200:
            raise requests.ConnectionError("Could not login with provided credentials. Please verify credentials or check if WarframeMarket.com is available.")
        
        user_data = response.json()["payload"]["user"]
        self.user_id = user_data["id"]
        self.user_name = user_data["ingame_name"]
