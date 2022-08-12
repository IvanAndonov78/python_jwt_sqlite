def resp_test2(response):
    if response is not None:
        status = '200 OK'
        headers = [('Content-Type', 'text/plain')]
        response(status, headers)
        out = 'byte_code_test'
        response = ''.join([out])
        return [response.encode()]
    else:
        return None

