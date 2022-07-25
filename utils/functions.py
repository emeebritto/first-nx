import hashlib


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
