#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2024/07/18 01:29:53
@Author  :   Kyle Wang 
@Version :   1.0
@Contact :   wangkui2000@hotmail.com
@License :   (C)Copyright 2017-2030, KyleWang
@Desc    :   myRecorder 类测试使用范例
'''

import time
import logging
from lib.myRecorder import myRecorder

def call_auto():
    try:
        Audio = myRecorder(logF="recorder.log", logOut=3, logL=logging.DEBUG)
        Audio.init(isMic=True)
        Audio.run(3)
        while True:
            file = Audio.get(True)
            if file:
                print("    Get Audio data:", file)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print(" "*4, "Stop by KeyboardInterrupt at call_auto()")
        Audio.stop()
        time.sleep(1)
    finally:
        try:
            del Audio
        except:
            pass
    print("  结束: call_auto()")


if __name__ == '__main__':
    # Usage Example: 自动录音并保存文件, 维护文件名称队列
    call_auto()