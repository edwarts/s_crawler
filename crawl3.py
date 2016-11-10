#!/usr/bin/env python
# coding=utf-8
# author:bo ma

# This is for test of gocardless and a smal simple crawler using python 3

from sys import argv
from urllib.request import urlopen
from urllib.parse import urlparse, urljoin, urlsplit, quote, urlunsplit
from bs4 import BeautifulSoup
from time import sleep
from collections import deque
import json


# This class is used to download web pages
class Retriever(object):
    def __init__(self, url, timeout):
        self.url = url
        self.timeOut = timeout

    def notConnect(self):
        try:
            urlopen(self.url, timeout=self.timeOut)
            return False
        except:
            return True
    # This is used to parse HTML, save links of a givn url
    def parseAndGetLinks(self):


        try:
            urlop = urlopen(self.url, timeout=self.timeOut)
            data = urlop.read().decode('utf-8', 'ignore')
            soup = BeautifulSoup(data, 'lxml')
            links = []
            for link in soup.find_all('a'):
                # print(link)
                if link.get('href'):
                    print('here get the href', link.get('href'))
                    if link.get('href')[:10] != 'javascript' and link.get('href') != '#':
                        links.append(link.get('href'))
            return links
        except:
            return []

    # this is used to get static content according to the requirement like img and js
    # @url is the link to get static content
    def parseAndGetStatic(self, url):
        try:
            urlop = urlopen(url, timeout=self.timeOut)
            data = urlop.read().decode('utf-8', 'ignore')
            soup = BeautifulSoup(data, 'lxml')
            staticLinks = []
            for link in soup.find_all(['img', 'src', 'link', 'script']):
                if link.get('script'):
                    eachlink = link.get('src')
                if link.get('src'):
                    eachlink = link.get('src')
                if link.get('href'):
                    eachlink = link.get('href')
                if eachlink:
                    if eachlink[:4] != 'http' and \
                                    eachlink.find('://') == -1:
                        eachlink = urljoin(url, eachlink)
                    staticLinks.append(eachlink)
            return staticLinks
        except:
            return []

# Crawker class
class Crawler(object):
    # mange entire crawling process
    count = 0  # static download page counter
    # for a search level limitation, this is a breadth first search on the start url
    deepLevel = 0

    def __init__(self, url, timeout, deeplevel):
        self.q = deque()
        self.q.append(url)
        self.visted = set()
        self.dom = urlparse(url)[1]
        self.timeOut = timeout
        self.deepLevel = deeplevel
        if self.dom[:4] == 'www.':
            self.dom = self.dom[4:]  # a very hard way to get the domin of the url

    # This is to get the satic page from the url link
    # @url is the link to get static content
    def getStatic(self, url):
        r = Retriever(url, self.timeOut)
        if r.notConnect():
            print(url + ' is not accessiable or it is not a validate url')
            return
        staticLinks = r.parseAndGetStatic(url)
        return staticLinks
    # This is used to get page content
    # @url is the link to get static content
    def getPage(self, url):
        r = Retriever(url, self.timeOut)
        if r.notConnect():
            print(url + ' is not accessiable or it is not a validate url')
            return
        Crawler.count += 1
        self.visted |= {url}

        links = r.parseAndGetLinks()  # get and process children links of a url
        if not links:
            return
        for eachlink in links:
            if eachlink[:4] != 'http' and \
                            eachlink.find('://') == -1:
                eachlink = urljoin(url, eachlink)

            if eachlink.lower().find('mailto:') != -1:
                #  print('....discarded, mailto link')
                continue

            # to transform the non-ascii to ascii
            eachlink = urlsplit(eachlink)
            eachlink = list(eachlink)
            eachlink[2] = quote(eachlink[2])
            eachlink = urlunsplit(eachlink)
            if eachlink not in self.visted:
                if eachlink.find(self.dom) == -1:
                    sleep(1)
                else:
                    if eachlink not in self.q:
                        self.q.append(eachlink)

    def go(self):
        # process links in queue
        result = []
        while self.q:
            # if you put a negtive number and this deep limitation will be not working which is used for search large page
            if abs(self.deepLevel) > 0:
                print('Now search layer ' + str(self.deepLevel))
                print(str(self.q))
                url = self.q.popleft()
                self.getPage(url)
                print('proccess url ' + url)
                static = self.getStatic(url)
                result.append({"url": url, "assets": static})
                self.deepLevel = self.deepLevel - 1
            else:
                # reach the limitation of the search layer
                break
        # Writing JSON data
        with open('data.json', 'w') as f:
            json.dump(result, f)
        return result

# This is utility function to validate the parameter reading from console
# @url is the root url to start the app
# @timeout is should be set according to the network status,the large it is the longer the crawler will wait for the remote to response
# @level is used to constraint how deep the crawler should go to if you want to run against a big page, -1 if you want to download everything
def inputValidat(url, timeout, level):
    try:
        urlopen(url, timeout=1)

    except:
        print('Enter correct url')
        return False
    try:
        int(timeout)
    except:
        print('Enter timeout limit in a numeric format')
        return False
    try:
        int(level)
    except:
        print('Enter search level in a numeric format')
        return False
    return True


def main():
    # by default the parameter should be at least 3
    if len(argv) == 4:
        if inputValidat(argv[1], argv[2], argv[3]):
            url = argv[1]
            timeout = int(argv[2])
            level = int(argv[3])
            print('Start with parameter:URL is ' + str(url) + ' and TimeOut is ' + str(
                timeout) + 'and the search level is ' + str(level))
            robot = Crawler(url, timeout, level)
            robot.go()
        else:
            print('Please provide correct parameters')
    else:
        print('Please provide enough parameters in python3 crawl3.py url timeout searchlevel format')


if __name__ == '__main__':
    main()
