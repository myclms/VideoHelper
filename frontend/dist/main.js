document.addEventListener('DOMContentLoaded', function () {
    var socket = new WebSocket('ws://localhost:5001'); // 创建WebSocket连接
    const videoElement = document.getElementById('videoPlayer');
    const videoList = document.getElementById('videoList');
    const urlElement = document.getElementById("inputSource");
    const searchElement = document.getElementById("search");
    const vttSourceElement = document.getElementById("vttSource");
    const vttSourceZHElement = document.getElementById("vttSourceZH");
    const player = new Plyr('#videoPlayer', {

    });
    player.captions.active = false;
    var downloadVideoLoading;
    var subtitleLoading;
    var listLoading;
    var sendSubtitle = false;



    function getFileName(path){
        let index = path.lastIndexOf('/');
		let filename = path.substr(index + 1);
        return filename.split('.')[0];
    }



    // 通信
    socket.onopen = function(event) {
        Qmsg.success('成功连接到后端');
        updateVideoList(); // 初始化视频列表

    };
    socket.onclose = function(event) {
        Qmsg.warning('连接已关闭');
    };
    socket.onerror = function(error) {
        Qmsg.error("无法连接到后端");
    };
    // 接收信号
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log(data)
        if(data['type'] == 'download'){
            downloadVideoLoading.close();
            let name = getFileName(data['path']);
            Qmsg.success("下载完成:"+name);

            let li = document.createElement('li');
            li.innerText = name;
            li.setAttribute('data-video-src', data['path']);
            videoList.appendChild(li);
        }
        else if(data['type'] == 'transcribe'){
            subtitleLoading.close();
            Qmsg.success("字幕生成成功");
            vttSourceElement.src = data['path'];
            sendSubtitle = false;
        }
        else if(data['type'] == 'translate'){
            subtitleLoading.close();
            Qmsg.success("字幕翻译成功");
            vttSourceZHElement.src = data['path'];
            sendSubtitle = false;
        }
        else if(data['type'] == 'updateVideoList'){
            listLoading.close();
            Qmsg.success("视频列表更新",{
                timeout:1500,
            });
            let videoPaths = data['videoList'];
            for(let i = 0; i < videoPaths.length; i++){
                let li = document.createElement('li');
                li.innerText = getFileName(videoPaths[i]);
                li.setAttribute('data-video-src', videoPaths[i]);
                videoList.appendChild(li);
            }
        }
        else if(data['type'] == 'error'){
            Qmsg.error(data['msg']);
        }
    };



    // 语音转录和字幕翻译
    var captionEnabled = false;

    player.on('ready', (event)=>{
        let currentSubtitlePath = ''; // 记录对应的视频路径
        let currentSubtitlePathZH = '';
        const videoElement = document.getElementById('videoPlayer');

        player.on('captionsenabled', (event)=>{
            let currentVideoPath = videoElement.src;
            if(! event.detail.plyr.captions.active){ // 关闭字幕
                return;
            }
            if(currentVideoPath == ''){ // 视频未加载
                return;
            }
            if(captionEnabled == false){ // 第一次开启字幕会发送两次active信号，这里过滤第一个信号
                captionEnabled = true;
                return;
            }
            if(sendSubtitle){
                Qmsg.warning("有字幕正在生成，请稍后重试");
                return;
            }
            else{
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
                            'name': getFileName(currentSubtitlePath),
                        })
                        );
                        sendSubtitle = true;
                        subtitleLoading = Qmsg.loading("正在生成字幕");
                    }
                }
                else if(event.detail.plyr.captions.language == "zh"){
                    console.log("zh");
                    // 判断currentSubtitlePath==currentVideoPath,Y->return,N->sendRequest
                    if(currentSubtitlePathZH == currentVideoPath){
                        console.log("sameZH");
                        return;
                    }
                    else{
                        currentSubtitlePathZH = currentVideoPath;
                        socket.send(JSON.stringify({
                            'type': 'translate',
                            'name': getFileName(currentSubtitlePathZH),
                        })
                        );
                        sendSubtitle = true;
                        subtitleLoading = Qmsg.loading("正在翻译字幕");
                    }
                }
            }       
        });
    })



    // 下载视频
    urlElement.addEventListener('keydown', function(event){
        if (event.code == 'Enter' && urlElement.value != ''){
            Qmsg.info("下载视频："+urlElement.value,{
                timeout:3000,
            });
            download();
        }
    })
    function download() {
        var videoName = prompt("","给视频取个名字吧");
        
        if (videoName == undefined || videoName == ''){
            Qmsg.info("下载取消！");
            return;
        }
        
        socket.send(JSON.stringify({
            'type': 'download',
            'url': urlElement.value,
            'name': videoName,
        })
        );
        downloadVideoLoading = Qmsg.loading("正在下载视频");
    }



    // 视频列表
    videoList.addEventListener('click', function (e) {
        if (e.target && e.target.nodeName === 'LI') {
            var videoSrc = e.target.getAttribute('data-video-src');
            videoElement.src = videoSrc;
            // videoElement.play();
            var items = videoList.getElementsByTagName('li');
            for (var i = 0; i < items.length; i++) {
                items[i].classList.remove('active');
            }
            e.target.classList.add('active');
        }
    });

    searchElement.addEventListener('keydown', function(event){
        if (event.code == 'Enter' && searchElement.value != ''){
            var items = videoList.getElementsByTagName('li');
            var inlist = [];
            var notinlist = []; 
            for (var i = 0; i < items.length; i++) {
                if (items[i].innerText.includes(searchElement.value)){
                    inlist.push(items[i]);
                }
                else{
                    notinlist.push(items[i]);
                }
            }
            videoList.length = 0;
            for(var i = 0; i < inlist.length; i++){
                videoList.appendChild(inlist[i]);
            }
            for(var i = 0; i < notinlist.length; i++){
                videoList.appendChild(notinlist[i]);
            }
        }
    });

    function updateVideoList() {
        listLoading = Qmsg.loading("正在获取视频列表")
        // 发送获取视频文件夹下所有文件名称的请求
        socket.send(JSON.stringify({
            'type': 'updateVideoList',
        }));
    }
 
});
