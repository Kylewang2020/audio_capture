# audio_capture

A simple recorder from both mic and speaker, save the result as wave file or numpy data. For use with speech recognition.

## 主要功能

- 选择录音设备[麦克风 or 扬声器] 并 初始化
  - 可以设置录音设备的时长
  - [x] 保存音频文件到 ./data/目录
  - [x] 降噪: 暂时放弃! 效果不明显，目前不考虑。
  - [ ] 自动识别声音语句的中断，并自动截取
    - 在给定的时间段内识别语音的数据波幅
      - 如果没有声音检测到，则给出空文件
      - 如果检测到声音，则去除静音时间段，给出纯声音的文件

- [x] 保存录音结果文件名称到 audio_queue
- [x] 日志
- [ ] Event
