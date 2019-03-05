FROM python:3
ADD . /Fack_Chat
WORKDIR /Fack_Chat
COPY requirements.txt ./
RUN pip install -r requirements.txt
CMD [ "python", "./chat.py" ]