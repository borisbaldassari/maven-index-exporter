
# Maven Index Exporter

This Docker image reads a Maven Indexer index and extract information about the indexed documents as a convenient text file.

It takes as input the full set of Maven indexes files, as can be seen in the central maven repository, and uses two Java tools ([maven-indexer-cli](https://maven.apache.org/maven-indexer/) and [clue](https://github.com/javasoze/clue)) to extract the indexes (in `indexes/`) and export them in the `export/` directory.

* You can read more about the sequence of actions in the `docs/` directory, including:
* [more information about the process](docs/README.md). 
* [instructions to run the exporter](docs/run_maven-index-exporter.md). 
* [instructions to build and test](docs/build_and_test.md) the Docker image. 

An official Docker image is provided for quick tests on [DockerHub](https://hub.docker.com/r/bbaldassari/maven-index-exporter).


