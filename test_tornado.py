#!/usr/bin/env python

import os
import json
import unittest
import urllib

import tornado.testing
from tornado.testing import AsyncHTTPTestCase

from app import Application
from db_sqlite import init_database


class TestHandlerBase(AsyncHTTPTestCase):

    def setUp(self):
        super(TestHandlerBase, self).setUp()

    def get_app(self):
        return Application()

    def test_insert_record(self):
        post_data = {'room': '3', 'name': 'Name', 'surname': 'Surname'}
        body = urllib.urlencode(post_data)
        response = self.fetch('/rooms', method='POST', body=body)
        data = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(data['message'], 'Room is occupied')
        response = self.fetch('/rooms', method='POST', body=body)
        data = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(data['message'], 'The tenant has already occupied this room')
        post_data = {'room': '4', 'name': 'Name2', 'surname': 'Surname2'}
        body = urllib.urlencode(post_data)
        response = self.fetch('/rooms', method='POST', body=body)
        data = json.loads(response.body)
        self.assertEqual(response.code, 200)
        self.assertEqual(data['message'], 'Room is occupied')

    def test_room(self):
        response = self.fetch('/rooms')
        data = json.loads(response.body)
        self.assertEqual(len(data['message']), 2)

    def test_rooms(self):
        response = self.fetch('/rooms/4')
        data = json.loads(response.body)
        self.assertEqual(len(data['message']), 1)

    def test_rooms2(self):
        response = self.fetch('/rooms/3')
        data = json.loads(response.body)
        self.assertEqual(len(data['message']), 1)

    def test_update(self):
        response = self.fetch('/rooms/3', method='PATCH', body='')
        data = json.loads(response.body)
        self.assertEqual(data['message'], 'The tenant Name Surname left the room')

    def test_delete(self):
        response = self.fetch('/rooms/3', method='DELETE')
        self.assertEqual(response.code, 200)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def all():
    suite = unittest.defaultTestLoader.discover('./', 'test_tornado.py', BASE_DIR)
    print suite
    return suite


if __name__ == '__main__':
    init_database()
    tornado.testing.main()


# class TestBucketHandler(TestHandlerBase):

#     def create_something_test(self):

#         # Example on how to hit a particular handler as POST request.
#         # In this example, we want to test the redirect,
#         # thus follow_redirects is set to False
#         post_args = {'room': '3', 'name': 'Nikita', 'surname': 'Vlasov'}
#         response = self.fetch(
#             '/rooms',
#             method='POST',
#             body=urllib.urlencode(post_args),
#             follow_redirects=False)

#         # On successful, response is expected to redirect to /tutorial
#         self.assertEqual(response.code, 302)
#         self.assertTrue(
#             response.headers['Location'].endswith('/tutorial'),
#             "response.headers['Location'] did not ends with /tutorial"
#         )

# if __name__ == '__main__':
#     unittest.main()


# import time
# import unittest
# from tornado import ioloop


# def async_calculate(callback):
#     """
#     @param callback:    A function taking params (result, error)
#     """
#     # Do something profoundly complex requiring non-blocking I/O, which
#     # will complete in one second
#     ioloop.IOLoop.instance().add_timeout(
#         time.time() + 1,
#         lambda: callback(17, None)
#     )


# class AsyncTest(unittest.TestCase):

#     def test_find(self):
#         def callback(result, error):
#             ioloop.IOLoop.instance().stop()
#             print 'Got result', result
#             self.assertEqual(42, result)

#         async_calculate(callback)
#         ioloop.IOLoop.instance().start()


# if __name__ == '__main__':
#     tornado.testing.main()
