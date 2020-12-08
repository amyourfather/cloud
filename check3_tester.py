import unittest
import requests
import subprocess
import time
import sys

def fail(msg):
    print('error:', msg)

def main():
    url = "http://localhost:80/api/auth/signup"
    payload = {'username': 'test_user', 'email': 'test_email@berkeley.edu', 'password': 'test_password'}
    response = requests.post(url, json=payload)
    global user_cookies
    user_cookies = response.cookies

    url = "http://localhost:80/api/auth/signup"
    payload = {'username': 'test_user2', 'email': 'test_email2@berkeley.edu', 'password': 'test_password2'}
    response = requests.post(url, json=payload)
    global user2_cookies
    user2_cookies = response.cookies

    print('Running posts create tests...')
    test_create()
    print('Finished posts create tests')

    print('Running feed tests...')
    test_feed()
    print('Finished feed tests')


def test_create():
    url = "http://localhost:81/api/posts/create"
    payload = {'postBody': 'test content'}
    response = requests.post(url, json=payload, cookies=user_cookies)
    if response.status_code != 201:
        fail('expected status code 201 but was {}'.format(response.status_code))

    url = "http://localhost:81/api/posts/create"
    payload = {'postBody': 'test content2'}
    response = requests.post(url, json=payload, cookies=user2_cookies)
    if response.status_code != 201:
        fail('expected status code 201 but was {}'.format(response.status_code))

def test_feed():
    url = "http://localhost:81/api/posts/0"
    response = requests.get(url, cookies=user_cookies)
    if response.status_code != 200:
        fail('expected status code 200 but was {}'.format(response.status_code))
    feed = response.json()
    if len(feed) != 1:
        fail('expected feed length 1 but was {}'.format(len(feed)))
    post = feed[0]
    if 'postID' not in post:
        fail('postID missing from post on feed')
    if 'AuthorID' not in post:
        fail('AuthorID missing from post on feed')
    global postID2
    postID2 = post['postID']
    global userID2
    userID2 = post['AuthorID']

    url = "http://localhost:81/api/posts/0"
    response = requests.get(url, cookies=user2_cookies)
    if response.status_code != 200:
        fail('expected status code 200 but was {}'.format(response.status_code))
    feed = response.json()
    if len(feed) != 1:
        fail('expected feed length 1 but was {}'.format(len(feed)))
    post = feed[0]
    if 'postID' not in post:
        fail('postID missing from post on feed')
    if 'AuthorID' not in post:
        fail('AuthorID missing from post on feed')
    global postID
    postID = post['postID']
    global userID
    userID = post['AuthorID']


if __name__ == '__main__':
    main()
