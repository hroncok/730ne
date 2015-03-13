import json
from social.backends.oauth import BaseOAuth2


class FITOAuth2(BaseOAuth2):
    name = 'fit'
    AUTHORIZATION_URL = 'https://auth.fit.cvut.cz/oauth/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://auth.fit.cvut.cz/oauth/oauth/token'
    ACCESS_TOKEN_METHOD = 'POST'
    ID_KEY = 'user_id'
    EXTRA_DATA = [('roles', 'roles')]

    def get_user_details(self, response):
        """Return user details from FIT account"""
        return {'username': response.get('user_id'),
                'email': response.get('user_email'),
                'first_name': response.get('firstName'),
                'last_name': response.get('lastName')}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = 'https://auth.fit.cvut.cz/oauth/api/v1/tokeninfo'
        try:
            data = self.get_json(url, params={'token': access_token})
        except ValueError:
            return None
        usermap_url = 'https://kosapi.fit.cvut.cz/usermap/v1/people/' + data['user_id']
        try:
            usermap = self.get_json(
                usermap_url, headers={'Authorization': 'Bearer %s' % access_token})
            data.update(usermap)
        except ValueError:
            pass
        return data


def get_roles(user):
    """Gets latest roles of given user"""
    extra_data = user.social_auth.latest(field_name='pk').extra_data
    try:
        return extra_data['roles']
    except KeyError:
        return []
