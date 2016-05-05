# -*- coding: utf-8 -*-

from urllib import parse
import requests
import time
import datetime
import sys
import argparse


對應版本 = "2.5.0"
登入網址 = "http://iw2.mcdonaldssurprise.com/account/login"
設置鬧鐘網址 = "http://iw2.mcdonaldssurprise.com/account/alarmsetconfig"
領取驚喜網址 = "http://iw2.mcdonaldssurprise.com/prize/collect"
CDN網址 = "http://cdn.mcdonaldssurprise.com/prizes/images/"

class HappyHackingMCDSSurprise(object):

    def __init__(self, 帳號, 密碼, 設備):
        self.帳號 = 帳號
        self.密碼 = 密碼
        self.設備 = 設備
        self.使用者 = None
        self.金鑰 = None
        self.鬧鐘時間 = None

    def 執行(self):
        if self.登入():
            if self.設置鬧鐘() and self.等待鬧鐘():
                if self.領取驚喜():
                    return True

    def 登入(self):
        登入資料 = {
            "cid": "2",
            "email": self.帳號,
            "pw": self.密碼,
            "device": self.設備
        }
        響應 = requests.post(登入網址, data=登入資料)
        JSON響應 = 響應.json()

        if JSON響應['error'] == 0:
            self.使用者 = JSON響應["userId"]
            self.金鑰 = JSON響應["key"]
            sys.stdout.write("登入成功\n")
            return True
        else:
            sys.stderr.write("登入失敗\n")

    def 設置鬧鐘(self):
        if not self.金鑰:
            sys.stderr.write("金鑰不存在\n")
            return

        加一分鐘 = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.鬧鐘時間 = datetime.datetime(加一分鐘.year, 加一分鐘.month, 加一分鐘.day, 加一分鐘.hour, 加一分鐘.minute)
        sys.stdout.write("設置鬧鐘: {}\n".format(self.鬧鐘時間))
        鬧鐘資料 = {
            "key": self.金鑰,
            "alarm_set": str(int(self.鬧鐘時間.timestamp())),
            "alarm_config": "1111111"
        }
        響應 = requests.post(設置鬧鐘網址, data=鬧鐘資料)
        JSON響應 = 響應.json()
        if JSON響應['error'] is 0:
            sys.stdout.write("鬧鐘設置成功\n")
            return True
        else:
            sys.stderr.write("鬧鐘設置失敗\n")

    def 等待鬧鐘(self):
        if not self.鬧鐘時間:
            sys.stderr.write("鬧鐘時間不存在\n")
            return

        while self.鬧鐘時間 > datetime.datetime.now():
            sys.stdout.write("等待鬧鐘時間到時...\n")
            time.sleep(5)
        return True

    def 領取驚喜(self):
        領取驚喜資料 = {
            "uid": self.使用者,
            "key": self.金鑰,
            "device": self.設備,
            "version": 對應版本,
            "alarm_set": str(int(self.鬧鐘時間.timestamp())),
            "repeat": "1"
        }

        響應 = requests.post(領取驚喜網址, data=領取驚喜資料)
        JSON響應 = 響應.json()
        if JSON響應['error'] is 0:
            sys.stdout.write("領取成功，分析結果...{}\n".format(JSON響應))
            return self.分析結果(JSON響應)
        else:
            sys.stderr.write("錯誤訊息: {}\n".format(JSON響應["errorMsg"]))
            if JSON響應["errorMsg"] is "One prize per day":
                sys.stderr.write("一個帳號不夠抽，那你有辦第二個嗎？\n")

    def 分析結果(self, JSON響應):
        if JSON響應['winnerPrize']['prizeType'] is '0':
            sys.stdout.write("該死的畜生！你中了甚麼？\n")
            sys.stdout.write("標題: {}\n".format(JSON響應['winnerPrize']['title']))
            sys.stdout.write("雞湯圖片: {}\n".format(parse.urljoin(CDN網址, JSON響應['winnerPrize']['alarmImage320'])))
            sys.stdout.write("雞湯分享: {}\n".format(JSON響應['winnerPrize']['shareText']))
        elif JSON響應['winnerPrize']['prizeType'] is '1':
            sys.stdout.write("噫！好了！我中了！\n")
            sys.stdout.write("標題: {}\n".format(JSON響應['winnerPrize']['title']))
            sys.stdout.write("優惠圖片: {}\n".format(parse.urljoin(CDN網址, JSON響應['winnerPrize']['offerImage'])))
            sys.stdout.write("產品圖片: {}\n".format(parse.urljoin(CDN網址, JSON響應['winnerPrize']['productImage'])))
            sys.stdout.write("分享訊息: {}\n".format(JSON響應['winnerPrize']['shareText']))
        return True

    def 暫存(self):
        買超值全餐送四塊麥克鷄塊 = "Buy EVM get 4 nuggets"
        請我吃薯餅 = "Hashbrown"
        豬肉滿福堡加蛋單點買一送一 = "ALC Sausage McMuffin with Egg BOGO"
        請我吃小薯 = "Free Small Fries"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="為懶惰的人所準備的早安鬧鐘優惠領取腳本")
    parser.add_argument("-u", "--user", help="你的帳號")
    parser.add_argument("-p", "--password", help="你的密碼")
    parser.add_argument("-d", "--device", help="你的設備ＩＤ", default="499018963093620")
    args = parser.parse_args()

    hhmd = HappyHackingMCDSSurprise(args.user, args.password, args.device)
    if hhmd.執行():
        sys.stdout.write("程序執行完成\n")
        sys.exit(0)
    else:
        sys.stderr.write("中斷\n")
        sys.exit(1)
