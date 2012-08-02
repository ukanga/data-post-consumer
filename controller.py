import cherrypy
import json


class FHConsume(object):

    @cherrypy.expose
    def index(self):
        if cherrypy.request.method not in ['POST']:
            return u"Only POST requests are allowed."

        content_type = cherrypy.request.headers['Content-type']
        # get posted data
        data = cherrypy.request.body.read()

        # deal with json data
        if content_type == 'application/json':
            response = json.dumps({'status': 'OK'})
            data = json.loads(data)
        # deal with xml data
        elif content_type == 'application/xml':
            response = '<?xmlversion="1.0"?><data><status>OK</status></data>'
        else:
            response = "OK"

        # TODO: do something or persist received data
        cherrypy.response.headers['Content-type'] = content_type
        return response


cherrypy.config.update({'server.socket_host': '0.0.0.0'})

cherrypy.quickstart(FHConsume(), '')
