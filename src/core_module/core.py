import json


def render(tpl_path):
    with open(tpl_path, 'r') as file:
        html_tpl = file.read().rstrip()
    return html_tpl


def redirect(headers, response, url):
    status = '302 Found'
    location_header = ("Location", url)
    headers.append(location_header)
    response(status, headers)
    return [b'1']


def escape(input_str):
    # Step 1:  Escape the URL encoded chars:
    escaped_str_from_url_encoding = (
        input_str
        .replace("+", " ")
        .replace('%3F', '?')
        # .replace("%0D%", "\n")
        .replace('%3B', ';')
        .replace('%2C', ',')
        .replace('%28', '(')
        .replace('%29', ')')
        .replace('%5B', '[')
        .replace('%25', '%')
        .replace('%21', '!')
        .replace('%5D', ']')
        .replace('%2B', '+')
        .replace('%7C', '|')
        .replace('%7E', '~')
        .replace('%3C', '<')
        .replace('%3E', '>')
        .replace('%2F', '/')
        .replace('%23', '#')
        .replace('%40', '@')
        .replace("h%27", "'")
        .replace('%22', '"')
        .replace('%5E', '^')
        .replace('%26', '&')
    )

    # Step 2: Escape the HTML special chars:
    escaped_str_from_html_spec_chars = (
        escaped_str_from_url_encoding
        .replace('&', '&amp;')
        .replace('<', '&lt')
        .replace('>', '&gt;')
        .replace('', '')
    )

    # Step 3: Escape SQL Injection:
    escaped_str_from_sql_injection = escaped_str_from_html_spec_chars.replace('--', '')

    # Step 4: Trim the processed string:
    escaped_and_trimmed_str = escaped_str_from_sql_injection.rstrip()
    return escaped_and_trimmed_str


def parse_req_body(environ):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0

    bytes_request_body = environ['wsgi.input'].read(request_body_size)

    req_body = bytes_request_body.decode('utf8').replace("'", '"')  # str
    str_list = req_body.split("&")  # str_list => ['key1=val1', 'key2=val2', ..]
    dict_list = []  # dict
    for i in range(0, len(str_list), 1):
        key = str_list[i].split("=")[0]
        val = str_list[i].split("=")[1]
        el = {key: val}
        dict_list.append(el)
    return dict_list  # [{'questionName': 'How+to+become+a+better+developer+%3F'}, {'currentDate': '2022-07-31'}]


def is_set(key, dict_ls):
    #  dict_ls = [{'questionName': 'How are you?'}, {'currentDate': '2022-07-31'}, {'complexity': '1'}]
    res = False
    for el in dict_ls:
        if el.get(key):
            res = True
            break
    return res


def get_val(key, dict_ls):
    res = None
    for el in dict_ls:
        if el.get(key):
            res = el.get(key)
            break
    return res


def get_posted_input(key, dict_ls):

    def is_set(key, dict_ls):
        #  dict_ls = [{'questionName': 'How are you?'}, {'currentDate': '2022-07-31'}, {'complexity': '1'}]
        res = False
        for el in dict_ls:
            if el.get(key):
                res = True
                break
        return res

    def get_val(key, dict_ls):
        res = None
        for el in dict_ls:
            if el.get(key):
                res = el.get(key)
                break
        return res

    return get_val(key, dict_ls) if is_set(key, dict_ls) else None


def get_processed_textarea(textarea_str):
    return textarea_str.split("%0D%0A")  # list


def set_cookie(headers, expiration, key, val):
    # cookie_header = ('Set-Cookie', 'token=yohoho') # YEP
    # cookie_header = ('Set-Cookie', f"{key}={val}; Expires=Mon, 20-Jul-2022 14:42:35 GMT") #yep
    cookie_header = ('Set-Cookie', f"{key}={val}; Expires={expiration}; HttpOnly")
    headers.append(cookie_header)


def get_cookie(environ):
    if has_cookie(environ):
        return environ['HTTP_COOKIE']  # tokenid=mytokenvalue
    return None


def get_cookies(environ):
    if has_cookie(environ):
        cookies = environ['HTTP_COOKIE']
        return cookies.split(';')


def clear_cookie(environ, headers):
    cookie_from_browser = get_cookie(environ)
    cookie_key = cookie_from_browser.split('=')[0]
    cookie_val = cookie_from_browser.split('=')[1]
    cookie_header = ('Set-Cookie', f"{cookie_key}={cookie_val}; Expires=Thu, 01-Jan-1970 00:00:00 GMT; HttpOnly")
    headers.append(cookie_header)


def get_json_file(path_to_file):
    with open(path_to_file) as data_file:
        dict_data = json.load(data_file)
    return dict_data


def write_in_json_file(path_to_file, dict_data):
    json_obj = json.dumps(dict_data, indent=4)  # Serializing json
    # Writing to sample.json
    with open(path_to_file, 'w') as outfile:
        outfile.write(json_obj)
    return 1


def dd(var):
    print('--------------------------')
    print(str(var))
    print('--------------------------')


def is_string(var):
    print(type(var) is str)


def print_type(var):
    print('--------------------------')
    print(str(type(var)))
    print('--------------------------')


def has_cookie(environ):
    if "HTTP_COOKIE" in environ:
        return True
    else:
        return False


def get_json_file(path_to_file):
    with open(path_to_file) as data_file:
        dict_data = json.load(data_file)
    return dict_data

