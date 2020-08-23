import os
import shutil
import stat

from PyInstaller.__main__ import run

if __name__ == '__main__':
    # https://blog.csdn.net/u013314786/article/details/103660978
    opts = [
        'backend/app.py',  # 主程序文件
        '-F',  # 打包单文件
        '--distpath=dist/bin'
    ]

    # 打包
    run(opts)

    # 复制静态资源
    base = 'dist/frontend'
    if os.path.exists(base):
        shutil.rmtree(base)
    shutil.copytree('frontend/dist', base)

    # 启动脚本
    start = 'dist/start.sh'
    with open(start, 'w') as file:
        file.write('./bin/app')
    os.chmod(start, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
