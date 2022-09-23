import hashlib
import uuid
import re
import os

def some_match(list1, list2):
  for item in list1:
    if item in list2: return True
  return False


def hashl(filePath):
  BLOCK_SIZE = 65536
  file_hash = hashlib.sha256()
  with open(filePath, 'rb') as f:
    fb = f.read(BLOCK_SIZE)
    while len(fb) > 0:
      file_hash.update(fb)
      fb = f.read(BLOCK_SIZE)

  return file_hash.hexdigest()


def replace(match, newValue, target):
  if type(target) == list:
    return re.sub(match, newValue or "", " ".join(target)).split()
  else:
    return re.sub(match, newValue or "", target)


def read_as_binary(filepath, fileFormat=None):
  newfilepath = ""
  if fileFormat:
    newfilepath = re.sub(r'\.\w*$', f".{fileFormat}", filepath)
    os.rename(filepath, newfilepath)
  data = open(newfilepath or filepath, "rb")
  os.remove(newfilepath or filepath)
  return data


def create_filePath(data, fileFormat, fileName=""):
  filePath = f"{fileName or str(uuid.uuid4())}.{fileFormat}"
  with open(filePath, 'wb') as file: file.write(data)
  return filePath