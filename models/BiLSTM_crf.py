import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.optim as optim
from utils.nltk_utils import tokenords, stem
from skils.learning import Learning

torch.manual_seed(1)


def argmax(vec):
	# return the argmax as a python int
	_, idx = torch.max(vec, 1)
	return idx.item()


def seq_to_ix(seq, to_ix, train=True):
	idxs = []
	seq = seq.split() if isinstance(seq, str) else seq
	for word in seq:
		if word not in to_ix:
			w_idx = len(to_ix) + 1
			if train: to_ix[word] = w_idx
			idxs.append(w_idx if train else 0)
		else:
			idxs.append(to_ix[word])
	return torch.tensor(idxs, dtype=torch.long)



def ix_to_seq(seq, to_seq):
	return [to_seq[ix] for ix in seq]


# Compute log sum exp in a numerically stable way for the forward algorithm
def log_sum_exp(vec):
	max_score = vec[0, argmax(vec)]
	max_score_broadcast = max_score.view(1, -1).expand(1, vec.size()[1])
	return max_score + \
		torch.log(torch.sum(torch.exp(vec - max_score_broadcast)))


START_TAG = "<START>"
STOP_TAG = "<STOP>"


class BiLSTM_CRF(nn.Module):
	def __init__(self, vocab_size, tag_to_ix, embedding_dim, hidden_dim):
		super(BiLSTM_CRF, self).__init__()
		self.embedding_dim = embedding_dim
		self.hidden_dim = hidden_dim
		self.vocab_size = vocab_size
		self.word_to_ix = {}
		self.tag_to_ix = tag_to_ix
		self.ix_to_tag = { val:key for key, val in self.tag_to_ix.items() }
		self.tagset_size = len(self.tag_to_ix)

		self.word_embeds = nn.Embedding(vocab_size, embedding_dim)
		self.lstm = nn.LSTM(embedding_dim, hidden_dim // 2,
			num_layers=1, bidirectional=True)

		# Maps the output of the LSTM into tag space.
		self.hidden2tag = nn.Linear(hidden_dim, self.tagset_size)

		# Matrix of transition parameters.  Entry i,j is the score of
		# transitioning *to* i *from* j.
		self.transitions = nn.Parameter(
				torch.randn(self.tagset_size, self.tagset_size))

		# These two statements enforce the constraint that we never transfer
		# to the start tag and we never transfer from the stop tag
		self.transitions.data[self.tag_to_ix[START_TAG], :] = -10000
		self.transitions.data[:, self.tag_to_ix[STOP_TAG]] = -10000

		self.hidden = self.init_hidden()

	def init_hidden(self):
		return (torch.randn(2, 1, self.hidden_dim // 2),
			torch.randn(2, 1, self.hidden_dim // 2))

	def _forward_alg(self, feats):
		# Do the forward algorithm to compute the partition function
		init_alphas = torch.full((1, self.tagset_size), -10000.)
		# START_TAG has all of the score.
		init_alphas[0][self.tag_to_ix[START_TAG]] = 0.

		# Wrap in a variable so that we will get automatic backprop
		forward_var = init_alphas

		# Iterate through the sentence
		for feat in feats:
			alphas_t = []  # The forward tensors at this timestep
			for next_tag in range(self.tagset_size):
				# broadcast the emission score: it is the same regardless of
				# the previous tag
				emit_score = feat[next_tag].view(
						1, -1).expand(1, self.tagset_size)
				# the ith entry of trans_score is the score of transitioning to
				# next_tag from i
				trans_score = self.transitions[next_tag].view(1, -1)
				# The ith entry of next_tag_var is the value for the
				# edge (i -> next_tag) before we do log-sum-exp
				next_tag_var = forward_var + trans_score + emit_score
				# The forward variable for this tag is log-sum-exp of all the
				# scores.
				alphas_t.append(log_sum_exp(next_tag_var).view(1))
			forward_var = torch.cat(alphas_t).view(1, -1)
		terminal_var = forward_var + self.transitions[self.tag_to_ix[STOP_TAG]]
		alpha = log_sum_exp(terminal_var)
		return alpha

	def _get_lstm_features(self, sentence):
		self.hidden = self.init_hidden()
		embeds = self.word_embeds(sentence).view(len(sentence), 1, -1)
		lstm_out, self.hidden = self.lstm(embeds, self.hidden)
		lstm_out = lstm_out.view(len(sentence), self.hidden_dim)
		lstm_feats = self.hidden2tag(lstm_out)
		return lstm_feats

	def _score_sentence(self, feats, tags):
		# Gives the score of a provided tag sequence
		score = torch.zeros(1)
		tags = torch.cat([torch.tensor([self.tag_to_ix[START_TAG]], dtype=torch.long), tags])
		for i, feat in enumerate(feats):
			score = score + \
				self.transitions[tags[i + 1], tags[i]] + feat[tags[i + 1]]
		score = score + self.transitions[self.tag_to_ix[STOP_TAG], tags[-1]]
		return score

	def _viterbi_decode(self, feats):
		backpointers = []

		# Initialize the viterbi variables in log space
		init_vvars = torch.full((1, self.tagset_size), -10000.)
		init_vvars[0][self.tag_to_ix[START_TAG]] = 0

		# forward_var at step i holds the viterbi variables for step i-1
		forward_var = init_vvars
		for feat in feats:
			bptrs_t = []  # holds the backpointers for this step
			viterbivars_t = []  # holds the viterbi variables for this step

			for next_tag in range(self.tagset_size):
				# next_tag_var[i] holds the viterbi variable for tag i at the
				# previous step, plus the score of transitioning
				# from tag i to next_tag.
				# We don't include the emission scores here because the max
				# does not depend on them (we add them in below)
				next_tag_var = forward_var + self.transitions[next_tag]
				best_tag_id = argmax(next_tag_var)
				bptrs_t.append(best_tag_id)
				viterbivars_t.append(next_tag_var[0][best_tag_id].view(1))
			# Now add in the emission scores, and assign forward_var to the set
			# of viterbi variables we just computed
			forward_var = (torch.cat(viterbivars_t) + feat).view(1, -1)
			backpointers.append(bptrs_t)

		# Transition to STOP_TAG
		terminal_var = forward_var + self.transitions[self.tag_to_ix[STOP_TAG]]
		best_tag_id = argmax(terminal_var)
		path_score = terminal_var[0][best_tag_id]

		# Follow the back pointers to decode the best path.
		best_path = [best_tag_id]
		for bptrs_t in reversed(backpointers):
			best_tag_id = bptrs_t[best_tag_id]
			best_path.append(best_tag_id)
		# Pop off the start tag (we dont want to return that to the caller)
		start = best_path.pop()
		assert start == self.tag_to_ix[START_TAG]  # Sanity check
		best_path.reverse()
		return path_score, best_path

	def neg_log_likelihood(self, sentence, tags):
		sentence = seq_to_ix(sentence, self.word_to_ix)
		tags = torch.tensor([self.tag_to_ix[t] for t in tags.split()], dtype=torch.long)

		feats = self._get_lstm_features(sentence)
		forward_score = self._forward_alg(feats)
		gold_score = self._score_sentence(feats, tags)
		return forward_score - gold_score

	def forward(self, sentence):  # dont confuse this with _forward_alg above.
		# Get the emission scores from the BiLSTM
		sentence = seq_to_ix(sentence, self.word_to_ix, train=False)
		print(sentence)
		lstm_feats = self._get_lstm_features(sentence)

		# Find the best path, given the features.
		score, tag_seq = self._viterbi_decode(lstm_feats)
		return score, tag_seq # ix_to_seq(tag_seq, self.ix_to_tag)



class NER(Learning):
	def __init__(self, tag_to_ix={}):
		super(NER, self).__init__()
		self.tag_to_ix = tag_to_ix
		self.EMBEDDING_DIM = 5
		self.HIDDEN_DIM = 4
		self.num_epochs = 20
		self.intentsPath = "data/intents.json"
		self.input_name = "pattern"
		self.output_name = "map"
		self._loadIntents()
		self.tag_to_ix = { START_TAG: 0, STOP_TAG: 1, "E": 2, "Q": 3 }
		self.model = BiLSTM_CRF(300, self.tag_to_ix, self.EMBEDDING_DIM, self.HIDDEN_DIM)
	

	def train(self):
		print("starting training")
		training_data = self.prepareData(data=self.intents)
		print("training_data (length)", len(training_data))
		optimizer = optim.SGD(self.model.parameters(), lr=0.01, weight_decay=1e-4)
		for epoch in range(self.num_epochs):
			for (sentence, tags) in training_data:
				self.model.zero_grad()
				loss = self.model.neg_log_likelihood(sentence, tags)
				loss.backward()
				optimizer.step()

			if (epoch + 1) % 2 == 0:
				epochLoss = "%.4f" % loss.item()
				print(f'Epoch [{epoch+1}/{self.num_epochs}], Loss: {epochLoss}')


	def predict(self, sentence):
		tokenized_sentence = tokenords(sentence)
		# sentence_words = [stem(word) for word in tokenized_sentence]
		with torch.no_grad():
			output = self.model(tokenized_sentence)[1]
			return output