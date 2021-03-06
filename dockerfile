FROM alpine:latest

RUN apk add --no-cache python3-dev && pip3 install --upgrade pip
RUN pip3 install --upgrade pip
WORKDIR /fct

COPY . /fct

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 3000

ENTRYPOINT ["python3"]
CMD ["faq_app/chat.py"]