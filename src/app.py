from wsgiref.simple_server import make_server
from src.router import urls_router


class App:

    def __init__(self, routes):
        self.routes = routes

    def __call__(self, environ, response):
        handler = self.routes.get(environ.get('PATH_INFO')) or self.routes.get('/not_found')
        return handler(environ, response)


application = App(urls_router.app_routes)

httpd = make_server('localhost', 8000, application)
httpd.serve_forever()
