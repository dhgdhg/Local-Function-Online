# -*-coding:utf-8 -*-

# 9/3/2019 7:32 PM, system_tools.py created by TWFB with PyCharm.

"""Description:
系统工具
"""
import json
import os
import re
from settings import BASE_DIR


def get_functions_dict():
    if BASE_DIR:
        function_dict = {}
        with open(os.path.join(BASE_DIR, 'utils', 'tools_functions.py'), 'r') as f:
            file_content = f.read()
            function_list = re.findall(
                r'def ([^#]*?)(\([^#]*?\)):\n\s*?"""\n\s*?description:([^#]*?)\n\s*?([^#]*?)"""',
                file_content,
                re.S
            )
            for i, v in enumerate(function_list):
                function_dict[function_list[i][0]] = {'description': function_list[i][2],
                                                      'parameters': {'required': {}, 'optional': {}}}
                optional_parameters_dict = {}
                tmp_optional_parameters = [h.split('=') for h in v[1].split(',') if '=' in h]
                tmp_optional_parameters_len = len(tmp_optional_parameters)
                for pi, [p, pv] in enumerate(tmp_optional_parameters):
                    pv = pv.strip()
                    if pi == tmp_optional_parameters_len - 1:
                        pv = pv.strip()[:-1]
                    if (pv[0] == '"' and pv[-1] == '"') or (pv[0] == "'" and pv[-1] == "'"):
                        pv = pv[1:-1]
                    if pv and pv[0] == '[' and pv[-1] == ']':
                        pv = pv[1:-1].split(' ')
                        pv.insert(0, 'list')
                    optional_parameters_dict[p.strip()] = pv

                for j in v[-1].strip().split('\n'):
                    tmp_list = j.replace('param', '').replace(' ', '').strip().split(':')[1:]
                    if tmp_list[0] == 'return':
                        function_dict[function_list[i][0]]['return'] = tmp_list[1]
                    else:
                        if tmp_list[0] in optional_parameters_dict.keys():
                            function_dict[function_list[i][0]][
                                'parameters'
                            ][
                                'optional'
                            ][
                                tmp_list[0]
                            ] = [tmp_list[1], optional_parameters_dict[tmp_list[0]]]
                        #     tmp_list[1] 是return介绍
                        else:
                            function_dict[function_list[i][0]]['parameters']['required'][tmp_list[0]] = tmp_list[1]
            return function_dict


def convert_str_to_dict(json_str):
    """
    json_str example:
    {"a":1}
    :param json_str:
    :return:
    """
    return json.loads(json_str)


def convert_data_str_to_dict(data_str):
    """
    data_str example:

        q: sdfsdf
        oq: sdfsdf
        aqs: chrome..69i57j0j69i60l4.811j0j4
        sourceid: chrome
        ie: UTF-8

    :param data_str:
    :return:
    """
    return {i[0].strip(): i[1].strip() for i in re.findall('(.+):(.*)\n', data_str)}


def response_to_json(response):
    response_dict = {}
    omit_args = ['iter_lines',
                 'close',
                 'content',
                 '_content',
                 'raw',
                 'json',
                 'connection',
                 'iter_content',
                 'raise_for_status',
                 'request'
                 ]
    for i in response.__dir__():
        if i not in omit_args and i[:2] != '__':
            if i == 'cookies':
                response_dict[i] = {}
                for k, v in response.cookies.items():
                    response_dict[i][k] = str(v)
            elif i == 'elapsed':
                response_dict[i] = str(response.__getattribute__(i)).split(',')[-1]
            elif i == 'headers':
                response_dict[i] = {}
                for k, v in response.headers.items():
                    response_dict[i][k] = json.dumps(v)
            else:
                response_dict[i] = response.__getattribute__(i)
    return json.dumps(response_dict)


def convert_single_data_to_json(single_data):
    return '{{"return":"{}"}}'.format(single_data)
