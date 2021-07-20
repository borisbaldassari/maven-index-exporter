
FROM adoptopenjdk/openjdk11:alpine-jre

COPY clue-*.jar /opt/
COPY indexer-cli-*.jar /opt/
COPY extract_indexes.sh /opt/

WORKDIR /work/

RUN ls /opt/
RUN ls -R /work/

CMD ["sh", "/opt/extract_indexes.sh", "/work/nexus-maven-repository-index.gz"]

