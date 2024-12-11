import re
string = "http://0.0.0.0:8000/warehouse/video/雨爱.mp4"
pattern = r'http://[^/]*/'
string = re.sub(pattern, '', string)
print(string)