import json
from datetime import datetime
from src.core_module import core


def get_json_file(path_to_file):
    with open(path_to_file) as data_file:
        dict_data = json.load(data_file)
    return dict_data


def write_in_json_file(path_to_file, dict_data):
    json_obj = json.dumps(dict_data, indent=4)  # Serializing json
    # Writing to sample.json
    with open(path_to_file, 'w') as outfile:
        outfile.write(json_obj)
    return True


def resp_save_log(environ, response):
    if response is not None:
        qs = environ['QUERY_STRING']
        # core.dd(qs) # current_date=2022-08-01&count=1
        data_ls = qs.split("&")
        # core.dd(data_ls) # ['current_date=2022-08-01', 'count=1']
        current_date = data_ls[0].split("=")[1]
        count = data_ls[1].split("=")[1]

        # now = datetime.today().strftime('%Y-%m-%d') # yep => '2022-07-31'

        # Read and Write data in a json file: -----------
        data = get_json_file('src/logs/logs.json')
        i = 0
        save_msg = 'Not saved'
        for el in data:
            data["logs"][i]["last_date"] = current_date
            data["logs"][i]["count_logs"] = data["logs"][i]["count_logs"] + int(count)
            if write_in_json_file('src/logs/logs.json', data):
                save_msg = 'Saved successfully!'
                break
            i += 1

        # -----------------------------------------------

        if qs is not None:
            headers = [('Content-Type', 'application/json')]
            status = '200 OK'
            response(status, headers)

            dict_el = {
                'last_datetime': current_date,
                'save_msg': save_msg
            }
            response = json.dumps(dict_el)  # converts dict(or list of dicts) to string
            return [response.encode()]
    return None

