import asyncio
import websockets
import json
from mylib import get_video, extract_audio, get_subtitle, check_log, update_settings, save_settings, get_settings, send_settings
from vars import msgs

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

        msg = recv['msg']

        if msg == msgs[0] :
            url = recv['url']
            if url=='':
                await websocket.send(json.dumps({'msg':msgs[4],'log':"Please input the url first, then click this button. "}))
            else:
                file_name = await get_video(websocket, url)
                if file_name != '':
                    await websocket.send(json.dumps({'msg':msgs[0],'file_name':file_name}))
            
        elif msg == msgs[1] :
            url = recv['url']
            if url=='':
                await websocket.send(json.dumps({'msg':msgs[4],'log':"Please input the url first, then click this button. "}))
            else:
                file_name = await extract_audio(websocket, url)
                if file_name != '':
                    await websocket.send(json.dumps({'msg':msgs[1],'file_name':file_name}))

        elif msg == msgs[2] :
            url = recv['url']
            if url=='':
                await websocket.send(json.dumps({'msg':msgs[4],'log':"Please input the url first, then click this button. "}))
            else:
                file_name = await get_subtitle(websocket, url)
                if file_name != '':
                    await websocket.send(json.dumps({'msg':msgs[2],'start':-1}))

        elif msg == msgs[5] :
            await update_settings(recv['key'], recv['value'])
            await save_settings()

        # response_text = f"your submit context: {recv_text}"
        # await websocket.send(response_text)

# 服务器端主逻辑
# websocket和path是该函数被回调时自动传过来的，不需要自己传
async def main_logic(websocket):
    await get_settings()
    await send_settings(websocket)
    await check_log(websocket)
    await recv_msg(websocket)

async def main():
    async with websockets.serve(main_logic, '0.0.0.0', 5001):
        await asyncio.Future()  # 这将永远挂起，直到服务器关闭

if __name__ == "__main__":
    asyncio.run(main())



# 字幕翻译
# 美化页面 UI
# you-get 命令行 --> 库调用
