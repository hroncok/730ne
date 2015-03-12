import json
from social.backends.oauth import BaseOAuth2


class FITOAuth2(BaseOAuth2):
    name = 'fit'
    AUTHORIZATION_URL = 'https://auth.fit.cvut.cz/oauth/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://auth.fit.cvut.cz/oauth/oauth/token'
    ACCESS_TOKEN_METHOD = 'POST'
    ID_KEY = 'user_id'

    def get_user_details(self, response):
        """Return user details from FIT account"""
        return {'username': response.get('user_id'),
                'email': response.get('user_email')}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = 'https://auth.fit.cvut.cz/oauth/api/v1/tokeninfo'
        try:
            return self.get_json(url, params={'token': access_token})
        except ValueError:
            return None
