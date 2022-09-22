FROM python:3.8
WORKDIR .
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y python3-opencv libsm6 libxext6 libgl1
RUN pip install -r requirements.txt
COPY . .
CMD [ "python", "chat.py"]