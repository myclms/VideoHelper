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

1. 克隆本项目，进入项目目录VideoHelper

2. 配置环境

   ``` bash
   conda create -n VideoHelper python=3.9
   conda activate VideoHelper
   pip install -r requirements.txt
   ```

3. 运行后端

   ```bash
   python ./backend/main.py
   ```

4. 使用python创建本地服务器，点击网址（默认为http://0.0.0.0:8000/）

   ```
   python -m http.server
   ```



## ✨ 主要功能



## ⚙️ 基本配置



## 💡 项目架构

命名方式：本项目前端一般使用驼峰命名法，后端一般使用下划线。

项目的主要目录结构说明如下：

```
VideoHelper/
├── backend/                    # 后端python代码
├── docs/                    	# 文档使用的图片等
├── frontend/					# 前端html\css\js等文件
├── warehouse/					# 存储视频和字幕文件
	├── video/
	├── subtitle/
	├── subtitle_zh/
├── index.html					# 前端主页面
├── requirements.txt			# 后端所需依赖
```

## 📝 说明



## 更新日志

2024.12.11

- 由于之前断断续续的开发，导致代码很... 所以**re0**。<u>基本的下载视频、获取原语言字幕。</u> 而且发现plyr支持vtt字幕，所以不用自己再实现字幕对齐等逻辑了。
- 记录当前开源使用：<u>plyr播放器，you-get, faster-whisper</u>。
- **plyr播放器js,css为在线加载**。
- **faster-whisper模型下载到本地。**

2024.12.7

- 增加video_list板块，可在多个获取过的视频中切换。支持在本地文件夹增加、删除视频（或多个视频）（增加后点击列表右上角加号刷新列表，删除要刷新整个页面以更新list）。后续支持在网页上删除视频，修改视频名称。后续支持选中字幕文本暂停视频。

![](https://gitee.com/myclms/pictures/raw/master/image-20241207225317666.png)

2024.12.6

- 新增 settings.bin，目前只有配置whisper模型大小（用于语音识别）。
- 删除音频提取功能，发现whisper可以直接处理视频!

2024.12.5

- 上传初始代码，实现了基本功能（抓取视频，提取音频，提取字幕）和基本网页前端。

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=myclms/VideoHelper&type=Date)](https://star-history.com/#myclms/VideoHelper&Date)