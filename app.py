#!/usr/bin/env python

from datetime import datetime

import tornado.httpserver
import tornado.ioloop
import tornado.web

from db_sqlite import init_database, _execute as db_exec
from utils import rn


class HotelHandler(tornado.web.RequestHandler):

    QUERY_WHERE_DEPARTURE_NULL = '''
        SELECT name, surname
        FROM tenants
        WHERE room_number=? AND departure IS NULL
    '''

    def get(self, room_number=None):
        SQL = '''
            SELECT name, surname, arrival, departure, room_number
            FROM tenants
        '''
        if rn(room_number):
            rows = db_exec('{} WHERE room_number=?'.format(SQL), room_number)
        else:
            rows = db_exec(SQL)
        data = []
        for row in rows:
            data.append({
                'name': row[0],
                'surname': row[1],
                'arrival': row[2],
                'departure': row[3],
                'number of room': row[4],
            })
        response = {
            'success': True,
            'message': data or 'All places are free',
        }
        self.write(response)

    def post(self):
        name = self.get_argument('name', None)
        surname = self.get_argument('surname', None)
        room_number = self.get_argument('room', None)

        if not (name and surname and rn(room_number)):
            response = {
                'success': False,
                'message': 'Fail: {}'.format(', '.join(
                    [entry for entry, value in (
                        ('name', name), ('surname', surname), ('room', room_number)) if not value] or [room_number]
                ))
            }
        else:
            rows = db_exec(self.QUERY_WHERE_DEPARTURE_NULL, room_number)

            if rows:
                response = {
                    'success': False,
                    'message': 'The tenant has already occupied this room'
                }
            else:
                db_exec('''
                    INSERT INTO tenants (name, surname, room_number)
                    VALUES (?, ?, ?)''', (name, surname, room_number))
                response = {
                    'success': True,
                    'message': 'Room is occupied'
                }
        self.write(response)

    def patch(self, room_number):
        rows = db_exec(self.QUERY_WHERE_DEPARTURE_NULL, room_number)
        if rows:
            row = rows[0]
            name = row[0]
            surname = row[1]
            db_exec('''
                UPDATE tenants
                SET departure=?
                WHERE room_number=? AND departure IS NULL
                ''', (datetime.now(), room_number))
            response = {
                'success': True,
                'message': 'The tenant %s %s left the room' % (name, surname)
            }
        else:
            response = {
                'success': False,
                'message': 'The room is not inhabited'
            }
        self.write(response)

    def delete(self, room_number):
        db_exec('''
            DELETE FROM tenants
            WHERE room_number=? AND departure IS NOT NULL''', (room_number,))
        response = {
            'success': True,
            'message': 'Information about tenants of this room is deleted'
        }
        self.write(response)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/rooms$', HotelHandler),
            (r'/rooms/$', HotelHandler),
            (r'/rooms/(\d+$)', HotelHandler),
        ]
        tornado.web.Application.__init__(self, handlers)


def main():
    app = tornado.httpserver.HTTPServer(Application())
    app.listen(8000)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()


if __name__ == '__main__':
    init_database()
    main()
