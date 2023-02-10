from threading import Thread
from re import sub as re_sub
from uuid import uuid4
from time import sleep
import subprocess
import requests
import hashlib
import time
import sys
import os


def syncmethod(func):
  def function(*args, **kwargs):
    th = Thread(target=func, args=args, kwargs=kwargs)
    th.start()
  return function


@syncmethod
def execute_command(command):
  print(f"executing subprocess: {command}")
  process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  sys.stdout.flush()
  while True:
    stdout = process.stdout.readlines()
    stderr = process.stderr.readlines()
    if stdout:
      for line in stdout:
        print("Out:", line)
    if stderr:
      for line in stderr:
        print("Error:", line)
    if process.poll() == 0:
      print("poll", process.poll())
      break
    time.sleep(1)


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
    return re_sub(match, newValue or "", " ".join(target)).split()
  else:
    return re_sub(match, newValue or "", target)


def read_as_binary(filepath, fileFormat=None, case=None):
  if case == False: return filepath
  newfilepath = ""
  if fileFormat:
    newfilepath = re_sub(r'\.\w*$', f".{fileFormat}", filepath)
    os.rename(filepath, newfilepath)
  data = open(newfilepath or filepath, "rb")
  os.remove(newfilepath or filepath)
  return data


def create_filePath(data, fileFormat="", folder=None, fileName=None):
  filename = f"{fileName or str(uuid4())}.{fileFormat}"
  filePath = f"{folder}/{filename}" if folder else filename
  with open(filePath, 'wb') as file: file.write(data)
  return filePath


def raiseError(msg, case):
  case = not case # reverse
  assert case, msg


@syncmethod
def interval(fc, time):
  while True:
    sleep(time)
    fc()


@syncmethod
def wake_up():
  url = "https://nexa-shi.herokuapp.com/test"
  try:
    requests.get(url)
  except Exception as e:
    print(f"wakeUp failed (url: {url})")


def keep_awake():
  print("keep_awake was activated.")
  interval(wake_up, 4 * 60)
