import pyaudio

def device_info_show(audio, show_input=True, show_output=True):
    # 列出所有音频设备
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        # 获取设备名称并尝试进行解码
        device_name = device_info['name']
        error_str = "鑰虫満"
        if error_str in device_name:
            device_name = device_name.encode('gbk').decode('utf-8', errors='replace')
            device_name = device_name.replace('\n', '').replace('\r', '')
        print("index:{:02d} :HostApi={} Channels[in:{}, out:{}] {}".format(
            i, device_info['hostApi'], device_info['maxInputChannels'], device_info['maxOutputChannels'], device_name))


if __name__ == '__main__':

    # 初始化 PyAudio
    p = pyaudio.PyAudio()

    device_info_show(p, True, True)

    default_input_device  = p.get_default_input_device_info()["index"]
    default_output_device = p.get_default_output_device_info()["index"]
    print("\n缺省设置:[输入设备:{}, 输出设备:{}]".format(default_input_device, default_output_device))
    # 关闭 PyAudio
    p.terminate()