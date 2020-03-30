# -*-coding:utf-8 -*-

# 9/3/2019 7:05 PM, tools_function.py created by TWFB with PyCharm.

"""Description:
传入的参数全为str类型, 加了=为选填参数
当参数默认值为method='[get post put delete head options]'这种类型时, 前端显示为select, 默认选第一个
retunr的类型为json类型
"""
import json
import urllib

import requests

from utils.system_tools import convert_single_data_to_json, convert_str_to_dict, convert_data_str_to_dict, \
    response_to_json


def string_replace(target_str, old_str, new_str=''):
    """
    description: 指定字符串替换返回替换结果
    :param target_str:
    :param old_str:
    :param new_str:
    :return:
    """

    return convert_single_data_to_json(target_str.replace(old_str, new_str))


def string_to_hex(target_str):
    """
    description: 字符串转16进制
    :param target_str:
    :return:
    """
    result_str = ''
    for i in target_str:
        result_str += hex(ord(i))
    return convert_single_data_to_json(result_str)


def request_url(url, method='[get post put delete head options]', headers={}, data={}, proxies={}):
    """
    description:url请求
    :param url:
    :param method:
    :param headers:
    :param data:
    :param proxies:
    :return:
    """
    if headers:
        try:
            headers = convert_str_to_dict(headers)
        except json.decoder.JSONDecodeError:
            headers = convert_data_str_to_dict(headers)
    if proxies:
        proxies = convert_str_to_dict(proxies)
    if data:
        try:
            data = convert_str_to_dict(data)
        except json.decoder.JSONDecodeError:
            try:
                data = {i.split('=')[0]: i.split('=')[1] for i in data.split('&')}
            except IndexError:
                data = convert_data_str_to_dict(data)
    if method == 'post':
        response = requests.post(url, headers=headers, proxies=proxies, data=data)
    elif method == 'put':
        response = requests.put(url, headers=headers, proxies=proxies, data=data)
    elif method == 'delete':
        response = requests.delete(url, headers=headers, proxies=proxies)
    elif method == 'head':
        response = requests.head(url, headers=headers, proxies=proxies)
    elif method == 'options':
        response = requests.options(url, headers=headers, proxies=proxies)
    else:
        response = requests.get(url, headers=headers, proxies=proxies)
    return response_to_json(response)


def url_decode_encode(url_str, options='[decode encode]'):
    """
    description: URL解编码
    :param url_str:
    :param options:
    :return:
    """
    if options == 'decode':
        return convert_single_data_to_json(urllib.parse.unquote(url_str))
    elif options == 'encode':
        return convert_single_data_to_json(urllib.parse.quote(url_str))


def string_to_ascii(string):
    """
    description: 字符串转ascii
    :param string:
    :return:
    """
    result_str = ''
    for i in string:
        result_str += str(ord(i)) + ' '
    return convert_single_data_to_json(result_str)


def ascii_to_string(ascii_str):
    """
    description: ascii转字符串
    :param ascii_str:
    :return:
    """
    if ',' in ascii_str:
        result_str = ''.join([chr(int(i.strip())) for i in ascii_str.split(',') if i.strip()])
    else:
        result_str = ''.join([chr(int(i.strip())) for i in ascii_str.split(' ') if i.strip()])
    return convert_single_data_to_json(result_str)
