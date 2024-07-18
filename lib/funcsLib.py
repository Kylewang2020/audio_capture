#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   funcs.py
@Time    :   2024/06/05 17:01:39
@Author  :   Kyle Wang 
@Version :   1.0
@Contact :   wangkui2000@hotmail.com
@License :   (C)Copyright 2017-2030, KyleWang
@Desc    :   通用函数定义
'''

import logging, time, os
from datetime import datetime

CurrentDir = os.path.dirname(os.path.realpath(__file__))
ParentDir  = os.path.dirname(CurrentDir)
LogPath    = CurrentDir


def log_init(logF="log.log", logOut=3, logL=logging.DEBUG, path=None):
    '''
    日志初始化. 
        logOut: 1=file only; 2=console only; 3=both 
        logL  : logging level. logging.DEBUG, logging.INFO...
    '''
    logger = None
    try:
        logger = logging.getLogger(__name__)
        logger.setLevel(level=logL)
        # formatter= logging.Formatter(datefmt='%H:%M:%S',
        #     Fmt='[%(levelname)-5s|%(asctime)s.%(msecs)03d|%(thread)s|%(lineno)d@%(funcName)s()] %(message)s' )
        formatter= logging.Formatter(datefmt='%H:%M:%S',
            fmt='[%(levelname)-5s|%(asctime)s.%(msecs)03d|%(thread)s|%(lineno)d@%(funcName)s()] %(message)s' )
        if logOut==2 or logOut==3:
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            logger.addHandler(console)
        if logOut==1 or logOut==3:
            if path is None:
                path = os.getcwd()
                path = os.path.join(path, "log")
            if not os.path.exists(path): os.mkdir(path)
            logF = os.path.join(path, logF)
            handler = logging.FileHandler(logF, encoding='utf-8')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.debug("log[level:{}, output:{}, file: \"{}\"]".format(logL, logOut, logF))
    except Exception as e:
        print("logger init failed:", e)
    
    if logger is None:
        raise Exception("logger init failed.")
    else:
        return logger


def timer(indent=2, isTimer=True):
    '''
    Decorator to count the time consuming. 
    Could stop by set the var isTimer=False.
    '''
    def decorator(func):
        def wrapper(*args, **kwargs):
            if isTimer: start_time = time.time()
            result = func(*args, **kwargs)
            if isTimer: 
                end_time = time.time()
                print(' '*indent, "{}()耗时:{:.6f}s".format(func.__name__, end_time-start_time))
            return result
        return wrapper
    return decorator

# dict key 字段最大长度
def dict_key_max_len(curArg):
    max_len = 10
    if not isinstance(curArg, dict):
        return max_len
    for key in curArg.keys():
        if len(key)>max_len: max_len = len(key)
    return max_len


def str_code_correct(value):
    error_str = "鑰虫満"
    if type(value) is str and error_str in value:
        value = value.encode('gbk').decode('utf-8', errors='replace')
        value = value.replace('\n', '').replace('\r', '')
    return value


# dict 遍历 print
def print_dict(curArg, isPrintShort=True, indent=4):
    if isinstance(curArg, dict):
        key_len = dict_key_max_len(curArg)
        for key, value in curArg.items():
            if (isinstance(value, list) and isinstance(value[0], dict)) or  isinstance(value, dict):
                print(' '*indent, "{} : [类型:{}, 元素个数:{}]".format(key, type(value), len(value)))
                print_dict(value, indent+4)
            else:
                if type(key) is str and 'default' in key and isPrintShort: return
                value = str_code_correct(value)
                print(' '*indent, "{:<{}}: {}".format(key, key_len+1, value))
    elif isinstance(curArg, list) and isinstance(curArg[0], dict):
        for i in range(len(curArg)):
            print_dict(curArg[i], indent)
    else:
        print(' '*indent, curArg)


def get_date_time_string():
    # 获取当前日期时间
    now = datetime.now()
    date_time_string = now.strftime("%m_%d_%H_%M_%S")
    return date_time_string


# 枚举所有 指定 host_api的音频设备
def list_audio_devices(audio, host_api_index=0):
    info = audio.get_host_api_info_by_index(host_api_index)
    num_devices = info.get('deviceCount')
    
    for i in range(num_devices):
        device_info = audio.get_device_info_by_host_api_device_index(0, i)
        print(f"Device {i}: {device_info['name']}")
        print_dict(device_info)


# 查找名称中包含“立体声混音”或“Stereo Mix”的设备编号
def find_stereo_mix_device(audio, host_api_index=0):
    info = audio.get_host_api_info_by_index(host_api_index)
    num_devices = info.get('deviceCount')
    
    for i in range(num_devices):
        device_info = audio.get_device_info_by_host_api_device_index(host_api_index, i)
        if 'Stereo Mix' in device_info.get('name', '') or '立体声混音' in device_info.get('name', ''):
            return i
    return None


def GetFileName(id=None, folder=None, isMic=None, Channels=2, Rate=44100, Fmt="paInt16", suffix=".wav"):
    '''
    获取录音文件名称。缺省为当前运行目录下的data子目录中
    如: D08_01-54-32_Speaker_channels1_rate16000_paFloat32_No-1.wav
    '''
    # 创建目录
    if folder is None:
        path = os.getcwd()
        path = os.path.join(path, "data")
    if not os.path.exists(path): os.mkdir(path)

    fileName = datetime.now().strftime("D%d_%H-%M-%S") + "_" 
    if isMic is not None:
        if isMic: fileName += "Mic_"
        else:     fileName += "Speaker_"
    fileName += "channels"+ str(Channels)+ "_rate" + str(Rate) + "_" + Fmt
    if id is not None:
        fileName += "_No-" + str(id)
    fileName += suffix
    fileName = os.path.join(path, fileName)
    return fileName


# 查找名称中包含“立体声混音”或“Stereo Mix”的设备编号
def get_mix_device(audio, host_api_index=0):
    info = audio.get_host_api_info_by_index(host_api_index)
    num_devices = info.get('deviceCount')
    for i in range(num_devices):
        device_info = audio.get_device_info_by_host_api_device_index(host_api_index, i)
        if 'Stereo Mix' in device_info.get('name', '') or '立体声混音' in device_info.get('name', ''):
            return i
    return None

if __name__ == '__main__':
    fileName = GetFileName(isMic=True, id=1)
    print(fileName)
    list_audio_devices()