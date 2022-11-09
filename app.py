import chat
import gradio as gr

def interaction(text):
  return text

demo = gr.Interface(fn=interaction, inputs="text", outputs=["text"])

# demo.launch()
