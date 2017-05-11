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
Python wrapper for TickSmith Query API - Specific to Nasdaq-Cx
'''

import ujson
from tickvaultpythonapi.client import BaseClient
from tickvaultpythonapi.auth.auth import OAuth
from tickvaultpythonapi.parsing.parse import Parser
from tickvaultpythonapi.parsing.predicate import BasePredicate


class NasdaqCxClient(BaseClient):
        
    def __init__(self, user_name, secret_key, base_url="https://nasdaq-cx.ticksmith.com"):
        '''
        Keyword args:
            user_name -- TickSmith username
            secret_key -- API key, found on the "Manage API Key" page
        '''
        self.base_url = base_url
        self.api_url = self.base_url + "/api/v1"
        self.user_name = user_name
        self.secret_key = secret_key

        self.auth = OAuth(self.get_token(self.base_url, self.user_name, self.secret_key))

    def _get_datasets(self):
        '''
        Gets all Nasdaq-Cx datasets
        '''

        endpoint = self.api_url + "/dataset/list/CX"
        return ujson.loads(self.query(endpoint=endpoint, auth=self.auth))

    def datasets(self):
        """
        Lists the names of all Nasdaq-Cx datasets

        Returns:
            A list of available datasets
        """

        return [ds['dataset'] for ds in self._get_datasets()]

    def describe(self, dataset):
        '''
        Describes the structure of a particular Nasdaq-Cx dataset

        Returns:
            A dict that maps a column to its type
        '''

        cols={}

        for ds in self._get_datasets():
            if ds['dataset'] == dataset.lower():
                for col in ujson.loads(ds['structure']):
                    cols[col['column']] = col['type']

        return cols

    def _query_dataset(self, dataset, source, tickers, start_time, end_time, fields, predicates="", limit=200):
        """
        Queries a Nasdaq-Cx dataset with the given arguments

        Keyword args:
            dataset -- Hits/Rollups/EOD
            source -- Exchange to query
            tickers -- One or more tickers (can be string or list)
            start_time -- Start time of query (format: yyyymmddhhhMMss)
            end_time -- End time of query (format: yyyymmddhhhMMss)
            fields -- One or more columns to return (can be string or list)
            predicates -- String of predicates (format: "column op value [and column op value]")
            limit -- Max number of records to return (default = 200)

        Returns:
            The result of the query as a JSON list
        """

        # Define endpoint pattern and the dictionary containing k-v pairs to replace the placeholders
        endpoint_pattern = self.api_url + "/dataset/query/cx/{ds}/{src}/{tick}/{time}"
        replace_dict = {'ds': dataset, 
                        'src': source, 
                        'tick': self._list_to_str("tickers", tickers), 
                        'time': start_time}
        
        # Define params (without predicates)
        params = {'endTime': end_time, 
                  'fields': self._str_to_list("fields", fields), 
                  'limit': limit}
        
        # Parse predicates 
        parsedPredicates = Parser(BasePredicate).parseString(predicates)
        
        result = self.run_query(pattern=endpoint_pattern,
                                replace_dict=replace_dict,
                                auth=self.auth,
                                params=params, 
                                predicates=parsedPredicates)
        
        return [ujson.loads(x) for x in result.split("\n") if x]    
    
    def query_hits(self, source, tickers, start_time, end_time, fields, predicates="", limit=200):
        """
        Queries the HITS Nasdaq-Cx dataset with the given arguments
    
        Keyword args:
            source -- Exchange to query
            tickers -- One or more tickers (can be string or list)
            start_time -- Start time of query (format: yyyymmddhhhMMss)
            end_time -- End time of query (format: yyyymmddhhhMMss)
            fields -- One or more columns to return (can be string or list)
            predicates -- String of predicates (format: "column op value [and column op value]")
            limit -- Max number of records to return (default = 200)
    
        Returns:
            The result of the query as a JSON list
        """
        return self._query_dataset("cx_hits", source, tickers, start_time, end_time, fields, predicates, limit)

    def query_rollup_1s(self, source, tickers, start_time, end_time, fields, predicates="", limit=200):
        """
        Queries the 1 second Rollup Nasdaq-Cx dataset with the given arguments
    
        Keyword args:
            source -- Exchange to query
            tickers -- One or more tickers (can be string or list)
            start_time -- Start time of query (format: yyyymmddhhhMMss)
            end_time -- End time of query (format: yyyymmddhhhMMss)
            fields -- One or more columns to return (can be string or list)
            predicates -- String of predicates (format: "column op value [and column op value]")
            limit -- Max number of records to return (default = 200)
    
        Returns:
            The result of the query as a JSON list
        """
        return self._query_dataset("cx_rollup_1000", source, tickers, start_time, end_time, fields, predicates, limit)
    
    def query_rollup_60s(self, source, tickers, start_time, end_time, fields, predicates="", limit=200):
        """
        Queries the 60 second Rollup Nasdaq-Cx dataset with the given arguments
    
        Keyword args:
            source -- Exchange to query
            tickers -- One or more tickers (can be string or list)
            start_time -- Start time of query (format: yyyymmddhhhMMss)
            end_time -- End time of query (format: yyyymmddhhhMMss)
            fields -- One or more columns to return (can be string or list)
            predicates -- String of predicates (format: "column op value [and column op value]")
            limit -- Max number of records to return (default = 200)
    
        Returns:
            The result of the query as a JSON list
        """
        return self._query_dataset("cx_rollup_60000", source, tickers, start_time, end_time, fields, predicates, limit)
    
    def query_eod_stats(self, source, tickers, start_time, end_time, fields, predicates="", limit=200):
        """
        Queries the EOD Stats Nasdaq-Cx dataset with the given arguments
    
        Keyword args:
            source -- Exchange to query
            tickers -- One or more tickers (can be string or list)
            start_time -- Start time of query (format: yyyymmddhhhMMss)
            end_time -- End time of query (format: yyyymmddhhhMMss)
            fields -- One or more columns to return (can be string or list)
            predicates -- String of predicates (format: "column op value [and column op value]")
            limit -- Max number of records to return (default = 200)
    
        Returns:
            The result of the query as a JSON list
        """
        return self._query_dataset("cx_eod_stats", source, tickers, start_time, end_time, fields, predicates, limit)

