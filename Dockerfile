FROM python:3.8
WORKDIR .
COPY requirements.txt requirements.txt
RUN pip install --ignore-installed -r requirements.txt
COPY . .
CMD [ "python", "chat.py"]