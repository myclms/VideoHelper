<div align="center">
  <img src="./docs/images/logo.jpeg"alt="VideoCaptioner Logo" width="100">
  <h1>VideoHelper</h1>
  <p>基于爬虫、语音识别、机器翻译、大语言模型的视频播放助手</p>
</div>

  简体中文 / [English](./docs/Readme_EN.md)

## 📖 项目介绍



## 📸 界面预览



## 🧪 测试



## 🚀 快速开始

1. 进入项目目录VideoHelper

2. 配置环境

   ``` bash
   conda create -n VideoHelper python=3.9
   conda activate VideoHelper
   pip install -r requirements.txt
   ```

3. 运行服务端

   ```bash
   python ./player/server/main.py
   ```

4. 打开网页，输入目标视频的网址

   ```
   路径： ./player/web/index.html
   ```



## ✨ 主要功能



## ⚙️ 基本配置



## 💡 项目架构

![](https://gitee.com/myclms/pictures/raw/master/image-20241205162350628.png)

项目的主要目录结构说明如下：

```
VideoHelper/
├── runtime/                    # 运行环境目录（不用更改）
├── AppData/                    # 应用数据目录
    ├── cache/              # 语音转录的LLM缓存目录，存储临时数据
```

## 📝 说明



## 更新日志

2024.12.7

- 增加video_list功能，可在多个获取过的视频中切换。支持在本地文件夹增加视频（或多个视频）（增加后点击列表右上角加号刷新列表）。后续支持在网页上删除视频，修改视频名称。

![](https://gitee.com/myclms/pictures/raw/master/image-20241207225317666.png)

2024.12.6

- 新增 settings.bin，目前只有配置whisper模型大小（用于语音识别）。
- 删除音频提取功能，发现whisper可以直接处理视频!

2024.12.5

- 上传初始代码，实现了基本功能（抓取视频，提取音频，提取字幕）和基本网页前端。

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=myclms/VideoHelper&type=Date)](https://star-history.com/#myclms/VideoHelper&Date)