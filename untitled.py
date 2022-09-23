from transformers import BertForQuestionAnswering, AutoTokenizer, pipeline

context = ("""My name is Nexa. I'm 20 years old. I'm pretty :)""")
question = input("you: ")

model = BertForQuestionAnswering.from_pretrained("deepset/bert-base-cased-squad2")
tokenizer = AutoTokenizer.from_pretrained("deepset/bert-base-cased-squad2")
tokenizer.encode(question, truncation=True, padding=True)
nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)

result = nlp({
	"question": question,
	"context": context
})

print(f"Nexa: {result['answer']}")