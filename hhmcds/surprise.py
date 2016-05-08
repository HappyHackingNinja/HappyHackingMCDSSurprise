# -*- coding: utf-8 -*-

from urllib import parse
import requests
import time
import datetime
import sys
import argparse
from hhmcds.model import 早安鬧鐘資料

登入網址 = "http://iw2.mcdonaldssurprise.com/account/login"
設置鬧鐘網址 = "http://iw2.mcdonaldssurprise.com/account/alarmsetconfig"
領取驚喜網址 = "http://iw2.mcdonaldssurprise.com/prize/collect"
CDN網址 = "http://cdn.mcdonaldssurprise.com/prizes/images/"


class HappyHackingMCDSSurprise(object):

    標題字典 = {
        "Buy EVM get 4 nuggets": "買超值全餐送四塊麥克鷄塊",
        "Hashbrown": "請我吃薯餅",
        "ALC Sausage McMuffin with Egg BOGO": "豬肉滿福堡加蛋單點買一送一",
        "Buy EVM Get a free 風味派": "買超值全餐送風味派",
        "Buy EVM get ICC for free": "買任一套餐送蛋捲冰淇淋",
        "ALC $75 Toast Platter": "好精彩大早餐單點75元",
        "ALC Grilled Chicken Burger BOGO": "板烤鷄腿堡買一送一",
        "Buy $33 drinks (包含冷熱飲), get 嫩蛋火腿Q Toast": "買小杯美式送嫩蛋火腿Q吐司",
        "Matcha Red Bean Sundae $30": "抹茶紅豆花聖代單點30元",
        "Buy SCF EVM get SCF ALC": "買勁辣鷄腿堡餐送勁辣鷄腿堡",
        "Buy $38 drink get FOF for free": "買任一大杯冷飲送麥香魚",
        "Free Small Fries": "請我吃小薯",
        "SCF ALC BOGO": "勁辣鷄腿堡買一送一",
        "Buy $38 Drink Get Free SCF for free": "買任一大杯冷飲送勁辣鷄腿堡",
        "McFlurry 2nd item half price": "冰炫風單點第二杯半價（限同口味）"

    }

    def __init__(self, 資料):
        if not isinstance(資料, 早安鬧鐘資料):
            raise TypeError("輸入資料類型錯誤")
        self.資料 = 資料

    def 執行(self):
        if self.登入():
            if self.設置鬧鐘() and self.等待鬧鐘():
                self.領取驚喜()
        return self.資料

    def 登入(self):
        登入資料 = {
            "cid": "2",
            "email": self.資料.信箱,
            "pw": self.資料.密碼,
            "device": self.資料.設備
        }
        響應 = requests.post(登入網址, data=登入資料)
        JSON響應 = 響應.json()

        if JSON響應['error'] == 0:
            self.資料.識別碼 = JSON響應["userId"]
            self.資料.金鑰 = JSON響應["key"]
            sys.stdout.write("登入成功: {0}\n".format(self.資料.信箱))
            return True
        else:
            sys.stderr.write("登入失敗: {0}\n".format(self.資料.信箱))

    def 設置鬧鐘(self):
        if not self.資料.金鑰:
            sys.stderr.write("金鑰不存在\n")
            return

        self.資料.更新鬧鐘時間()
        sys.stdout.write("更新鬧鐘時間: {}\n".format(self.資料.鬧鐘時間))
        鬧鐘資料 = {
            "key": self.資料.金鑰,
            "alarm_set": str(int(self.資料.鬧鐘時間.timestamp())),
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
        if not self.資料.鬧鐘時間:
            sys.stderr.write("鬧鐘時間不存在\n")
            return

        while self.資料.鬧鐘時間 > datetime.datetime.now():
            sys.stdout.write("等待鬧鐘時間到時...\n")
            time.sleep(5)
        return True

    def 領取驚喜(self):
        領取驚喜資料 = {
            "uid": self.資料.識別碼,
            "key": self.資料.金鑰,
            "device": self.資料.設備,
            "version": self.資料.對應版本,
            "alarm_set": str(int(self.資料.鬧鐘時間.timestamp())),
            "repeat": "1"
        }

        響應 = requests.post(領取驚喜網址, data=領取驚喜資料)
        JSON響應 = 響應.json()
        if JSON響應['error'] is 0:
            self.資料.抽獎成功 = True
            sys.stdout.write("領取成功，分析結果...{}\n".format(JSON響應))
            return self.分析結果(JSON響應)
        else:
            sys.stderr.write("錯誤訊息: {}\n".format(JSON響應["errorMsg"]))
            if JSON響應["errorMsg"] is "One prize per day":
                sys.stderr.write("一個帳號不夠抽，那你有辦第二個嗎？\n")

    def 分析結果(self, JSON響應):
        if JSON響應['winnerPrize']['prizeType'] is '0':
            self.資料.抽獎結果 = "雞湯圖片"
            sys.stdout.write("該死的畜生！你中了甚麼？\n")
            sys.stdout.write("標題: {}\n".format(JSON響應['winnerPrize']['title']))
            sys.stdout.write("雞湯圖片: {}\n".format(parse.urljoin(CDN網址, JSON響應['winnerPrize']['alarmImage320'])))
            # sys.stdout.write("雞湯分享: {}\n".format(JSON響應['winnerPrize']['shareText']))
        elif JSON響應['winnerPrize']['prizeType'] is '1':
            sys.stdout.write("噫！好了！我中了！\n")
            if JSON響應['winnerPrize']['title'] in HappyHackingMCDSSurprise.標題字典:
                self.資料.抽獎結果 = HappyHackingMCDSSurprise.標題字典[JSON響應['winnerPrize']['title']]
            else:
                self.資料.抽獎結果 = JSON響應['winnerPrize']['title']
            sys.stdout.write("標題: {}\n".format(self.資料.抽獎結果))
            sys.stdout.write("優惠圖片: {}\n".format(parse.urljoin(CDN網址, JSON響應['winnerPrize']['offerImage'])))
            sys.stdout.write("產品圖片: {}\n".format(parse.urljoin(CDN網址, JSON響應['winnerPrize']['productImage'])))
            # sys.stdout.write("分享訊息: {}\n".format(JSON響應['winnerPrize']['shareText']))
        return True

    def 標題(self, 標題):
        買超值全餐送四塊麥克鷄塊 = "Buy EVM get 4 nuggets"
        請我吃薯餅 = "Hashbrown"
        豬肉滿福堡加蛋單點買一送一 = "ALC Sausage McMuffin with Egg BOGO"
        買超值全餐送風味派 = "Buy EVM Get a free 風味派"
        買任一套餐送蛋捲冰淇淋 = "Buy EVM get ICC for free"
        好精彩大早餐單點75元 = "ALC $75 Toast Platter"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="為懶惰的人所準備的早安鬧鐘優惠領取腳本")
    parser.add_argument("-u", "--user", help="你的帳號")
    parser.add_argument("-p", "--password", help="你的密碼")
    parser.add_argument("-d", "--device", help="你的設備ＩＤ", default="490154203237518")
    args = parser.parse_args()

    data = 早安鬧鐘資料(args.user, args.password, args.device)
    hhmd = HappyHackingMCDSSurprise(data)
    if hhmd.執行().抽獎結果:
        sys.stdout.write("程序執行完成\n")
        sys.exit(0)
    else:
        sys.stderr.write("中斷\n")
        sys.exit(1)
