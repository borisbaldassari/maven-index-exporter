
# Maven Index Exporter

This Docker image reads a Maven Indexer index and extract information about the indexed documents as a convenient text file.

It takes as input the full set of Maven indexes files, as can be seen in the central maven repository, and uses two Java tools ([maven-indexer-cli](https://maven.apache.org/maven-indexer/) and [clue](https://github.com/javasoze/clue)) to extract the indexes (in `indexes/`) and export them in the `export/` directory.

* You can read more about the sequence of actions in the `docs/` directory, including:
* [more information about the process](docs/README.md). 
* [instructions to run the exporter](docs/run_maven_index_exporter.md). 
* [instructions to build and test](docs/build_and_test.md) the Docker image. 

An official Docker image is provided for quick tests on [DockerHub](https://hub.docker.com/r/bbaldassari/maven-index-exporter).

## List of maven repositories

We also provide a curated list of maven repositories that can be used with the Docker images, i.e. they use the Maven indexer, make their indexes publicly available, and use the same version as the exporter. 

See [docs/maven_repositories.md](docs/maven_repositories.md).

