import gradio as gr
import re
# import requests
# import json

io1 = gr.Interface.load("spaces/keras-io/question_answering")
def question_answering(value, context):
	context = re.sub(r'(\s)+', ' ', context)
	context = re.sub(r'(\n)+', '\n', context)
	# context = re.sub(r'\W+', ' ', context)
	result = io1(context, value)
	print(result)
	return result[0]


# def question_answering(value, context):
# 	result = requests.post("https://keras-io-question-answering.hf.space/api/predict", data=json.dumps({
# 		"cleared": False,
# 		"data":[context, value],
# 		"session_hash":"hpynipjq3ih"
# 	}), headers={
# 		"Host": "keras-io-question-answering.hf.space",
# 		"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0",
# 		"Accept": "*/*",
# 		"Accept-Language": "en-US,en;q=0.5",
# 		"Accept-Encoding": "gzip, deflate, br",
# 		"Referer": "https://keras-io-question-answering.hf.space/",
# 		"Content-Type": "application/json",
# 		"Content-Length": "73309",
# 		"Origin": "https://keras-io-question-answering.hf.space",
# 		"DNT": "1",
# 		"Connection": "keep-alive",
# 		"Cookie": "session-space-cookie=14ce8d266aad6659609c01dbf35caaaa",
# 		"Sec-Fetch-Dest": "empty",
# 		"Sec-Fetch-Mode": "cors",
# 		"Sec-Fetch-Site": "same-origin",
# 		"Sec-GPC": "1",
# 		"Pragma": "no-cache",
# 		"Cache-Control": "no-cache"
# 	})


# 	data = result.json()
# 	print(data)
# 	res = data["data"][0]
# 	return res
