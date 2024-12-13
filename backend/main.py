import asyncio
import websockets
import json
from vars import types, video_dir
from mylib import update_video_list, download, whisper_transcribe
import sys



# 接收客户端消息并处理
async def recv_msg(websocket):
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
                # await websocket.send(json.dumps({'type':types[0],'file_name':file_name}))
                pass
            else:
                await websocket.send(json.dumps({'type':types[0],'path':video_dir + '/' + recv['name'] + '.mp4'}))

        elif type == types[1] :
            await whisper_transcribe(websocket, recv['name'])

        elif type == types[2] :
            # await update_settings(recv['key'], recv['value'])
            # await save_settings()
            pass

        elif type == types[3] :
            await update_video_list(websocket)
            

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



# 字幕翻译
# 美化页面 UI
