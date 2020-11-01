class TooLongException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        print("姓名长度是" + str(self.msg) + "，超过长度了")
