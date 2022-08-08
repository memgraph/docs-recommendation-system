FROM memgraph/memgraph-mage:1.3.1

USER root

# Copy the local query modules
COPY transformations/ /transformations
COPY procedures/ /procedures

USER memgraph