import subprocess
import ffmpeg
import json
import urllib
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

# download
async def download(url:str, name:str):
    print("download")
    try:
        result = subprocess.run(['you-get', '-o', video_dir,'-O',name, url], capture_output=True, text=True)
        path_v = video_dir + '/' + name + '.mp4'
        if os.path.exists(path_v):
            return 'success'
        else:
            print(result.stdout)
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

async def translate(websocket, name:str, target_lang:str):
    pass
    path_s_zh = ''
    await websocket.send(json.dumps({'type':types[2],'path':path_s_zh}))
