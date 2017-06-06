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
Wrapper over DSL parser from pyparsing
'''

import pyparsing as pp
import collections
import sys
import re
from tickvaultpythonapi.parsing.predicate import BasePredicate


class Parser(object):
    
    
    def __init__(self, predClass=BasePredicate):
        """
        Keyword args:
            predClass: a predicate class that has an operation object to get 
            its op_to_str attribute (ex. BasePredicate)
        """
        self.predClass = predClass
        
        self.column = pp.Word(pp.alphas+"_")('column')
        
        operations = list(self.predClass.get_op_class().op_to_str.keys())
        self.operation = pp.oneOf(operations, caseless=True)('operation')
        
        self.value = pp.Word(pp.alphanums+","+"."+"%"+"_")('value')
        self.and_ = pp.Keyword("and", caseless=True)

        self.pred = pp.Group(self.column + self.operation + self.value)
        self.parser = self.pred + pp.ZeroOrMore(pp.Suppress(self.and_) + self.pred)

    def parseString(self, toParse):
        """
        Keyword args:
            toParse: the string containing the predicates to parse
                (ex. "price > 3 and volume <= 4")
        Returns:
            a list of Predicate objects (defined by predClass)
        """
        
        if not toParse:
            return []
        
        predicates = []
        # Get list of triplets representing predicates
        parsedList = self.parser.parseString(toParse)

        # Check that the number of predicates matches what is expected
        expected = len(re.findall(' and($| )', toParse.lower())) + 1
        found = len(parsedList)
        if found != expected:
            sys.exit("Malformed predicates: One or more predicates could not be parsed\n"
                     "\tExpected: " + str(expected) + " predicates\n"
                     "\tFound: " + str(found) + " predicates")

        # Check for multiple conditions on same column
        allCols = [triplet['column'] for triplet in parsedList]
        dups = [dup for dup, count in collections.Counter(allCols).items() if count > 1]
        if dups:
            sys.exit("There are multiple conditions on the column(s): " + ",".join(dups))

        # Create predicates from triplets
        for preds in parsedList:
            predicates.append(self.predClass(preds['column'], preds['operation'], preds['value']))

        return predicates


if __name__ == '__main__':
    testList = [  # List of test strings
    # Valid identifiers
    "price > 3 and volume <= 4 and ticker = TD and exchange like X", "name=TIME_WEIGHTED_AVERAGE_SPREAD", "",
    # Not valid
    "ticker in TD,RY", "price => 3", "volume =! 4" ]
    
    p = Parser(BasePredicate)
    for text in testList:
        print ("---Test for '{0}'".format(text))
        try:
            result = p.parseString(text)
            for r in result:
                print(r.get_as_kv_pair())
        except pp.ParseException as x:
            print( "   No match: {0}".format(str(x)))
        print()