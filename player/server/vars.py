msgs = ['get_video', 'extract_audio', 'get_subtitle', 'log2', 'log3', 'setting'] # 0 -- 5
types = ['mp4', 'm4a', 'txt']
model_sizes = ['tiny', 'tiny.en', 'base', 'base.en', 'small', 'small.en', 'distil-small.en', 
               'medium', 'medium.en', 'distil-medium.en', 'large-v1', 'large-v2', 'large-v3', 
               'large', 'distil-large-v2', 'distil-large-v3', 'large-v3-turbo', 'turbo']


setting_name = 'settings.bin'
log_name = 'log.txt'
error_log_name = 'error.txt'
path_to_raw_video = 'player/web/video'
path_to_raw_audio = 'player/web/audio'
path_to_raw_sub = 'player/web/sub'

settings = {
    'whisper_model_size': 'large-v2',
}