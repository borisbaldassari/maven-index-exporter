
FROM adoptopenjdk/openjdk11:alpine-jre

# Download and install jars
ADD https://github.com/javasoze/clue/releases/download/release-6.2.0-1.0.0/clue-6.2.0-1.0.0.jar /opt/
ADD https://repo1.maven.org/maven2/org/apache/maven/indexer/indexer-cli/6.0.0/indexer-cli-6.0.0.jar /opt/

# Copy index extraction script
COPY extract_indexes.sh /opt/

WORKDIR /work/

RUN ls /opt/
RUN ls -R /work/

# Parse default index file (will be overriden by cli parameters)
CMD ["sh", "/opt/extract_indexes.sh", "/work/nexus-maven-repository-index.gz"]

