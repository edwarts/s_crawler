#!/usr/bin/env python
# coding=utf-8
# author:bo ma

from flask import Flask

app = Flask(__name__)


# This is a mock server used for unitest only, you can find the tree of the webpage structure is
# testpage->p1,p2,p3, two layer only


@app.route('/testpage/')
def testpage(name=None):
    mockData = ""
    with open('testpages/testpage.html') as htmlpage:
        mockData = htmlpage.readlines()
    return str(mockData)


@app.route('/p1/')
def p1(name=None):
    mockData = ""
    with open('testpages/page1.html') as htmlpage:
        mockData = htmlpage.readlines()
    return str(mockData)


@app.route('/p2/')
def p2(name=None):
    mockData = ""
    with open('testpages/page2.html') as htmlpage:
        mockData = htmlpage.readlines()
    return str(mockData)


@app.route('/p3/')
def p3(name=None):
    mockData = ""
    with open('testpages/page3.html') as htmlpage:
        mockData = htmlpage.readlines()
    return str(mockData)


def main():
    app.run(debug=True, host='127.0.0.1')


if __name__ == '__main__':
    main()
