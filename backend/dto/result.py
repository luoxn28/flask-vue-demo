import logging

logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO)


# restful返回结果
class Result:
    def __init__(self, code=0, data={}, msg=''):
        self.code = code
        self.data = data
        self.msg = msg

    def to_json(self):
        return {
            'code': self.code,
            'data': self.data,
            'msg': self.msg
        }

    @staticmethod
    def success(data={}):
        return Result(data=data).to_json()

    @staticmethod
    def fail(msg: str, code=-1):
        logging.warning('发生异常 ' + msg)
        return Result(code, data={}, msg=msg).to_json()
