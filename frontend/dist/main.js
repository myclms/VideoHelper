document.addEventListener('DOMContentLoaded', function() {
    var socket = new WebSocket('ws://localhost:5001'); // 创建WebSocket连接
    const videoElement = document.getElementById('videoPlayer');
    const videoList = document.getElementById('videoList');
    const videoTitleElement = document.getElementById('videoName');
    const urlElement = document.getElementById("url");
    const downloadElement = document.getElementById("download");
    const nameElement = document.getElementById("name");
    const searchElement = document.getElementById("search");
    const vttSourceElement = document.getElementById("vttSource");
    const vttSourceZHElement = document.getElementById("vttSourceZH");
    const translateSettingElement = document.getElementById("translateSetting");
    const modelSizeElement = document.getElementById("modelSize");
    const apiTokenElement = document.getElementById("apiToken");
    const player = new Plyr('#videoPlayer', {

    });
    player.captions.active = false;
    var downloadVideoLoading;
    var subtitleLoading;
    var listLoading;
    var sendSubtitle = false;



    function getFileName(path) {
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
        if (data['type'] == 'download') {
            downloadVideoLoading.close();
            let name = getFileName(data['path']);
            Qmsg.success("下载完成:" + name);

            let li = document.createElement('li');
            li.setAttribute('data-video-src', data['path']);
            li.className = "list-group-item";
            li.innerHTML += '<img class="playing-gif none-display" src="frontend/playing.gif" /> ' + name;
            videoList.appendChild(li);
        } else if (data['type'] == 'transcribe') {
            subtitleLoading.close();
            Qmsg.success("字幕生成成功");
            vttSourceElement.src = data['path'];
            sendSubtitle = false;
        } else if (data['type'] == 'translate') {
            subtitleLoading.close();
            Qmsg.success("字幕翻译成功");
            vttSourceZHElement.src = data['path'];
            sendSubtitle = false;
        } else if (data['type'] == 'updateVideoList') {
            listLoading.close();
            Qmsg.success("视频列表已更新", {
                timeout: 1500,
            });
            let videoPaths = data['videoList'];
            for (let i = 0; i < videoPaths.length; i++) {
                let li = document.createElement('li');
                li.setAttribute('data-video-src', videoPaths[i]);
                li.className = "list-group-item";
                li.innerHTML += '<img class="playing-gif none-display" src="frontend/playing.gif" /> ' + getFileName(videoPaths[i]);
                videoList.appendChild(li);
            }
        } else if (data['type'] == 'error') {
            Qmsg.error(data['msg']);
            if ('apiToken is null.' == data['msg']) {
                subtitleLoading.close();
            }
        } else if (data['type'] == 'setting') {
            modelSizeElement.value = data['config']['translate']['model_size'];
            apiTokenElement.value = data['config']['translate']['api_key'];
        } else if (data['type'] == 'translateSetting') {
            Qmsg.success("翻译设置已保存")
        }

    };



    // 语音转录和字幕翻译
    var captionEnabled = false;

    player.on('ready', (event) => {
        player.pause();
        let currentSubtitlePath = ''; // 记录对应的视频路径
        let currentSubtitlePathZH = '';

        player.on('captionsenabled', (event) => {
            let currentVideoPath = videoElement.src;
            if (!event.detail.plyr.captions.active) { // 关闭字幕
                captionEnabled = false;
                return;
            }
            if (currentVideoPath == '') { // 视频未加载
                return;
            }
            if (captionEnabled == false) { // 第一次开启字幕会发送两次active信号，这里过滤第一个信号
                captionEnabled = true;
                return;
            }
            if (sendSubtitle) {
                Qmsg.warning("有字幕正在生成，请稍后重试");
                return;
            } else {
                if (event.detail.plyr.captions.language == "en") {
                    console.log("en");
                    // 判断currentSubtitlePath==currentVideoPath,Y->return,N->sendRequest
                    if (currentSubtitlePath == currentVideoPath) {
                        console.log("sameEN");
                        return;
                    } else {
                        currentSubtitlePath = currentVideoPath;
                        socket.send(JSON.stringify({
                            'type': 'transcribe',
                            'name': getFileName(currentSubtitlePath),
                        }));
                        sendSubtitle = true;
                        subtitleLoading = Qmsg.loading("正在生成字幕");
                    }
                } else if (event.detail.plyr.captions.language == "zh") {
                    console.log("zh");
                    // 判断currentSubtitlePath==currentVideoPath,Y->return,N->sendRequest
                    if (currentSubtitlePathZH == currentVideoPath) {
                        console.log("sameZH");
                        return;
                    } else {
                        currentSubtitlePathZH = currentVideoPath;
                        socket.send(JSON.stringify({
                            'type': 'translate',
                            'name': getFileName(currentSubtitlePathZH),
                        }));
                        sendSubtitle = true;
                        subtitleLoading = Qmsg.loading("正在翻译字幕");
                    }
                }
            }
        });
    })



    // 下载视频
    downloadElement.addEventListener('click', function(event) {
        Qmsg.info("下载视频：" + nameElement.value, {
            timeout: 2000,
        });

        socket.send(JSON.stringify({
            'type': 'download',
            'url': urlElement.value,
            'name': nameElement.value,
        }));
        downloadVideoLoading = Qmsg.loading("正在下载视频");
    })



    // 视频列表
    videoList.addEventListener('click', function(e) {
        var videoSrc = e.target.getAttribute('data-video-src');
        videoElement.src = videoSrc;
        videoTitleElement.innerText = e.target.innerText;
        // videoElement.play();
        var items = videoList.getElementsByTagName('li');
        for (var i = 0; i < items.length; i++) {
            items[i].firstElementChild.classList.add('none-display');
            items[i].classList.remove('playing');
        }
        e.target.firstElementChild.classList.remove('none-display');
        e.target.classList.add('playing');
    });

    searchElement.addEventListener('keydown', function(event) {
        if (event.code == 'Enter' && searchElement.value != '') {
            var items = videoList.getElementsByTagName('li');
            var inlist = [];
            var notinlist = [];
            for (var i = 0; i < items.length; i++) {
                if (items[i].innerText.includes(searchElement.value)) {
                    inlist.push(items[i]);
                } else {
                    notinlist.push(items[i]);
                }
            }
            videoList.length = 0;
            for (var i = 0; i < inlist.length; i++) {
                videoList.appendChild(inlist[i]);
            }
            for (var i = 0; i < notinlist.length; i++) {
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



    // 设置
    translateSettingElement.addEventListener('click', function(event) {
        modelSize = modelSizeElement.value;
        apiToken = apiTokenElement.value;
        // console.log(modelSize);
        // console.log(apiToken);
        socket.send(JSON.stringify({
            'type': 'translateSetting',
            'modelSize': modelSize,
            'apiToken': apiToken,
        }));
    })

});