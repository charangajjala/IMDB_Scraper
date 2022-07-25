from flask import jsonify
class MyException(Exception):
    def __init__(self, msg,code):
        self.msg = msg
        self.code = code

def error_handler(err):
    return jsonify({"msg":err.msg}),err.code 