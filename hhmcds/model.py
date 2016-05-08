import datetime


class 早安鬧鐘資料(object):

    def __init__(self, 信箱, 密碼, 設備):
        self.信箱 = 信箱
        self.密碼 = 密碼
        self.設備 = 設備
        self.識別碼 = None
        self.金鑰 = None
        self.鬧鐘時間 = None
        self.註冊成功 = False
        self.抽獎成功 = False
        self.抽獎結果 = None
        self.對應版本 = "2.5.0"

    def 更新鬧鐘時間(self):
        # 加一分鐘 = datetime.datetime.now() + datetime.timedelta(minutes=1)
        加一分鐘 = datetime.datetime.now()
        self.鬧鐘時間 = datetime.datetime(加一分鐘.year, 加一分鐘.month, 加一分鐘.day, 加一分鐘.hour, 加一分鐘.minute)
