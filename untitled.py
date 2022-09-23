from transformers import BertForQuestionAnswering, AutoTokenizer, pipeline

context = ("""the cat is red and the house is yellow""")
question = input("you: ")

model = BertForQuestionAnswering.from_pretrained("deepset/bert-base-cased-squad2")
tokenizer = AutoTokenizer.from_pretrained("deepset/bert-base-cased-squad2")
tokenizer.encode(question, truncation=True, padding=True)
nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)

result = nlp({
	"question": question,
	"context": context
})

if result["score"] > 1: print(f"Nexa: {result['answer']}")
else: print("??")

print(f"Context: {result['score']}")