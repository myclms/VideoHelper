import  { socket } from './main.js'

const player = new Plyr('#videoPlayer', {

});
player.captions.active = false;

var sendSubtitle = false;

player.on('ready', (event)=>{
    let currentSubtitlePath = ''; // 记录对应的视频路径
    let currentSubtitlePathZH = '';
    const videoElement = document.getElementById('videoPlayer');
    let captionEnabled = false;

    player.on('captionsenabled', (event)=>{
        let currentVideoPath = videoElement.src;
        if(currentVideoPath == ''){
            return;
        }
        if(captionEnabled == false){// 第一次开启字幕会发送两次active信号，这里过滤第一个信号
            captionEnabled = true;
            return;
        }
        // console.log(event.detail.plyr);
        console.log("active");
        if(sendSubtitle){
            alert("有字幕正在生成，请稍等");
            return;
        }
        else{
            sendSubtitle = true;
            
            if(event.detail.plyr.captions.language == "en"){
                console.log("en");
                // 判断currentSubtitlePath==currentVideoPath,Y->return,N->sendRequest
                if(currentSubtitlePath == currentVideoPath){
                    console.log("sameEN");
                    return;
                }
                else{
                    currentSubtitlePath = currentVideoPath;
                    socket.send(JSON.stringify({
                        'type': 'transcribe',
                        'path': currentSubtitlePath,
                    })
                    );
                    alert("正在生成字幕");
                }
            }
            else if(event.detail.plyr.captions.language == "zh"){
                console.log("zh");
                return;
            }
        }       
    });
})