# -*- coding: utf-8 -*-

import requests
import sys
import argparse
from hhmcds.model import 早安鬧鐘資料

註冊網址 = "http://iw2.mcdonaldssurprise.com/account/register"


class 分身(object):

    def __init__(self, 資料):
        if not isinstance(資料, 早安鬧鐘資料):
            raise TypeError("輸入資料類型錯誤")
        self.資料 = 資料

    def 執行(self):
        return self.註冊()

    def 註冊(self):
        註冊資料 = {
            "cid": "2",
            "email": self.資料.信箱,
            "pw": self.資料.密碼,
            "device": self.資料.設備,
            "s": "-1",
            "dob": "0",
            "gender": "-1"
        }
        sys.stdout.write("註冊信箱: {}\n".format(self.資料.信箱))
        響應 = requests.post(註冊網址, data=註冊資料)
        JSON響應 = 響應.json()

        if JSON響應['error'] == 0:
            sys.stdout.write("註冊成功\n")
            return True
        elif JSON響應['error'] == 1:
            sys.stderr.write("此帳號已被註冊\n")
        else:
            sys.stdout.write("非預期狀況: {}\n".format(JSON響應))
            sys.stderr.write("註冊失敗\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="為懶惰的人所準備的早安鬧鐘優惠領取腳本")
    parser.add_argument("-u", "--user", help="你的帳號")
    parser.add_argument("-p", "--password", help="你的密碼")
    parser.add_argument("-d", "--device", help="你的設備ＩＤ", default="490154203237518")
    args = parser.parse_args()

    data = 早安鬧鐘資料(args.user, args.password, args.device)

    mss = 分身(data)
    if mss.執行():
        sys.stdout.write("程序執行完成\n")
        sys.exit(0)
    else:
        sys.stderr.write("中斷\n")
        sys.exit(1)