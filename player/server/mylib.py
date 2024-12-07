import datetime
import subprocess
import ffmpeg
import json
import pickle
import os
from audio_transcibe import whisper_transcribe, whisper_transcribe_local
from vars import *



def get_time():
    now = datetime.datetime.now()
    return str(datetime.date.today())+'-'+now.strftime('%H-%M-%S')

def write_into_log(time, url, type, name):
    with open(log_name, 'a+') as f:
        f.write(time+'\t'+url + '\t'+type+'\t'+name+'\n')

def write_into_error_log(url, type, error_info):
    with open(error_log_name, 'a+') as f:
        f.write(get_time()+'\n'+url + '\t'+type+'\n'+error_info)

# 遍历log_name文件（逆序，假设最近的更可能会是想找的）每一行
# 找到相同的url则再在最后加一行，并且返回文件名（时间）
# 没找到则返回文件名为''
def confirm_has_type(url:str, type:str):
    # type == mp4, m4a, txt
    has = False
    time = ''
    name = ''

    # 检查log，如果有重复url则不下载
    with open(log_name, 'a+') as f:
        print("............ Checking log ............")
        f.seek(0)
        lines = f.readlines()
        lines.reverse()
        for line in lines:
            t_url = line.split('\t')[1]
            t_type = line.split('\t')[2]
            if url.strip() == t_url.strip() and t_type.strip() == type:
                print("............ Same " + type + ", no need to produce ............")
                has = True
                time = line.split('\t')[0]
                name = line.split('\t')[3].strip()
                break

    if has:
        write_into_log(time, url, type, name)
    
    return has, name

async def get_video(websocket, url:str, video_name:str):
    has_video,file_name = confirm_has_type(url, types[0])
    
    # 下载url对应视频 ———— you-get
    # 将视频保存到本地
    await websocket.send(json.dumps({'msg':msgs[3],'log':'............ Downloading video start ............'}))
    result = subprocess.run(['you-get', '-i', url], capture_output=True, text=True)
    await websocket.send(json.dumps({'msg':msgs[4],'log':result.stdout}))
    write_into_error_log(url, types[0], result.stderr)

    if has_video:
        if file_name != video_name:# 如果文件名不同，则重命名
            os.rename(path_to_raw_video + "/" + file_name + '.mp4', path_to_raw_video + "/" + video_name + '.mp4')

    elif not has_video:
        result = subprocess.run(['you-get', '-o', path_to_raw_video,'-O',video_name, url], capture_output=True, text=True)

        # 谷歌浏览器只支持h264编码格式 h265->h264
        path_raw = path_to_raw_video + "/" + video_name + '.mp4'
        probe = ffmpeg.probe(path_raw)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        if 'H.265' in video_stream['codec_long_name'] :
            path_new = path_to_raw_video + "/" + video_name + '-1.mp4'
            ffmpeg.input(path_raw).output(path_new, vcodec='h264').run()
            os.remove(path_raw)
            os.rename(path_new, path_raw)

        write_into_error_log(url, types[0], result.stderr)
 
    write_into_log(get_time(), url, types[0], video_name)
    await websocket.send(json.dumps({'msg':msgs[3],'log':'............ Downloading video end ............'}))
    await update_list(list_operation_types[0], video_name)
    await send_added_list(websocket)

    return video_name

# async def extract_audio(websocket, url:str):

#     has_audio,file_name_a = confirm_has_type(url, types[1])
#     if has_audio:
#         print("............ Same audio, no need to extract ............")
#     else:
#         has_video,file_name_v = confirm_has_type(url, types[0])
#         if not has_video:
#             await websocket.send(json.dumps({'msg':msgs[4],'log':"Please submit the url first, then click this button. "}))
#             return ''
#         else:
#             # file_name_v != ''
#             # file_name_a == ''
#             file_name_a = get_time()
#             # 提取音频 ———— ffmpeg
#             await websocket.send(json.dumps({'msg':msgs[3],'log':"............ Extracting audio start ............"}))
#             path_a = path_to_raw_audio + '/' + file_name_a + '.' + types[1]
#             path_v = path_to_raw_video + '/' + file_name_v + '.' + types[0]

#             # result = subprocess.run(['ffmpeg', '-i', path_v, '-vn', '-acodec', 'copy', path_a], capture_output=True, text=True)
#             try:
#                 ffmpeg.input(path_v).output(path_a).run()
#             except Exception as ex:
#                 write_into_error_log(url, types[1], ex)
#             # await websocket.send(json.dumps({'msg':msgs[4],'log':result.stderr}))
#             # write_into_error_log(url, types[1], result.stderr)
#             write_into_log(file_name_a, url, types[1])
#             await websocket.send(json.dumps({'msg':msgs[3],'log':"............ Extracting audio end ............"}))

#     return file_name_a
        

async def get_subtitle(websocket, url:str):

    has_sub,file_name_s = confirm_has_type(url, types[2])
    if has_sub:
         await websocket.send(json.dumps({'msg':msgs[2],'start':-2}))
         print("............ Same subtitle, no need to transcibe ............")
         await whisper_transcribe_local(websocket, path_to_raw_sub + '/' + file_name_s + '.' + types[2]) # 读取本地文件发送
         return file_name_s
    else:
        # has_audio,file_name_a = confirm_has_type(url, types[1])
        # if not has_audio:
        #     await websocket.send(json.dumps({'msg':msgs[4],'log':"Please extract audio first, then click this button. "}))
        #     return ''
        # else:
        #     await websocket.send(json.dumps({'msg':msgs[2],'start':-2}))
        #     # file_name_a != '', file_name_s == ''
        #     await websocket.send(json.dumps({'msg':msgs[3],'log':"............ Getting subtitle start (first try may need to download model, please wait minutes ) ............"}))
        #     file_name_s = get_time()
        #     path_s = path_to_raw_sub + '/' + file_name_s + '.' + types[2]
        #     path_a = path_to_raw_audio + '/' + file_name_a + '.' + types[1]
        #     # 语音识别 ———— whisper
        #     # with open(setting_name, 'ab+') as f:
        #     #     model = f.readline().strip()
        #     await whisper_transcribe(websocket, path_a, path_s, 
        #                             model_size=settings['whisper_model_size'] if settings['whisper_model_size'] in model_sizes else 'large-v2') # 转录并保存、发送
        #     write_into_log(file_name_s, url, types[2])
        #     await websocket.send(json.dumps({'msg':msgs[3],'log':"............ Getting subtitle end ............"}))
        #     return file_name_s
        has_video,file_name_v = confirm_has_type(url, types[0])
        if not has_video:
            await websocket.send(json.dumps({'msg':msgs[4],'log':"Please submit the url first, then click this button. "}))
            return ''
        else:
            file_name_s = file_name_v
            await websocket.send(json.dumps({'msg':msgs[2],'start':-2}))
            await websocket.send(json.dumps({'msg':msgs[3],'log':"............ Getting subtitle start (first try may need to download model, please wait minutes ) ............"}))
            path_s = path_to_raw_sub + '/' + file_name_s + '.' + types[2]
            path_v = path_to_raw_video + '/' + file_name_v + '.' + types[0]
            # 语音识别 ———— whisper
            await whisper_transcribe(websocket, path_v, path_s, 
                                    model_size=settings['whisper_model_size'] if settings['whisper_model_size'] in model_sizes else 'large-v2') # 转录并保存、发送
            write_into_log(get_time(), url, types[2], file_name_s)
            await websocket.send(json.dumps({'msg':msgs[3],'log':"............ Getting subtitle end ............"}))
            return file_name_s


async def check_log():
    # await websocket.send(json.dumps({'msg':msgs[3],'log':"............ Checking log start ............"}))
    print("............ Checking log start ............")

    good_lines = []
    urls = []
    with open(log_name, "a+") as f:
        f.seek(0)
        lines = f.readlines()
        for line in lines:
            try:
                t_file_name = line.split('\t')[3].strip()
                t_type = line.split('\t')[2]
                t_url = line.split('\t')[1]
                if t_url in urls:
                    continue
                urls.append(t_url)

                if t_type.strip() == types[0]:
                    if os.path.exists(path_to_raw_video + '/' + t_file_name + '.' + types[0]):
                        good_lines.append(line)
                # elif t_type.strip() == types[1]:
                #     if os.path.exists(path_to_raw_audio  + '/' + t_file_name + '.' + types[1]):
                #         good_lines.append(line)
                elif t_type.strip() == types[2]:
                    if os.path.exists(path_to_raw_sub + '/' + t_file_name + '.' + types[2]):
                        good_lines.append(line)
            except Exception as ex:
                write_into_error_log('check_log', 'check_log', str(ex))

    with open(log_name, "w+") as f:
            for line in good_lines:
                f.write(line)

    # await websocket.send(json.dumps({'msg':msgs[3],'log':"............ Checking log end ............"}))
    print("............ Checking log end ............")

async def get_settings():
    global settings
    print("............ Get settings ............")
    if os.stat(setting_name).st_size != 0 :
        with open(setting_name, 'rb') as f:
            settings = pickle.load(f)

async def save_settings():
    global settings
    print("............ Save settings ............")
    with open(setting_name, 'wb') as f:
        pickle.dump(settings, f)

async def send_settings(websocket):
    global settings
    print("............ Send settings ............")
    print(settings)
    await websocket.send(json.dumps({'msg':msgs[5],'settings':settings}))

async def update_settings(key, value):
    global settings
    print("............ Update settings ............")
    settings[str(key)] = value

async def get_list():
    global video_list
    print("............ Get list ............")
    with open(log_name, "r") as f:
        lines = f.readlines()
        lines = list(set(lines))
        for line in lines:
            t_list = line.split('\t')
            t_name = t_list[3].strip()
            t_type = t_list[2]
            if t_type == types[0]:
                video_list.append(t_name)
            # elif t_type == types[2]:
            #     subs.append(t_name)

async def send_list(websocket):
    global video_list
    print("............ Send list ............")
    await websocket.send(json.dumps({'msg':msgs[6],'video_list':video_list}))

async def send_added_list(websocket):
    global video_list
    print("............ Send update list ............")
    await websocket.send(json.dumps({'msg':msgs[6],'video_list':[video_list[-1]]}))

async def update_list(list_operation:str, name:str=''):
    # 增
    global video_list
    print("............ Update list ............")
    if list_operation_types[0] == list_operation and name:
        video_list.append(name)
    # 删
    # elif list_operation_types[1] == list_operation and name:
    #     video_list.remove(name)
