import json
import urllib

from forms import FunctionForm
from flask import Flask, render_template, jsonify, request
from utils.system_tools import get_functions_dict
import utils.tools_functions

app = Flask(__name__)
functions_dict = get_functions_dict()


@app.route('/', methods=['GET', 'POST'])
def index():
    form = FunctionForm()
    return render_template('index.html', functions_dict=functions_dict, form=form)


@app.route('/function', methods=['GET', 'POST'])
def function():
    """
    请求示例: /function?function_name=string_replace&target_str=http&old_str=t&new_str=o
    (, , ):
    :return: 函数执行结果
    """
    # TODO URL, UTF-8 Decode
    # request_args_dict = {k: urllib.parse.unquote(v[0]).decode('utf8') for k, v in
    #                      request.args.to_dict(flat=False).items()}
    request_args_dict = {k: v[0] for k, v in
                         request.form.to_dict(flat=False).items()}
    function_name = request_args_dict.get('function_name')
    if function_name and functions_dict.get(function_name, None):
        request_args_dict.pop('function_name')
        function_result = getattr(utils.tools_functions, function_name)(**request_args_dict)
        return function_result
    else:
        return ''


if __name__ == '__main__':
    app.run()
