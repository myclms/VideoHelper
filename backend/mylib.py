import subprocess
import json
import urllib
from zhipuai import ZhipuAI
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



# translate
async def translate(websocket, name:str, target_lang="ZH", api_key = "", model_size="glm-4-flash"):
    print("translate")
    config = get_config()
    print("config:")
    print(config)
    api_key = config['translate']['api_key']
    if config['translate']['model_size'] != "":
        model_size = config['translate']['model_size'] 
    if api_key == "" :
        await websocket.send(json.dumps({'type':types[4],'msg':'apiToken is null.'}))
        print("apiToken is null.")
        return
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
        with open(path_s, "r") as f:
            vtt_text = f.read()

        client = ZhipuAI(api_key=api_key) # 填写您自己的APIKey
        response = client.chat.completions.create(
            model=model_size,  # 填写需要调用的模型编码
            messages=[
                {"role": "user", "content": """
                你是一位精通简体中文的专业翻译，曾参与诸多国际电影、热门视频的字幕翻译工作，因此对于字幕的翻译有深入的理解。我希望你能帮我将以下字幕段落翻译成中文。
                规则：
                - 翻译时要准确传达电影或者视频含义。
                - 保留特定的术语或名字，并在其前后加上空格，例如："中 UN 文"。
                - 保留原本的vtt字幕格式。
                - 分成两次翻译，只需要打印第二次意译的结果：
                1. 根据字幕内容直译，不要遗漏任何信息
                2. 根据第一次直译的结果重新意译，遵守原意的前提下让内容更通俗易懂，符合中文表达习惯

                本条消息只需要回复OK，接下来的消息我将会给你发送完整内容，收到后请按照上面的规则打印第二次意译的翻译结果，并且保证打印结果符合webvtt字幕文件格式要求。"""},
                {"role": "assistant", "content": "OK"},
                {"role": "user", "content": vtt_text}
            ],  
        )
        with open(path_s_zh, "w") as f:
            f.write(response.choices[0].message.content)
                        
    await websocket.send(json.dumps({'type':types[2],'path':path_s_zh}))
    print("translate success")



# setting
def get_config():
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

async def init_setting(websocket):
    print("setting")
    config = get_config()
    await websocket.send(json.dumps({'type':types[5],'config':dict(config)}))
    print("setting success")



# translate_setting
async def update_translate_setting(websocket, m:str, a:str):
    print("update_translate_setting")
    config = get_config()

    config['translate']['model_size'] = m
    config['translate']['api_key'] = a

    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)

    await websocket.send(json.dumps({'type':types[6]}))
    print("update_translate_setting success")
