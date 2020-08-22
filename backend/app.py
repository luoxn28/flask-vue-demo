from flask import Flask, render_template

app = Flask(__name__,
            template_folder="../frontend/dist",
            static_folder="../frontend/dist/static")


# 主页面
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
