import subprocess
import httpx
import json
import urllib
import time
import os
from vars import *
from faster_whisper import WhisperModel



# video_list
async def update_video_list(websocket):
    # 遍历文件夹下全部文件名，发送文件路径
    print("update_video_list")
    video_names = os.listdir(video_dir) # 含后缀名
    video_paths = [video_dir + '/' + t for t in video_names if 'mp4' in t]
    
    await websocket.send(json.dumps({'type':types[3],'videoList':video_paths}))
    print("update_video_list success")

# download
async def download(url:str, name:str):
    print("download")
    try:
        result = subprocess.run(['you-get', '-o', video_dir,'-O',name, url], capture_output=True, text=True)
        path_v = video_dir + '/' + name + '.mp4'
        if os.path.exists(path_v):
            print("download success")
            return 'success'
        else:
            print(result.stdout)
            print("download fail")
            return 'fail'
    except Exception as ex:
        print(ex)
        return 'fail'
    
    
# transcribe
async def whisper_transcribe(websocket, name:str, model_size="large-v2", compute_type="int8"):
    print("whisper_transcribe")
    name = urllib.parse.unquote(name)
    path_v = video_dir + '/' + name + '.mp4'
    path_s = path_v.replace('video', 'subtitle').replace('mp4', 'vtt')
    if os.path.exists(path_s):
        await websocket.send(json.dumps({'type':types[1],'path':path_s}))
    else:
        os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

        model = WhisperModel(model_size, device="auto", compute_type=compute_type)

        segments, info = model.transcribe(path_v, beam_size=5)

        print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

        with open(path_s, 'w', encoding='utf-8') as webvtt_file:
            # 写入WebVTT文件头
            webvtt_file.write("WEBVTT\n\n")
            # 转换每一行
            for segment in segments:
                start_s = segment.start % 60
                start_m = int(segment.start // 60)
                end_s = segment.end % 60
                end_m = int(segment.end // 60)               
                webvtt_file.write("%02d:%06.3f --> %02d:%06.3f\n" % (start_m, start_s, end_m, end_s))
                webvtt_file.write(f"{segment.text}\n\n")
        await websocket.send(json.dumps({'type':types[1],'path':path_s}))
    
    print("whisper_transcribe success")

async def translate(websocket, name:str, target_lang="ZH", deeplx_api="http://127.0.0.1:1188/translate"):
    print("translate")
    name = urllib.parse.unquote(name)
    path_v = video_dir + '/' + name + '.mp4'
    path_s = path_v.replace('video', 'subtitle').replace('mp4', 'vtt')
    path_s_zh = path_s.replace('subtitle', 'subtitle_zh')
    # 检查是否生成了目标语言字幕文件
    if os.path.exists(path_s_zh):
        pass
    else:
        # 检查是否生成了原语言字幕文件
        if not os.path.exists(path_s):
            # 生成原语言字幕文件
            await whisper_transcribe(websocket, name)

        # 生成目标语言字幕文件
        sleep_time = 15
        with open(path_s_zh, 'w') as f_zh:
            with open(path_s, 'r') as f:
                for line in f:
                    if line=='\n' or line.startswith('WEBVTT') or '-->' in line:
                        f_zh.write(line)
                    else:
                        # 调用deepl翻译文本
                        src_text = line.strip()
                        data = {
                            "text": src_text,
                            "target_lang": target_lang
                        }
                        post_data = json.dumps(data)
                        try:
                            r = httpx.post(url = deeplx_api, data = post_data).json()
                            while r['code'] != 200:
                                try:
                                    # retry
                                    print("retry: sleep %ds.", sleep_time)
                                    time.sleep(sleep_time)
                                    r = httpx.post(url = deeplx_api, data = post_data).json()
                                    sleep_time += 5
                                except Exception as e:
                                    pass
                        except Exception as e:
                            while type(r)!=type({}) or r['code'] != 200:
                                try:
                                    # retry
                                    print(f"retry: sleep {sleep_time}s.")
                                    time.sleep(sleep_time)
                                    r = httpx.post(url = deeplx_api, data = post_data).json()
                                    sleep_time += 5
                                except Exception as e:
                                    pass
                        # print(r)
                        f_zh.write(r['data'] + '\n')
                        
    await websocket.send(json.dumps({'type':types[2],'path':path_s_zh}))
    print("translate success")
