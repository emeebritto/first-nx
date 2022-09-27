from transformers import BertForQuestionAnswering, AutoTokenizer, pipeline
import re


model = BertForQuestionAnswering.from_pretrained("deepset/bert-base-cased-squad2")
tokenizer = AutoTokenizer.from_pretrained("deepset/bert-base-cased-squad2")
nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)

context = ("""I'm happy. July is happy. cat is red.""")


def full_answer(question, context, base):
	context = context.split(".")
	count = 0
	for part in context:
		count += len(part)
		if count >= base["start"]:
			return part
	return None


while True:
	question = input("you: ")
	# question = re.sub(r"(are)? you('re| are)?", "am I", question)
	print(question)
	tokenizer.encode(question, truncation=True, padding=True)
	# nlp = pipeline('question-answering', model='pierreguillou/bert-large-cased-squad-v1.1-portuguese')

	result = nlp({
		"question": question,
		"context": context
	})

	if result["score"] > 0.02:
		print(f"Nexa: {result['answer']}")
		print(f"Nexa (Complex Answer): {full_answer(question=question, context=context, base=result)}")
	else: print("??")

	print(f"Score: {result['score']}")