import cherrypy
import json

from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

db = TinyDB(storage=MemoryStorage)

MAX_RECORDS = 10


def add_json_record(data):
    """Adds a new record to the database. Edits records based on the '_id' key
    in the json data

    @return primary key of the new or edited record
    """
    if not isinstance(data, dict):
        return None
    Record = Query()
    rec = db.get(Record._id == data.get('_id'))

    if rec:
        db.update(data, eids=[rec.eid])
        eid = rec.eid
    else:
        pop_top_records()
        eid = db.insert(data)

    return eid


def pop_top_records():
    """Maintain a list if MAX_RECORDS in the database"""

    if len(db) >= MAX_RECORDS:
        to_delete = (len(db) - MAX_RECORDS) + 1
        count = 0
        eids = []
        for r in db:
            if count < to_delete:
                eids.append(r.eid)
            else:
                break
            count += 1
        db.remove(eids=eids)


class DataConsumer(object):

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def index(self):
        if cherrypy.request.method not in ['POST', 'PATCH', 'PUT']:
            data = []
            for r in db:
                data.append(r)

            return data

        data = cherrypy.request.json
        response = {'status': 'OK'}

        if data.get('_id'):
            response['ref'] = add_json_record(data)

        return response


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(DataConsumer(), '')
