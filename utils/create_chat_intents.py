import re
import json
import uuid
from random import randint

contexts = []
thread_contexts = []
intents = []

# print(dir(str))
with open('data/dialog.md', 'r') as dialog:
  dialog_lines = dialog.readlines()
  for index in range(0, len(dialog_lines) - 1, 2):
    dialog_line = dialog_lines[index];
    dialog_response_line = dialog_lines[index + 1]; 

    tag = str(uuid.uuid4())
    thread_v1 = dialog_line.startswith('    ')
    thread_v2 = dialog_line.startswith('        ')
    atThread = thread_v2 or thread_v1
    if (not atThread): thread_contexts = []
    context = None

    if atThread and not len(thread_contexts):
      context = [contexts[-1]]
    elif atThread and len(thread_contexts):
      context = [thread_contexts[-1]]

    intent = {
      "tag": tag,
      "patterns": dialog_line.strip().split(' || '),
      "context": context,
      "responses": dialog_response_line.strip().split(' || ')
    }

    print(intent)

    if (atThread):
      contexts.append(tag)
    else:
      thread_contexts.append(tag)
    intents.append(intent)

  intents_file = open("data/intents.json", "w")
  json.dump({ "intents": intents }, intents_file, indent=2)
  intents_file.close()

    #print(list([match.groups()[0], match.groups()[1].strip()] for match in matches if match.groups()[0]))
    # if (len(dialog_line.split(' : ')) < 2): continue
    # raw_str_author, raw_str_msg = dialog_line.split(' : ');
    # print(raw_str_author.replace('*', ''), raw_str_msg.replace('', ''), sep=" | ")