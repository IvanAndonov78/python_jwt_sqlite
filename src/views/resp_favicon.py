def resp_favicon(response):
    if response is not None:
        status = '200 OK'
        headers = [('Content-Type', 'image/x-icon')]
        response(status, headers)
        response = ''.join([''])
        return [response.encode()]
    else:
        return None





