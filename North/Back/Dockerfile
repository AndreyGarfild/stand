FROM python:alpine

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 5011

CMD ["python3","app.py"]