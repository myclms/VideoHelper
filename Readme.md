<div align="center">
  <img src="./docs/images/logo.jpeg"alt="VideoCaptioner Logo" width="100">
  <h1>VideoHelper</h1>
  <p>基于爬虫、语音识别、机器翻译、大语言模型的视频播放助手</p>
</div>

  简体中文 / [English](./docs/Readme_EN.md)

## 📖 项目介绍

​	基于爬虫、语音识别、机器翻译、大语言模型的视频播放助手，定位为一款带有<u>下载视频、生成字幕、字幕翻译</u>等功能的**在本地使用的 ** **网页视频播放器**。本项目借鉴、使用了诸多开源项目的成果，是三名大三学生的专业选修课大作业。

## 📸 界面预览

![](https://gitee.com/myclms/pictures/raw/master/image-20241214152151193.png)



## 🚀 快速开始

1. 克隆本项目或者下载项目文件夹，进入项目目录VideoHelper

2. 配置python环境

   ``` bash
   conda create -n VideoHelper python=3.9
   conda activate VideoHelper
   pip install -r requirements.txt
   ```

3. 下载依赖[Deeplx](https://github.com/OwO-Network/DeepLX/releases)到项目文件夹

3. **linux**下启动（每次启动前都要 “conda activate VideoHelper” 激活python虚拟环境）

   ```sh
   bash launch.sh
   ```

4. 使用

   见[主要功能](#functions)

5. 退出


 <span id="functions"> </span>

## ✨ 主要功能

- **视频下载**：输入网页URL（要求网页存在一个视频，并且为you-get所支持）,为视频取一个名字，下载视频到本地。视频列表自动更新。
- **字幕生成**：点击视频播放器控制条的 “设置”(齿轮图标) -> “Captions” -> “原字幕” ，生成视频字幕文件到本地 ，并且播放器自动加载。
- **字幕翻译**：点击视频播放器控制条的 “设置”(齿轮图标) -> “Captions” -> “中文字幕” ，生成视频字幕文件到本地 ，并且播放器自动加载。
- **视频列表**：支持本地修改，修改后重新启动即可。
- ![](https://gitee.com/myclms/pictures/raw/master/image-20241214152055615.png)

## ⚙️ 基本配置

- **视频下载** 使用开源项目you-get，<u>需要联网</u>下载。
- **字幕生成** 使用本地模型faster-whisper，默认模型规模为**large-v2** 。第一次使用会自动下载模型到默认路径（<u>需要联网</u>），大小大约3G，自动检测GPU。生成速度和电脑配置、视频时长有关。
- **字幕翻译** 使用开源项目deeplx。是部署到本地的服务。



## 💡 项目架构

![](https://gitee.com/myclms/pictures/raw/master/image-20241212220322630.png)

代码命名方式：本项目前端一般使用驼峰命名法，后端一般使用下划线。

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
├── tmp							# 谷歌浏览器运行需要的用户数据目录
├── deeplx_*_*					# deeplx可执行文件
├── index.html					# 前端主页面
├── requirements.txt			# 后端所需依赖
```

## Ackownledgement

- [you-get](https://github.com/soimort/you-get)
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
- [deeplx](https://github.com/OwO-Network/DeepLX)
- [plyr播放器](https://github.com/sampotts/plyr)



## 开发日志

2024.12.17

- 使用BootStrap优化前端页面

2024.12.16

- 添加翻译功能

2024.12.13

- 在本地开服务器解决前端加载本地文件时的跨源问题，发现又引入了视频无法拖动的问题。转而改为仍然本地运行网页，使用shell脚本启动chrome浏览器并且添加参数 “--disable-web-security --user-data-dir=tmp” 以解决跨源问题。同时简化启动方法。

  [参考连接](https://blog.csdn.net/weixin_48594833/article/details/124345191)

- 优化通知UI。

- 增加通过名称搜索已经下载的视频的功能。

2024.12.11

- 由于之前断断续续的开发，导致代码很... 所以**re0**。<u>基本的下载视频、获取原语言字幕。</u> 而且发现plyr支持vtt字幕，所以不用自己再实现字幕对齐等逻辑了。
- 记录当前开源使用：<u>plyr播放器，you-get, faster-whisper</u>。
- **plyr播放器js,css为在线加载**。
- **faster-whisper模型下载到本地。**

2024.12.7

- 增加video_list板块，可在多个获取过的视频中切换。支持在本地文件夹增加、删除视频（或多个视频）（增加后点击列表右上角加号刷新列表，删除要刷新整个页面以更新list）。后续支持在网页上删除视频，修改视频名称。后续支持选中字幕文本暂停视频。

2024.12.6

- 新增 settings.bin，目前只有配置whisper模型大小（用于语音识别）。
- 删除音频提取功能，发现whisper可以直接处理视频!

2024.12.5

- 上传初始代码，实现了基本功能（抓取视频，提取音频，提取字幕）和基本网页前端。

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=myclms/VideoHelper&type=Date)](https://star-history.com/#myclms/VideoHelper&Date)