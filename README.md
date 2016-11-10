# A crawl by Python

## Please use Python 3 to run this

## How to install it

You can use `pip` to install the requirements as follows:

``` 
pip install -r requirements.txt
```

## How to use it

You only need to type 

``` 
python3 crawl3.py your-start-url timeout researchlevel
```

in your terminal. And then input the starturl ,timeout and researchlevel. The result is saved in the file named "data.json" in the same folder as well as STDOUT.

The research level can be set -1 if you want to explore the whole internet

You can run the test case by following the instruction:

```
1 python3 mockserver.py to run the mockserver for the test case
2 python3 -m unittest unit_test pagecrawlbehaviour_test
```

## For fun to run on docker

``` 
docker build -t crawl
docker run crawl crawl3.py your-start-url timeout researchlevel
```