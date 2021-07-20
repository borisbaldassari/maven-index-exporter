
# Maven Index Exporter

This Docker image reads a Maven Indexer index and extract information about
the indexed documents as a convenient text file.

## Sequence

The export is

## Output

The Docker image uses clue to export the lucene indexes to text format. See
the clue documentation for the export option.

As an example a list of fields can be found in

## How to build

The build downloads binaries for both tools (maven-indexer-cli and clue).

```
docker build . -t bbaldassari/maven-index-exporter --no-cache
```

## How to use

The Docker image uses volumes to exchanges files. Prepare a directory with
enough space disk (see warning below) and pass it to docker:

```
docker run -v /work:/work bbaldassari/maven-index-exporter
```

### Size of generated files

Beware that maven indexes are compressed and text export can become huge.
When executed on the maven central indexes (5.2 GB), the process generates
49GB of text data on disk:

```
boris@castalia:maven$ du -sh /work/*
49G	/work/export
5,2G	/work/indexes
1,2G	/work/nexus-maven-repository-index.gz
```
