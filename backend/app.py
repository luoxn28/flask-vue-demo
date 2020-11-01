import os

from flask import Flask, render_template, request

from backend.utils import file_utils
from backend.component.excel.base import excelr
from backend.core import excel, excel_dict
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


# excel文件上传 http://docs.jinkan.org/docs/flask/patterns/fileuploads.html
@app.route('/api/hello/post', methods=["POST"])
def post():
    try:
        file = request.files['file']
        if not excelr.excel_name_legal(file.filename):
            return Result.fail('上传文件不合法: ' + file.filename)

        # 保存excel文件并加载到内存数据库
        path = file_utils.save(app.config['UPLOAD_FOLDER'], file)
        excel_dict.load_excel_data(path)
        return Result.success(path)
    except Exception as e:
        return Result.fail(str(e))


@app.route('/api/query/sheet/names', methods=["POST"])
def query_sheet_names():
    try:
        return Result.success(excel_dict.read_sheet_names())
    except Exception as e:
        return Result.fail(str(e))


@app.route('/api/current/sheet/name', methods=["POST"])
def current_sheet_name():
    try:
        return Result.success(excel_dict.current_sheet_name())
    except Exception as e:
        return Result.fail(str(e))


@app.route('/api/query/sheet/data', methods=["POST"])
def query_sheet_data():
    try:
        path = request.json.get('path')
        if not excelr.excel_name_legal(path):
            return Result.fail('参数错误或者文件类型不合法')
        elif not os.path.exists(path):
            return Result.fail('路径不存在: ' + path)

        sheet = request.json.get('sheet')
        if not excel_dict.sheet_names or sheet not in excel_dict.sheet_names:
            return Result.fail('sheet不存在: ' + sheet)
        lambda_code = request.json.get('lambda')

        return Result.success(excel.query_excel_data(path, sheet, lambda_code))
    except Exception as e:
        return Result.fail(str(e))


# 获取excel文件内容
@app.route('/api/hello/sheet/data', methods=["POST"])
def hello_sheet_data():
    try:
        path = request.json.get('path')
        if not excelr.excel_name_legal(path):
            return Result.fail('参数错误或者文件类型不合法')
        elif not os.path.exists(path):
            return Result.fail('路径不存在: ' + path)

        sheet = request.json.get('sheet')
        if not excelr.contains_sheet(path, sheet):
            return Result.fail('sheet不存在: ' + sheet)

        return Result.success(excel.read_excel_data(path, sheet))
    except Exception as e:
        return Result.fail(str(e))


if __name__ == '__main__':
    app.run()
