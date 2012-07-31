import cherrypy


class FHConsume(object):

    @cherrypy.expose
    def index(self):
        return "Consume Formhub data"


cherrypy.config.update({'server.socket_host': '0.0.0.0'})

cherrypy.quickstart(FHConsume(), '')
