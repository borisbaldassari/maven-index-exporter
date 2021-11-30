
# Documentation 


## Sequence

The index files can be dowloaded from any maven repository that uses
maven-indexer, like maven central:

    https://repo1.maven.org/maven2/.index/

Copy all files (i.e. the main index, the updates and properties file) into
the volume directory (`$WORKDIR`). It will be mounted as `/work/` in the
docker image.

The export is then achieved in two steps:

* Unpack the Lucene indexes from the Maven Indexer indexes using
  `maven-indexer-cli`. The command used is:

```
$ java --illegal-access=permit -jar $INDEXER_JAR \
       --unpack $FILE_IN \
       --destination $WORKDIR/indexes/ \
       --type full
```

This generates a set of binary lucene files as shown below:

```
$ ls -lh $WORKDIR/indexes/
total 5,2G
-rw-r--r-- 1 root root 500M juil.  7 22:06 _4m.fdt
-rw-r--r-- 1 root root 339K juil.  7 22:06 _4m.fdx
-rw-r--r-- 1 root root 2,2K juil.  7 22:07 _4m.fnm
-rw-r--r-- 1 root root 166M juil.  7 22:07 _4m_Lucene50_0.doc
-rw-r--r-- 1 root root 147M juil.  7 22:07 _4m_Lucene50_0.pos
[SNIP]
-rw-r--r-- 1 root root  363 juil.  7 22:06 _e0.si
-rw-r--r-- 1 root root 1,7K juil.  7 22:07 segments_2
-rw-r--r-- 1 root root    8 juil.  7 21:54 timestamp
```

* Export the Lucene documents from the Lucene indexes using `clue`. This
  generates a set of text files as shown below:

```
$ java --illegal-access=permit -jar $JAR_CLUE $WORKDIR/indexes/ \
       export $WORKDIR/export/ text
```

This generates a bunch of text files relating to the Lucene indexes, made
available in `$WORKDIR/export/`. For our purpose we only keep the `*.fld`
file that includes the indexed documents.

## Output

The clue command is documented on [its github page](https://github.com/javasoze/clue).
The indexed Lucene documents are located in the `*.fld` file.

A description of the fields used by maven-indexer can be found in the project's
API docs: https://maven.apache.org/maven-indexer-archives/maven-indexer-6.0.0/indexer-core/apidocs/org/apache/maven/index/ArtifactInfo.html

## How to build

The build downloads binaries for both tools (maven-indexer-cli and clue), so make sure there is an internet connection.
Go to the `docker/` dorectory and issue the folowing command:

```
$ docker build . -t bbaldassari/maven-index-exporter --no-cache
```

An up-to-date docker image is also available on docker hub at
[bbaldassari/maven-index-exporter](https://hub.docker.com/r/bbaldassari/maven-index-exporter).

```
$ docker pull bbaldassari/maven-index-exporter
```
