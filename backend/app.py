import os
import sys

from flask import Flask, render_template, request
from xlrd import XLRDError

from backend.component.base import excelr
from backend.component import xls_excelr, xlsx_excelr
from backend.core import excel
from backend.dto.result import Result

app = Flask(__name__,
            template_folder="../frontend/dist",
            static_folder="../frontend/dist/static")
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')


# 主页面
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


# 接口测试
@app.route('/hello/world', methods=["POST"])
def hello_world():
    text = request.json.get("word")
    print(text)
    return 'hello_world ' + text


# 文件上传 http://docs.jinkan.org/docs/flask/patterns/fileuploads.html
@app.route('/hello/post', methods=["POST"])
def post():
    file = request.files['file']
    if not file.filename or ('.' not in file.filename) or (file.filename.rsplit('.', 1)[1] not in ('xlsx', 'xls')):
        return {"code": -1, "data": "上传文件不合法" + file.filename}

    base = app.config['UPLOAD_FOLDER']
    if not os.path.exists(base):
        os.mkdir(base)
    path = os.path.join(base, file.filename)
    file.save(path)

    return {"code": 0, "data": path}


# 获取excel文件
@app.route('/hello/sheet/names', methods=["POST"])
def hello_sheet_names():
    try:
        path = request.json.get('path')
        if not excelr.excel_name_legal(path):
            return Result.fail(msg='参数错误或者文件类型不合法')
        elif not os.path.exists(path):
            return Result.fail(msg='{} 路径不存在'.format(path))

        names = excelr.read_sheet_names(path)
        return Result.success(data=names)
    except Exception as e:
        return Result.fail(msg=str(e))


# 获取excel文件内容
@app.route('/hello/sheet/data', methods=["POST"])
def hello_sheet_data():
    try:
        path = request.json.get('path')
        if not excelr.excel_name_legal(path):
            return Result.fail(msg='参数错误或者文件类型不合法')
        elif not os.path.exists(path):
            return Result.fail(msg='{} 路径不存在'.format(path))

        sheet = request.json.get('sheet')
        sheets = excelr.read_sheet_names(path)
        if not sheet or sheet not in sheets:
            return Result.fail(msg='{} sheet不存在'.format(sheet))

        return Result.success(excel.read_excel_data(path, sheet))
    except Exception as e:
        return Result.fail(msg=str(e))


if __name__ == '__main__':
    app.run()
