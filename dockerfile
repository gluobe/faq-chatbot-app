FROM alpine:latest

RUN apk add --no-cache python3-dev && pip3 install --upgrade pip

WORKDIR /fct

COPY . /fct

RUN pip3 --no-cache-dir install -r requirements.txt
ENV SLACK_SECRET c6746653654493e16297fd7c04913564
ENV SLACK_ACCES_TOKEN xoxb-555682767666-559725976260-WcyqCql08gOY6YjjVEwkY0DB

EXPOSE 3000

ENTRYPOINT ["python3"]
CMD ["faq_app/chat.py"]