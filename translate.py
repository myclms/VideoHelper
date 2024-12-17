import httpx, json

deeplx_api = "http://127.0.0.1:1188/translate"

data = {
	"text": "何も見えないフリをしていた",
	"target_lang": "zh"
}

post_data = json.dumps(data)
r = httpx.post(url = deeplx_api, data = post_data).json()
print(r['code'])
print(r['data'])