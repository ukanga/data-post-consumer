# -*- coding: utf-8 -*-
"""
This is a simple CherryPy microservice that recieves JSON data,
stores it in memory and will list all items in memory on GET requests.
"""
import cherrypy

from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

db = TinyDB(storage=MemoryStorage)

MAX_RECORDS = 10


def add_json_record(data):
    """Adds or edits record in the database.

    Edits records based on the '_id' key
    in the json data

    @return primary key of the new or edited record
    """
    if not isinstance(data, dict):
        return None

    eid = None
    Record = Query()  # pylint: disable=invalid-name

    _id = data.get('_id')
    if _id:
        rec = db.get(Record._id == _id)  # pylint: disable=W0212

        if rec:
            db.update(data, eids=[rec.eid])
            eid = rec.eid

    if not eid:
        pop_top_records()
        eid = db.insert(data)

    return eid


def pop_top_records():
    """Maintain a list if MAX_RECORDS in the database"""

    if len(db) >= MAX_RECORDS:
        to_delete = (len(db) - MAX_RECORDS) + 1
        count = 0
        eids = []
        for row in db:
            if count < to_delete:
                eids.append(row.eid)
            else:
                break
            count += 1
        db.remove(eids=eids)


class DataConsumer:  # pylint: disable=too-few-public-methods
    """The DataConsumer class

    Implements API endpoints for consuming and listing the in-memeory data.
    """
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def index(self):  # pylint: disable=no-self-use
        """Index endpoint."""
        if cherrypy.request.method not in ['POST', 'PATCH', 'PUT']:
            return reversed(list(db))

        data = cherrypy.request.json
        response = {'status': 'OK'}

        if data.get('_id'):
            response['ref'] = add_json_record(data)

        return response


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(DataConsumer(), '')
