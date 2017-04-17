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
Provides reusable query structure
'''

import sys
from tickvaultpythonapi.parsing.operation import Operation, BaseOperation


class Predicate(object):

    key = ""
    operation = ""
    value = ""
    opClass = Operation()  # Defaults to operation, which allows no operations

    def __init__(self, key, op, val):
        """
        Assign key, operation and value
        """
        self.key = key
        self.operation = self.get_valid_op(op)
        self.value = val

    def get_valid_op(self, op):
        """
        Uses opClass (subtypes of Operation) to determine whether the
        given operation is allowed. If it is, it returns the string that
        will be appended to the key name (ex. '>' results in 'Gte', so that the
        query will be 'keyGte')
        """
        try:
            return self.opClass.get_str(op)
        except Exception as e:
            sys.exit(e)

    def get_as_kv_pair(self):
        """
        Get as key-value pair
        (ex. key = 'price', operation = '!=', value = '50',
        result= {"priceNeq" : "50"})
        """
        return {self.key + self.operation : str(self.value)}

    def get_as_tuple(self):
        """
        Get as tuple
        (ex. key = 'price', operation = '!=', value = '50',
        result= ("priceNeq","50")
        """
        return (self.key + self.operation, str(self.value))

    def __str__(self):
        """
        @Overrride of __str__()
        """
        return self.key + self.operation + "=" + str(self.value)


class BasePredicate(Predicate):

    # Replace opClass with BaseOperation
    opClass = BaseOperation()
        
    # Getter for opClass
    @classmethod
    def get_op_class(self):
        return self.opClass


if __name__ == '__main__':
    params = {"param1":"value1"}
    bp = BasePredicate("line_type", "=", "T,E")
    print(bp.opClass.op_to_str)
    p = bp.get_as_kv_pair()
    params = {**params, **p}
    print(params)
    print(BasePredicate("price", ">", 7).get_as_kv_pair())
    print(BasePredicate("price", ">=", "a"))
    print(BasePredicate("price", "<=", "7").get_as_kv_pair())
    print(BasePredicate("price", "!=", "7"))
