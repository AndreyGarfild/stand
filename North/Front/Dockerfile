FROM python:alpine

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 5010

CMD ["python3","app.py"]