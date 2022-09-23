from transformers import BertForQuestionAnswering, AutoTokenizer, pipeline


model = BertForQuestionAnswering.from_pretrained("deepset/bert-base-cased-squad2")
tokenizer = AutoTokenizer.from_pretrained("deepset/bert-base-cased-squad2")


def answer_by_context(context, value):
	tokenizer.encode(value, truncation=True, padding=True)
	nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)

	result = nlp({
		"question": value,
		"context": (context)
	})

	print(f"Score (Transformers): {result['score']}")
	return result['answer'] if result["score"] > 0.008 else None