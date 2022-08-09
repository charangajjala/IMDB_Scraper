from flask import jsonify
class MyException(Exception):
    def __init__(self, msg,code):
        self.msg = msg
        self.code = code

def error_handler(err):
    return jsonify({"msg":err.msg}),err.code 

def request_validation(kwd,type):
    if kwd is None or type is None:
        raise MyException("Both keyword and type are required",400)
    kwd = kwd.strip()
    type = type.strip()
    if kwd == '' or type == '':
        raise MyException('Keyword and type cannot be empty',400)