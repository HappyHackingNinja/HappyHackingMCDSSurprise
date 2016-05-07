import sys
from hhmcds.model import 早安鬧鐘資料
from hhmcds.surprise import HappyHackingMCDSSurprise
from hhmcds.smurf import MCDSSurpriseSmurf


def 抽獎():
    for idx in range(1, 100):
        data = 早安鬧鐘資料("test+{:02d}@gmail.com".format(idx), "password", "531360765412016")
        hhmd = HappyHackingMCDSSurprise(data)
        if hhmd.執行():
            sys.stdout.write("程序執行完成\n\n")
        else:
            sys.stderr.write("中斷\n")


def 創小號():
    for idx in range(1, 100):
        data = 早安鬧鐘資料("test+{:02d}@gmail.com".format(idx), "password", "531360765412016")
        mss = MCDSSurpriseSmurf(data)

        if mss.執行():
            sys.stdout.write("程序執行完成\n\n")
        else:
            sys.stderr.write("中斷\n")


if __name__ == "__main__":
    抽獎()