FROM python:3.8

USER root

# Install CMake for gqlalchemy
RUN apt-get update && \
  apt-get --yes install cmake && \
  rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader wordnet
RUN python -m nltk.downloader omw-1.4
RUN python -m nltk.downloader punkt

COPY . /app
WORKDIR /app

ENTRYPOINT [ "python", "app.py" ]