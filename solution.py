#!/usr/bin/env python

import unittest
from pprint import pprint, pformat


def expand_helper(current_path, components, doc, result):
    if not components:
        return

    component = components[0]
    if len(components) == 1:
        if component != '*' and component in doc:
            current_path.append(component)
            key = '.'.join(current_path)
            result[key] = doc[component]
            current_path.pop()
            return

    if component == '*':
        keys = doc.keys()
        for k in keys:
            current_path.append(k)
            expand_helper(current_path, components[1:], doc[k], result)
            current_path.pop()
    else:
        if component not in doc:
            return

        if not type(doc[component]) is dict:
            return

        current_path.append(component)
        expand_helper(current_path, components[1:], doc[component], result)
        current_path.pop()


# return a collection of keys matching the key expression.
def expand_keys(key, doc):
    if key == '*':
        return doc

    components = key.split('.')
    current_path = []
    result = {}
    expand_helper(current_path, components, doc, result)
    return result


class Tests(unittest.TestCase):

    def setUp(self):
        self.doc = {
            'a': {
                'b': {
                    'c': 'hello'
                },
                'd': {
                    'c': 'sup',
                    'e': {
                        'f': 'blah blah blah'
                    }
                }
            }
        }

    def test0(self):
        test = {
            'a': {
                'd': {
                    'e': {
                        'f': 'blah blah blah'
                    },
                    'c': 'sup'
                },
                'b': {
                    'c': 'hello'
                }
            }
        }
        self.assertEqual(test, self.doc)

    def test1(self):
        test = {'a.d.e.f': 'blah blah blah'}
        result = expand_keys('a.d.e.f', self.doc)
        self.assertEqual(test, result)

    def test2(self):
        test = {'a.b.c': 'hello', 'a.d.c': 'sup'}
        result = expand_keys('a.*.c', self.doc)
        self.assertEqual(test, result)

    def test3(self):
        test = {'a.d.e': {'f': 'blah blah blah'}}
        result = expand_keys('a.*.e', self.doc)
        self.assertEqual(test, result)

    def test4(self):
        test = {}
        result = expand_keys('a.b.c.e.*', self.doc)
        self.assertEqual(test, result)

    def test5(self):
        test = {'a': {'b': {'c': 'hello'}, 'd': {'c': 'sup', 'e': {'f': 'blah blah blah'}}}}
        result = expand_keys('*', self.doc)
        self.assertEqual(test, result)


if __name__ == '__main__':
    unittest.main()
