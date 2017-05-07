#!/usr/bin/env python3

"""
Quick and dirty Python test for potential developers at Common Code

  - implement the 4 functions in the solution.py file
  - all the tests in this file should pass
  - you can run the tests by executing this file
"""

import unittest
from datetime import date

from solution import sort_list, rgb_to_hex, get_github_members, get_ssl_expiry


class WorkAtCommonCodeAsADeveloperTestCase(unittest.TestCase):

    def test_sort_list(self):
        # self.assertEqual(sort_list([1, 2, 3, 4]), [1, 2, 3, 4])
        self.assertEqual(sort_list([1, 12, 3, -5]), [-5, 1, 3, 12])
        self.assertEqual(
            sort_list(['Guido', 'Fred', 'Georg', 'Benjamin']),
            ['Benjamin', 'Fred', 'Georg', 'Guido']
        )

    def test_rgb_to_hex(self):
        self.assertEqual(rgb_to_hex(0, 0, 0), '#000')
        self.assertEqual(rgb_to_hex(214, 51, 108), '#d6336c')
        self.assertEqual(rgb_to_hex(66, 99, 235), '#4263eb')
        self.assertEqual(rgb_to_hex(255, 232, 204), '#ffe8cc')
        self.assertEqual(rgb_to_hex(136, 34, 170), '#82a')

    def test_get_github_members(self):
        # NOTE: The answers here is correct at time of writing, feel free to
        # update this if the count on https://github.com/commoncode changes
        self.assertEqual(get_github_members('commoncode'), 12)
        self.assertEqual(get_github_members('melbdjango'), 2)
        self.assertTrue(get_github_members('Github') > 150)

    def test_get_ssl_expiry(self):
        self.assertEqual(get_ssl_expiry('github.com'), date(2018, 5, 17))
        self.assertTrue(
            (date.today() - get_ssl_expiry('commoncode.io')).days < 0
        )


if __name__ == '__main__':
    unittest.main()
