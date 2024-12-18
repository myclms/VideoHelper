types = ['download', 'transcribe', 'translate', 'updateVideoList', 'error', 'setting', 'translateSetting']
video_dir = 'warehouse/video'
config_file = 'config.json'

"""
download:
    request:
    {
        'type': 'download',
        'url': urlElement.value : str,
        'name': videoName : str,
    }
    response:
    {
        'type': 'download',
        'path': videoPath : str,
    }

transcribe:
    request:
    {
        'type': 'transcribe',
        'name': getFileName(currentSubtitlePath) : str,
    }
    response:
    {
        'type': 'transcribe',
        'path': subtitlePath : str,
    }

translate:
    request:
    {
        'type': 'translate',
        'name': getFileName(currentSubtitlePathZH) : str,
    }
    response:
    {
        'type': 'translate',
        'path': subtitlePathZH : str,
    }

updateVideoList:
    request:
    {
        'type': 'updateVideoList',
    }
    response:
    {
        'type': 'updateVideoList',
        'videoList': videoList : list,
    }

error:
    {
        'type': 'error',
        'msg': message : str,
    }

translateSetting:
    {
        'type': 'translateSetting',
        'modelSize': str,
        'apiToken': str,
    }
"""