import chat
from api import fileManager
import gradio as gr

def interaction(search):
  if "file::" in search:
    fileId = search.split("::")[1]
    file_infor = fileManager.getFileObjById(fileId)
    return file_infor["path"] if file_infor else ""
  return None

nxapp = gr.Interface(fn=interaction, inputs="text", outputs=["file"])
nxapp.launch()