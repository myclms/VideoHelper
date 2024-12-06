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

2024.11.23

- 新增 Whisper-v3 模型支持，大幅提升语音识别准确率

- 优化字幕断句算法，提供更自然的阅读体验

- 修复检测模型可用性时的稳定性问题

  

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=myclms/VideoHelper&type=Date)](https://star-history.com/#myclms/VideoHelper&Date)