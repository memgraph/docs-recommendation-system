FROM memgraph/memgraph-mage:1.3

USER root

# Install Python
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-setuptools \
    python3-dev \
    && pip3 install -U pip


# Copy the local query modules
COPY transformations/ /transformations
COPY procedures/ /procedures

USER memgraph