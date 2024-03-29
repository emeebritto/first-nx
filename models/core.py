import torch
import torch.nn as nn
import torch.nn.functional as F
from utils.nltk_utils import tokenords
from torch.autograd import Variable


MAX_LENGTH = 10

use_cuda = torch.cuda.is_available()
teacher_forcing_ratio = 0.5


class Silly:
  def __init__(self):
    super(Silly, self).__init__()
    self.mind = {}


  def __call__(self, *args, **kwargs):
    uInput = args[0]
    tokens = tokenords(uInput.lower().strip())
    train = kwargs.get("train", False)

    if train:
      for idx, word in enumerate(tokens):
        try:
          for n in range(1, 8):
            self.mind[" ".join(tokens[idx:idx+n])] = tokens[idx+n]
        except Exception as e:
          break
        print(self.mind)
      return "I learned it"
    else:
      idx = 7
      while idx:
        print(idx)
        next_word = self.mind.get(" ".join(tokens[-idx:]))
        print(next_word)
        if next_word: return next_word
        idx -= 1


class NeuralNet(nn.Module):
  def __init__(self, n_vocab, hidden_size, num_classes):
    super(NeuralNet, self).__init__()
    self.nx = nn.Sequential(
      nn.Dropout(p=0.2),
      nn.Linear(n_vocab, hidden_size),
      nn.ReLU(),
      nn.Linear(hidden_size, hidden_size),
      nn.ReLU(),
      nn.Linear(hidden_size, hidden_size),
      nn.ReLU(),
      nn.Linear(hidden_size, num_classes)
    )

  def forward(self, x):
    return self.nx(x)
    # no activation and no softmax at the end


class LSTM(nn.Module):
  def __init__(self, n_vocab, hidden_size, num_classes):
    super(LSTM, self).__init__()
    self.lstm_size = 128
    self.embedding_dim = 128
    self.num_layers = 3

    self.embedding = nn.Embedding(
      num_embeddings=n_vocab,
      embedding_dim=self.embedding_dim,
    )
    self.lstm = nn.LSTM(
      input_size=self.lstm_size,
      hidden_size=self.lstm_size,
      num_layers=self.num_layers,
      dropout=0.2,
    )
    self.fc = nn.Linear(self.lstm_size, n_vocab)

  def forward(self, x, prev_state):
    embed = self.embedding(x)
    output, state = self.lstm(embed, prev_state)
    logits = self.fc(output)

    return logits, state

  def init_state(self, sequence_length):
    return (
      torch.zeros(self.num_layers, sequence_length, self.lstm_size),
      torch.zeros(self.num_layers, sequence_length, self.lstm_size)
    )



class EncoderRNN(nn.Module):
  def __init__(self, input_size, hidden_size, n_layers=1):
    super(EncoderRNN, self).__init__()
    self.n_layers = n_layers
    self.hidden_size = hidden_size

    self.embedding = nn.Embedding(input_size, hidden_size)
    self.gru = nn.GRU(hidden_size, hidden_size)

  def forward(self, inputs, hidden):
    embedded = self.embedding(inputs).view(1, 1, -1)
    output = embedded
    for i in range(self.n_layers):
        output, hidden = self.gru(output, hidden)
    return output, hidden

  def init_hidden(self):
    result = Variable(torch.zeros(1, 1, self.hidden_size))
    if use_cuda:
      return result.cuda()
    else:
      return result


class DecoderRNN(nn.Module):
  def __init__(self, hidden_size, output_size, n_layers=1):
    super(DecoderRNN, self).__init__()
    self.n_layers = n_layers
    self.hidden_size = hidden_size

    self.embedding = nn.Embedding(output_size, hidden_size)
    self.gru = nn.GRU(hidden_size, hidden_size)
    self.out = nn.Linear(hidden_size, output_size)
    self.softmax = nn.LogSoftmax()

  def forward(self, inputs, hidden):
    output = self.embedding(inputs).view(1, 1, -1)
    for i in range(self.n_layers):
      output = F.relu(output)
      output, hidden = self.gru(output, hidden)
    output = self.softmax(self.out(output[0]))
    return output, hidden

  def init_hidden(self):
    result = Variable(torch.zeros(1, 1, self.hidden_size))
    if use_cuda:
      return result.cuda()
    else:
      return result


class AttnDecoderRNN(nn.Module):
  def __init__(self, hidden_size, output_size, n_layers=1, dropout_p=0.1, max_length=MAX_LENGTH):
    super(AttnDecoderRNN, self).__init__()
    self.hidden_size = hidden_size
    self.output_size = output_size
    self.n_layers = n_layers
    self.dropout_p = dropout_p
    self.max_length = max_length

    self.embedding = nn.Embedding(self.output_size, self.hidden_size)
    self.attn = nn.Linear(self.hidden_size * 2, self.max_length)
    self.attn_combine = nn.Linear(self.hidden_size * 2, self.hidden_size)
    self.dropout = nn.Dropout(self.dropout_p)
    self.gru = nn.GRU(self.hidden_size, self.hidden_size)
    self.out = nn.Linear(self.hidden_size, self.output_size)

  def forward(self, inputs, hidden, encoder_output, encoder_outputs):
    embedded = self.embedding(inputs).view(1, 1, -1)
    embedded = self.dropout(embedded)

    attn_weights = F.softmax(
      self.attn(torch.cat((embedded[0], hidden[0]), 1))
    )
    attn_applied = torch.bmm(
      attn_weights.unsqueeze(0),
      encoder_outputs.unsqueeze(0)
    )

    output = torch.cat((embedded[0], attn_applied[0]), 1)
    output = self.attn_combine(output).unsqueeze(0)

    for i in range(self.n_layers):
      output = F.relu(output)
      output, hidden = self.gru(output, hidden)

    output = F.log_softmax(self.out(output[0]))
    return output, hidden, attn_weights

  def init_hidden(self):
    result = Variable(torch.zeros(1, 1, self.hidden_size))
    if use_cuda:
      return result.cuda()
    else:
      return result
