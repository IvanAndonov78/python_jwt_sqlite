def resp_not_found(response):
    response('404 Not Found', [('Content-Type', 'text/plain')])
    return [b'not found']

