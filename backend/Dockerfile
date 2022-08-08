FROM python:3.8

USER root

# Install CMake for gqlalchemy
RUN apt-get update && \
  apt-get --yes install cmake && \
  rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT [ "python", "app.py" ]

#CMD ["app.py" ]