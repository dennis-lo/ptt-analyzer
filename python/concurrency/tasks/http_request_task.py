""" A class that represents an HTTP request """

import json
import urllib.parse

from ..task import Task

class HttpRequestTask(Task):
    def __init__(self, url, data=None, headers=None, method='POST', \
            content_type='form', charset='utf-8'):
        """ Instantiation

        Arguments:
            url -           URL of the HTTP request
            data -          A dictionary of request params
            headers -       A map of request headers
            method -        Request method, e.g. GET, POST, etc.
            content_type -  Content-type, either form or json
            charset -       Charset of request and response messages
        """
        super().__init__()
        self.url = url
        self.data = data
        self.headers = headers
        self.method = method
        self.content_type = content_type
        self.charset = charset

        if not self.headers:
            # Init headers
            if self.headers is None:
                self.headers = {}

            # Default headers
            self.headers['User-Agent'] = \
                    'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'

            if data:
                # Input data provided, include content-type and charset
                if not content_type or content_type == 'form':
                    self.headers['Content-Type'] = \
                            f'application/x-www-form-urlencoded; charset={charset}'

                elif content_type == 'json':
                    self.headers['Content-Type'] = \
                            f'application/json; charset={charset}'


    def get_data(self):
        """ Returns encoded input content """
        ret_data = None

        # Check input params
        if self.data:
            if not self.content_type or self.content_type == 'form':
                # Form data
                ret_data = urllib.parse.urlencode(self.data, \
                        encoding=self.charset, quote_via=urllib.parse.quote)

            elif self.content_type == 'json':
                # JSON
                ret_data = json.dumps(self.data, separators=(',', ':'))

        # Encode content
        if ret_data:
            ret_data = ret_data.encode(self.charset)

        # Return result
        return ret_data

