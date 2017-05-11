#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2017 TickSmith Corp.
#
# Licensed under the MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


'''
Python wrapper for TickSmith Query API
'''

import requests
import ujson
import pandas as pd
from tickvaultpythonapi.parsing.predicate import Predicate


class BaseClient(object):

    def _except_on_empty_input(self, value, field):
        if not value:
            raise Exception("Please provide a value for the field : %s" % field)
    
    def _str_to_list(self, field_name, to_convert):
        if isinstance(to_convert, str):
            return to_convert.split(",")
        elif isinstance(to_convert, list):
            return to_convert
        else:
            raise Exception("Fields needs to be a list or a string")

    def _list_to_str(self, field_name, to_convert):    
        if isinstance(to_convert, list):
            return ','.join(map(str, to_convert))
        elif isinstance(to_convert, str):
            return to_convert
        else:
            raise Exception("Tickers needs to be a list or a string")
    
    def get_token(self, url, user_name, secret_key):
        """
        Calls https://<URL>/sso/token with the provided user_name
            and api_key to generate the access token used to make more requests

        Keyword args:
            url -- URL of the server (ex. 'https://nasdaq-cx.ticksmith.com')
            user_name -- TickSmith username
            secret_key -- API key, found on the "Manage API Key" page

        Returns:
            The access token used to make further requests
        """

        # check for empty input
        self._except_on_empty_input(url, "url")
        self._except_on_empty_input(user_name, "username")
        self._except_on_empty_input(secret_key, "api key")

        endpoint = "{url}/sso/token".format(url=url)
        headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "Accept": "application/json"}
        data = {"grant_type": "client_credentials"}

        try:
            response = requests.post(endpoint, headers=headers, 
                                     data=data, auth=(user_name, secret_key))
            # raise http errors so we can reraise if they happen
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
            raise
        except requests.exceptions.ConnectionError as e:
            print(e.args[0].args[0])
            raise
        except Exception as e:
            print(e)
            raise

        # response.text is a JSON object, with the token in the "access_token" field
        jObj = ujson.loads(response.text)
        return jObj["access_token"]


    def run_query(self, pattern, replace_dict, auth, params="", predicates=""):
        '''
        Prepares endpoint; populates params with predicates; calls 'query'
        
        Keyword args:
            pattern -- Endpoint pattern with {} placeholders (ex. .../api/{dataset})
            replace_dict -- Dict used to replace placeholders. Keys must match placeholder names 
            params -- Dict of params to query
            predicates -- List of predicate objects, already parsed from their string representations
            auth -- Auth object to use (BasicAuth, OAuth, etc.)
            
        Returns:
            The result of calling 'query'
        '''
        endpoint = pattern.format(**replace_dict)

        # Convert predicates to their tuple representations and add them to params
        if predicates:
            if not params:
                params = {}
            preds = dict(list(map(Predicate.get_as_tuple, predicates)))
            params = {**params, **preds}

        return self.query(endpoint=endpoint, auth=auth, params=params)

    def query(self, endpoint, auth, params=""):
        """
        Queries a given endpoint

        Keyword args:
            endpoint -- Endpoint to query (ex. 'https://nasdaq-cx.ticksmith.com/api/v1/dataset/query/...')
            params -- Dictionary of params, properly formatted
            auth -- The type of auth to use

        Returns:
            The result of the query
        """

        try:
            response = requests.get(endpoint, params=params, auth=auth)
            # raise http errors so we can raise if they happen
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
            raise
        except requests.exceptions.ConnectionError as e:
            print(e.args[0].args[0])
            raise
        except Exception as e:
            print(e)
            raise

        # raise exception if response is empty or filled with nulls
        if not response or not str(response.text).rstrip('\x00'):
            raise Exception("Request returned no results")
        return response.text

    def as_dataframe(self, in_list, index="ts"):
        '''
        Converts a json list to a pandas DataFrame

        Keyword args:
            in_list -- A list of json objects

        Returns:
            A pandas DataFrame indexed by timestamp
        '''
        df = pd.DataFrame(in_list).set_index(index)
        df.index = pd.DatetimeIndex(df.index)
        return df
