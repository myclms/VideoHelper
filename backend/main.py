import asyncio
import websockets
import json
from vars import types, video_dir
from mylib import update_video_list, download, whisper_transcribe

# 检测客户端权限，用户名密码通过才能退出循环
# async def check_permit(websocket):
#     while True:
#         recv_str = await websocket.recv()
#         cred_dict = recv_str.split(":")
#         if cred_dict[0] == "admin" and cred_dict[1] == "123456":
#             response_str = "congratulation, you have connect with server\r\nnow, you can do something else"
#             await websocket.send(response_str)
#             return True
#         else:
#             response_str = "sorry, the username or password is wrong, please submit again"
#             await websocket.send(response_str)

# 接收客户端消息并处理，这里只是简单把客户端发来的返回回去
async def recv_msg(websocket):
    while True:
        recv = await websocket.recv()
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
            await whisper_transcribe(websocket, recv['path'])

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

async def main():
    async with websockets.serve(main_logic, '0.0.0.0', 5001):
        await asyncio.Future()  # 这将永远挂起，直到服务器关闭

if __name__ == "__main__":
    asyncio.run(main())



# 视频列表
# 字幕翻译
# 美化页面 UI
# you-get 命令行 --> 库调用
# log（视频信息）优化
