from src.core_module import core


def resp_main_css(response):
    if response is not None:
        main_css = 'src/static/css/main.css'
        status = '200 OK'
        headers = [('Content-Type', 'text/css')]
        response(status, headers)
        txt = core.render(main_css)
        response = ''.join([txt])
        return [response.encode()]
    else:
        return None

