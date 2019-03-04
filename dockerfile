FROM python:3

ADD chat.py /

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY help.py

COPY slack.py

CMD [ "python", "./chat.py" ]