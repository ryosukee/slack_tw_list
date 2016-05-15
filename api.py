import requests
from requests_oauthlib import OAuth1
from configparser import ConfigParser
import json


class API:
    def __init__(self):
        self.keyf = 'keys.ini'
        self.config = ConfigParser()
        self.config.read(self.keyf)
        auth = [self.config['Key'][k] for k in ['CK', 'CS', 'AT', 'AS']]
        self.auth = OAuth1(*auth)
        self.url = 'https://api.twitter.com/1.1/'
        self.list_id = self.config['ListID']['ID']
        self.last_id = self.config['LastID']['ID']
        self.slack_url = self.config['Slack']['url']

    def get_list(self):
        url = self.url + 'lists/statuses.json'
        params = {'list_id': self.list_id, 'since_id': self.last_id, 'include_rts': 'true', 'count': 20000}
        response = requests.get(url, params=params, auth=self.auth)
        return response.json()

    def set_last_id(self, num):
        self.config['LastID']['ID'] = str(num)
        self.config.write(open(self.keyf, 'w'))

    def post2slack(self, text, name, icon_url=None,icon_emoji=None):
        if icon_url is not None:
            j = {'text': text, 'username': name, 'icon_url': icon_url}
        elif icon_emoji is not None:
            j = {'text': text, 'username': name, 'icon_emoji': icon_emoji}
        else:
            assert False, 'icon_url or icon_emoji is required'
        params = {'payload': json.dumps(j)}
        r = requests.post(self.slack_url, data=params)
