import json
import requests

from core.exceptions import InternalError


class Http:
    """Http Call Header"""
    HEADER = {'Accept': 'application/json'}

    """
        Generic Http request function

        param method: 'GET', 'POST' or 'PUT'
        param url: the requested URL
        param headers: the headers
        data: the request boy, if needed

        raises InternalError: if status code > 400 or JSON parsing error
        raises Connection: if connection fails

        returns: the request's response content

    """

    def request(self, method, url, headers, data=None):
        try:
            r = requests.request(method=method, url=url, headers=headers, data=data)
            print(r.status_code)
            content = r.json()
            if r.status_code >= 400:
                raise InternalError
            print(content)
        except json.decoder.JSONDecodeError:
            raise InternalError
        except requests.exceptions.ConnectionError:
            raise ConnectionError
        return content

    """GET function, calls with the right arguments request()"""

    def get(self, url):
        return self.request(method='GET', url=url, headers=self.HEADER)

    """GET function, calls with the right arguments request() """

    def post(self, url, data=None):
        return self.request(method='POST', url=url, headers=self.HEADER, data=data)

    """PUT function, calls with the right arguments request() """

    def put(self, url, data=None):
        return self.request(method='PUT', url=url, headers=self.HEADER, data=data)
