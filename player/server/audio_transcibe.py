from faster_whisper import WhisperModel
import os
import json
from vars import msgs


async def send_one_sub(websocket, subtitle:str, start_time:float, end_time:float):
    # sio.emit('subtitle', {'subtitle': subtitle, 'start':start_time, 'end':end_time})
    await websocket.send(json.dumps({'msg':msgs[2], 'start':start_time, 'end':end_time, 'subtitle': subtitle}))


# 语音转文字
async def whisper_transcribe(websocket, path_a:str, path_s:str, model_size="large-v2", compute_type="int8"):
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

    model = WhisperModel(model_size, device = "auto", compute_type=compute_type)

    segments, info = model.transcribe(path_a, beam_size=5)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    with open(path_s, 'w') as f:
        for segment in segments:
            f.write(str(format(segment.start, '.2f')) + '\t' + str(format(segment.end, '.2f') + '\t' + segment.text + '\n'))
            await send_one_sub(websocket, segment.text, segment.start, segment.end)


# 发送本地字幕
async def whisper_transcribe_local(websocket, path_s):
    with open(path_s, 'r') as f:
        lines = f.readlines()
        for line in lines:
            things = [t.strip() for t in line.split('\t')]
            await send_one_sub(websocket, things[2], float(things[0]), float(things[1]))