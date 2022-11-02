from transformers import BertForQuestionAnswering, AutoTokenizer, pipeline
from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
from utils.functions import syncmethod
from time import sleep, time
from threading import Lock
# from transformers import TrOCRProcessor
from PIL import Image
import torch


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Bert:
	def __init__(self):
		super(Bert, self).__init__()
		self._model = None
		self._tokenize = None
		self.auto_del_is_running = False
		self.scheduled_del = 0
		self._lock = Lock()

	@syncmethod
	def auto_delete(self):
		auto_del_is_running = True
		while True:
			sleep(5)
			if time() >= self.scheduled_del:
				self._model = None
				self._tokenizer = None
				self.auto_del_is_running = False
				break


	def _load_data(self):
		self._model = BertForQuestionAnswering.from_pretrained("deepset/bert-base-cased-squad2")
		self._tokenizer = AutoTokenizer.from_pretrained("deepset/bert-base-cased-squad2")
		if not self.auto_del_is_running: self.auto_delete()


	def predict(self, context, value):
		self.scheduled_del = time() + (2 * 60)
		self._lock.acquire()
		if not self._model: self._load_data()
		self._tokenizer.encode(value, truncation=True, padding=True)
		nlp = pipeline('question-answering', model=self._model, tokenizer=self._tokenizer)
		self._lock.release()
		return nlp({
			"question": value,
			"context": (context)
		})


bert = Bert()



def answer_by_context(context, value):
	result = bert.predict(context, value)
	print(f"Score (Transformers): {result['score']}")
	return result['answer'] if result["score"] > 0.1 else None


def caption_from_image(image_paths):
	model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
	feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
	tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
	model.to(device)

	max_length = 16
	num_beams = 4
	gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

	images = []
	for image_path in image_paths:
		i_image = Image.open(image_path)
		if i_image.mode != "RGB":
			i_image = i_image.convert(mode="RGB")

		images.append(i_image)

	pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
	pixel_values = pixel_values.to(device)

	output_ids = model.generate(pixel_values, **gen_kwargs)

	preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
	preds = [pred.strip() for pred in preds]
	return preds


def conversation(value):
	mname = "facebook/blenderbot-400M-distill"
	model = BlenderbotForConditionalGeneration.from_pretrained(mname)
	tokenizer = BlenderbotTokenizer.from_pretrained(mname)
	inputs = tokenizer([value], return_tensors="pt")
	reply_ids = model.generate(**inputs)
	return tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]



# def caption_from_image(image_paths):
# 	image = Image.open(image_paths).convert("RGB")
# 	processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-printed')
# 	model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-printed')
# 	pixel_values = processor(images=image, return_tensors="pt").pixel_values
# 	generated_ids = model.generate(pixel_values)
# 	generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
# 	print("generated_text", generated_text)
# 	return generated_text



# caption = predict_step(['ja24ztazbp86iyvkyton-1527154415.jpeg'])
# print(caption)