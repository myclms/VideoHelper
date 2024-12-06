const videoElement = document.querySelector("video");
const inputElement = document.querySelector("input[type='text']");
const logElement = document.querySelector("div.log");
const subElement = document.querySelector(".getSubtitle")
const whisperElement = document.querySelector("#whisper_model_size")



const socket = new WebSocket('ws://localhost:5001'); // 创建WebSocket连接
const sub_list = []; // 创建字幕队列
const rate = 1 * 1000; // 刷新字幕时间间隔(/ms)
const eps = 0.1;
const maxlog = 3;



var current_log_num = 2;
let showing = false;
let sending_sub = false;
var last_video_url = '';
var last_audio_url = '';
var last_sub_url = '';
let last_video_time=0, current_video_time=0;
let sub_index = -1;



socket.onopen = function(event) {
    console.log('连接已打开');
};

socket.onclose = function(event) {
    console.log('连接已关闭');
};

socket.onerror = function(error) {
    console.log('Error: ', error);
};

// 接收并处理信息
socket.onmessage = (event) => {
    // console.log('Receive: ', event.data);
    const data = JSON.parse(event.data);

    if (data.msg == 'get_video') {
        videoElement.src = 'video/' + data.file_name + '.mp4';
        // console.log(videoElement.src)
        videoElement.load();
    }
    // else if (data.msg == 'extract_audio') {
    //     // path_a = 'audio/' + data.file_name + '.m4a';
    // }
    else if (data.msg == 'get_subtitle') {
        // console.log(String(data.start)+' --> '+String(data.end)+'    '+String(data.subtitle));
        if (data.subtitle) {
            if(data.start == -1){// 传输完毕
                sending_sub = false
                // find_subtitles(0, sub_list.length-1);
            }
            else if(data.start == -2){// 开始传输
                sending_sub = true
                last_sub_url = inputElement.value
            }
            else{// 正在传输
                // 放进字幕队列
                sub_list.push({'start':data.start, 'end':data.end, 'subtitle':data.subtitle});
            }
        }
    }
    else if (data.msg == 'log2' || data.msg == 'log3') {
        if (current_log_num >= maxlog){
            tE = logElement.querySelector("p");
            if(tE){
                tE.remove();
            }
        }

        pElement = document.createElement("p");
        // console.log(data.msg)
        if (data.msg == 'log2'){
            pElement.className = 'text2'
        }
        else if (data.msg == 'log3'){
            pElement.className = 'text3'
        }
        pElement.innerText = data.log;
        logElement.appendChild(pElement);
        beautify_log();
        current_log_num += 1;
    }
    else if (data.msg == 'setting') {
        // console.log(data.settings)
        whisperElement.value = data.settings.whisper_model_size;
    }
};

function get_video() {
    if (inputElement.value != last_video_url){
        socket.send(JSON.stringify({
            'msg': 'get_video',
            'url': inputElement.value,
        })
        );
        last_video_url = inputElement.value;
    }
}

// function aud_button_click() {
//     if (inputElement.value != last_audio_url){
//         socket.send(JSON.stringify({
//             'msg': 'extract_audio',
//             'url': inputElement.value,
//         }))
//         last_audio_url = inputElement.value;
//     }
// }

function sub_button_click() {
    if(showing){
        $d.style.opacity = 0
        showing = false
    }
    else{
        create_subtitle()
        showing = true
        if(! sending_sub && inputElement.value != last_sub_url){
            sub_list.length = 0;
            socket.send(JSON.stringify({
                'msg': 'get_subtitle',
                'url': inputElement.value,
            }))
        }
        find_subtitles(0, sub_list.length-1)
    }
}

function set_whisper_model_size() {
    socket.send(JSON.stringify({
        'msg': 'setting',
        'key': 'whisper_model_size',
        'value': whisperElement.value,
    }))
}

videoElement.addEventListener("timeupdate", function () {
    // console.log("timeupdate:" + videoElement.currentTime);

    if (showing){
        sub_index = find_subtitles(0, sub_list.length-1);
        if(sub_index>-1 && sub_index<sub_list.length){
            $d.innerText = sub_list[sub_index]['subtitle'];
        }
    }
    setTimeout(()=>{
        ;
    }, rate);
});

// 二分查找字幕列表（有序），寻找适合当前时间的字幕显示到d
function find_subtitles(l, r) {
    if (l > r){
        return -1;
    }
    const mid = Math.floor((l+r)/2);
    if (mid<0 || mid>=sub_list.length){
        return -1;
    }  
    // 获取视频的当前播放时间
    const currentTime = videoElement.currentTime;
    // 获取字幕的起始时间和结束时间
    const start_time = sub_list[mid]['start'];
    const end_time = sub_list[mid]['end'];
    if (currentTime >= start_time-eps && currentTime <= end_time+eps) {
        return mid;
    }
    else {
        if (currentTime < start_time){
            return find_subtitles(l, mid-1);
        }
        else{
            return find_subtitles(mid+1, r);
        }
    }
}

let $d
function create_subtitle() {
    $d = document.createElement('div')
    $d.style.position = 'absolute'
    $d.style.bottom = '20px'
    $d.style.left = '50%'
    $d.style.transform = 'translateX(-50%)'
    $d.style.color = 'white'
    $d.style.fontSize = '24px'
    $d.style.opacity = 1
    $d.style.backgroundColor = 'rgba(0,0,0,0.5)'
    $d.style.padding = '10px'
    $d.style.borderRadius = '5px'
    $d.style.zIndex = 9999
    $d.style.transition = 'opacity 1s'
    $d.innerText = '............'
    // append 相邻 video
    videoElement.parentElement.appendChild($d)
}

function beautify_log() {
    $('.text1').textillate({ in: { effect: 'rollIn' } });
    $('.text2').textillate({
        initialDelay: 500, 	//设置动画开始时间
        in: { 
            effect: 'flipInX',	//设置动画名称
            delay: 50,
        }
    });
    $('.text3').textillate({
        initialDelay: 10,
        in: { 
            effect: 'bounceInDown' ,
            delay: 5,
        }
    });
}
