from wtforms import Form, StringField


class FunctionForm(Form):
    function_name = StringField()
    parameters_json = StringField()
