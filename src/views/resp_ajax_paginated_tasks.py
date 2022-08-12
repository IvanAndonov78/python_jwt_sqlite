import json
from src.services.pagination_service import PaginationService
from src.core_module import core


def resp_ajax_paginated_tasks(environ, response):
    if response is not None:
        qs = environ['QUERY_STRING']
        # core.dd(qs)  # items_per_page=5&page_num=1
        params = qs.split("&")
        # core.dd(params)  # ['items_per_page=5', 'page_num=1']
        items_per_page = int(params[0].split("=")[1])
        page_num = int(params[1].split("=")[1])
        if items_per_page is not None and page_num is not None:
            headers = [('Content-Type', 'application/json')]
            status = '200 OK'
            response(status, headers)

            paginator = PaginationService(items_per_page)
            paginated_tasks = paginator.paginate(page_num)
            pages = paginator.get_pages()  # total pages
            ls = []
            for row in paginated_tasks:
                dict_el = {
                    'taskid': row[0],
                    'taskname': row[1],
                    'enddate': row[2],
                    'isregular': row[3],
                    'isclosed': row[4],
                    'total_pages': pages,
                    'page_num': page_num,
                    'items_per_page': items_per_page
                }
                ls.append(dict_el)

            response = json.dumps(ls)  # converts dict(or list of dicts) to string
            return [response.encode()]
    return None

