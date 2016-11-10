#!/usr/bin/env python
# coding=utf-8
# author:bo ma

import unittest
import crawl3


class CrawlMockServerTest(unittest.TestCase):
    #   please run the mock server before you run this test case
    def setUp(self):
        self.url = 'http://127.0.0.1:5000/testpage/'
        self.timeout = 20
        self.deeplevel = 6
        self.cr = crawl3.Crawler(self.url, self.timeout, self.deeplevel)
        self.re = crawl3.Retriever(self.url, self.timeout)

    def tearDown(self):
        pass

    def testCrawlServerBehaviour(self):
        # test total output number
        self.assertEqual(4, len(self.cr.go()))
        # testoage only has 1 assets. It is used to test whether getting correct static assets number
        self.assertEqual(1, len(self.re.parseAndGetStatic(self.url)))
        # page1 has 4 assets. It is used to test whether getting correct static assets number
        self.assertEqual(4, len(self.re.parseAndGetStatic('http://127.0.0.1:5000/p1')))
        # root page testpage has 3 children page
        self.assertEqual(3, len(self.re.parseAndGetLinks()))


if __name__ == '__main__':
    unittest.main()
