from weibo_api import Client

from bs4 import BeautifulSoup
import execjs
import requests

_client: Client
_mHOST = "https://m.weibo.cn"


def init(client: Client):
    global _client
    _client = client


def get_hometimeline():
    result = []

    home_timeline = _client.get('statuses/home_timeline')
    statuses = home_timeline['statuses']

    def check_and_merge(status):
        result.append(status)

    [check_and_merge(st) for st in statuses]
    pass


def get_weibo_details_by_id(id):
    url = "{}/detail/{}".format(_mHOST, id)
    res = _client._session.get(url).text

    soup = BeautifulSoup(res, 'html.parser')
    body_tag = soup.body
    script_tag = body_tag.find_all('script')[1].string
    script_tag += '''
    function get_var() {
        return $render_data;
    }
    '''
    ctx = execjs.compile(script_tag)
    res = ctx.call('get_var')

    return res
