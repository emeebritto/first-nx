from transformers import BertForQuestionAnswering, AutoTokenizer, pipeline

context = ("""Jogo é toda e qualquer atividade em que exista a figura do jogador (como indivíduo praticante) e regras que podem ser para ambiente restrito ou livre. Geralmente os jogos têm poucas regras e estas tendem a ser simples. Sua presença é importante em vários aspectos, entre eles a regra define o início e fim do jogo. Pode envolver dois ou mais jogando entre si como adversários ou cooperativamente com grupos de adversários. É importante que um jogo tenha adversários interagindo e como resultado de interação exista um vencedor e um perdedor.""")
question = input("you: ")

# model = BertForQuestionAnswering.from_pretrained("deepset/bert-base-cased-squad2")
# tokenizer = AutoTokenizer.from_pretrained("deepset/bert-base-cased-squad2")
# tokenizer.encode(question, truncation=True, padding=True)
# nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)
nlp = pipeline('question-answering', model='pierreguillou/bert-large-cased-squad-v1.1-portuguese')


result = nlp({
	"question": question,
	"context": context
})


def full_answer(question, context, base):
	context = context.split(".")
	count = 0
	for part in context:
		count += len(part)
		if count >= base["start"]:
			return part
	return None


if result["score"] > 0.1:
	print(f"Nexa: {result['answer']}")
	print(f"Nexa (Complex Answer): {full_answer(question=question, context=context, base=result)}")
else: print("??")

print(f"Context: {result['score']}")