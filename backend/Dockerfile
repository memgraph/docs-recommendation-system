FROM python:3.8

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT [ "python" ]

CMD ["app.py" ]