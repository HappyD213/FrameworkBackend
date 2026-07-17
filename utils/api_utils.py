from requests import Session


class ApiUtils:
    def __init__(self, url, headers=None):
        if headers is None:
            headers = {}

        self.session = Session()
        self.session.headers.update(headers)
        self.url = url

    def get(self, endpoint_url, **kwargs):
        response = self.session.get(self.url + endpoint_url, **kwargs)
        return response

    def post(self, endpoint_url, data=None, json=None, **kwargs):
        response = self.session.post(self.url + endpoint_url, data=data, json=json, **kwargs)
        return response
