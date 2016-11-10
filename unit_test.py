#!/usr/bin/env python
# coding=utf-8
# author:bo ma

import unittest
import crawl3
from urllib.parse import urlparse


class CrawlTest(unittest.TestCase):
    def setUp(self):
        self.url = 'example.com'
        self.correctUrl = 'http://www.google.com'
        self.wrongUrl = 'http://www.example'
        self.html = '<a href = "tst.html" />'
        self.timeOut = 20
        self.level = 10
        self.retr = crawl3.Retriever(self.url, self.timeOut)

    def tearDown(self):
        pass

    def testUrlValidate(self):
        # validate url timeout and level
        self.assertTrue(crawl3.inputValidat(self.correctUrl, self.timeOut, self.level))
        # validate wrong url
        self.assertFalse(crawl3.inputValidat(self.wrongUrl, self.timeOut, self.level))
        # validate wrong timeOut
        self.assertFalse(crawl3.inputValidat(self.correctUrl, 'ff', self.level))
        # validate wrong level
        self.assertFalse(crawl3.inputValidat(self.correctUrl, self.timeOut, 'ff'))


if __name__ == '__main__':
    unittest.main()
