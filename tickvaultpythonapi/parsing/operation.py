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
Defines base operations that can be used in predicates
'''

class Operation(object):

    """
        No operations are allowed with the default Operation object

        When populated, the dictionary is:
            {"operation ascii character" : "string representing operation"}
        ex.
            {">=":"Gte"}
    """
    op_to_str = {}

    def _is_valid(self, operation):
        """
        Check if given operation exists in dict
        """
        return operation.lower() in self.op_to_str

    def get_str(self, operation):
        """
        Return the string representing the operation
        """
        if not self._is_valid(operation):
            raise Exception("Invalid operator: " + operation)
        return self.op_to_str[operation.lower()]


class BaseOperation(Operation):

    # Replace op_to_str with the allowed base operations
    op_to_str = {
            '<': 'Lt',
            '<=': 'Lte',
            '>': 'Gt',
            '>=': 'Gte',
            '!=': 'Neq',
            '=': 'Eq',
            '==': 'Eq',
            'like': 'Like'
            }


if __name__ == '__main__':
    p = BaseOperation()
    print(list(p.op_to_str.keys()))
    print(p._is_valid("in"))
