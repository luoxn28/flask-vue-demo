from flask import Flask, render_template, request

app = Flask(__name__,
            template_folder="../frontend/dist",
            static_folder="../frontend/dist/static")


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


if __name__ == '__main__':
    app.run()
