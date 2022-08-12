def resp_test1(response):
    if response is not None:
        status = '200 OK'
        headers = [('Content-Type', 'text/html')]
        response(status, headers)
        msg = 'TEST 1'
        message = '<html><body><h1>' + msg + '</h1><body></html>'
        response = ''.join([message])
        return [response.encode()]
    else:
        return None

