import asyncio
import websockets
import json
from vars import types, video_dir
from mylib import update_video_list, download, whisper_transcribe, translate, update_translate_setting, init_setting
import sys



# 接收客户端消息并处理
async def recv_msg(websocket):
    await init_setting(websocket)
    while True:
        try:
            recv = await websocket.recv()
        except websockets.ConnectionClosedOK:
            print("Client closed connection")
            return
        try:
            recv = json.loads(recv)
        except Exception as e:
            print('Error: ',e)
            continue
    
        print('Receive: ',recv)

        type = recv['type']

        if type == types[0] :
            url = recv['url']
            status = await download(url, recv['name'])
            if status != 'success':
                await websocket.send(json.dumps({'type':types[4],'msg':'下载失败'}))
            else:
                await websocket.send(json.dumps({'type':types[0],'path':video_dir + '/' + recv['name'] + '.mp4'}))

        elif type == types[1] :
            await whisper_transcribe(websocket, recv['name'])

        elif type == types[2] :
            await translate(websocket, recv['name'], 'zh')

        elif type == types[3] :
            await update_video_list(websocket)

        elif type == types[6] :
            await update_translate_setting(websocket, recv['modelSize'], recv['apiToken'])

        # response_text = f"your submit context: {recv_text}"
        # await websocket.send(response_text)

# 服务器端主逻辑
# websocket和path是该函数被回调时自动传过来的，不需要自己传
async def main_logic(websocket):
    await recv_msg(websocket)
    sys.exit(0)

async def main():
    async with websockets.serve(main_logic, '0.0.0.0', 5001):
        print("Server started on ws://0.0.0.0:5001")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())



# 多种语言的识别不准确
# 优化速度、准确率
# 使用先进的框架
