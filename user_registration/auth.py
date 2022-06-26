from google.auth.transport import requests
from google.oauth2 import id_token

class Google:

    @staticmethod
    def validate(auth_token):
        try:
            id_info = id_token.verify_oaut2_token(
                auth_token, requests.Requests()
            )

            if 'account.google.com' in id_info['iss']:
                return id_info

        except:
            return 'Invaild token or expired'