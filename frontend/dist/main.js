export const socket = new WebSocket('ws://localhost:5001'); // 创建WebSocket连接

document.addEventListener('DOMContentLoaded', function () {
    const videoElement = document.getElementById('videoPlayer');
    const videoList = document.getElementById('videoList');
    const urlElement = document.getElementById("inputSource");
    const vttSourceElement = document.getElementById("vttSource");



    function getFileName(path){
        let index = path.lastIndexOf('/');
		let filename = path.substr(index + 1);
        return filename.split('.')[0];
    }



    // 通信
    socket.onopen = function(event) {
        console.log('连接已打开');
        updateVideoList(); // 初始化视频列表

    };
    socket.onclose = function(event) {
        console.log('连接已关闭');
    };
    socket.onerror = function(error) {
        console.log('Error: ', error);
    };
    // 接收信号
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log(data)
        if(data['type'] == 'download'){
            let name = getFileName(data['path']);
            alert("下载完成:"+name);

            let li = document.createElement('li');
            li.innerText = name;
            li.setAttribute('data-video-src', data['path']);
            videoList.appendChild(li);
        }
        else if(data['type'] == 'transcribe'){
            alert("字幕生成结束");
            vttSourceElement.src = data['path'];
        }
        else if(data['type'] == 'translate'){
            alert("中文字幕生成完成");
        }
        else if(data['type'] == 'updateVideoList'){
            alert("视频列表已更新");
            let videoPaths = data['videoList'];
            for(let i = 0; i < videoPaths.length; i++){
                let li = document.createElement('li');
                li.innerText = getFileName(videoPaths[i]);
                li.setAttribute('data-video-src', videoPaths[i]);
                videoList.appendChild(li);
            }
        }
    };



    // 语音转录
    // 见player.js



    // 日志
    // function beautifyLog() {
    //     $('.text1').textillate({ in: { effect: 'rollIn' } });
    //     $('.text2').textillate({
    //         initialDelay: 500, 	//设置动画开始时间
    //         in: { 
    //             effect: 'flipInX',	//设置动画名称
    //             delay: 50,
    //         }
    //     });
    //     $('.text3').textillate({
    //         initialDelay: 10,
    //         in: { 
    //             effect: 'bounceInDown' ,
    //             delay: 5,
    //         }
    //     });
    // }




    // 下载视频
    urlElement.addEventListener('keydown', function(event){
        if (event.code == 'Enter' && urlElement.value != ''){
            alert("下载视频："+urlElement.value);
            download();
        }
    })
    function download() {
        var videoName = prompt("","给视频取个名字吧");
        
        if (videoName == undefined || videoName == ''){
            alert("下载取消！");
            return;
        }
        
        socket.send(JSON.stringify({
            'type': 'download',
            'url': urlElement.value,
            'name': videoName,
        })
        );
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

    function updateVideoList() {
        alert("正在获取视频列表")
        // 发送获取视频文件夹下所有文件名称的请求
        socket.send(JSON.stringify({
            'type': 'updateVideoList',
        }));
    }

 
});
