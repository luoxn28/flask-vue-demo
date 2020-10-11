import os


# 存储文件并返回该文件存储路径
def save(basepath: str, file):
    if not os.path.exists(basepath):
        os.mkdir(basepath)
    path = os.path.join(basepath, file.filename)
    file.save(path)
    return path
