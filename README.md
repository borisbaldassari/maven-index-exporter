
# Maven Index Exporter

This Docker image reads a Maven Indexer index and extract information about
the indexed documents as a convenient text file.

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
API docs:
https://maven.apache.org/maven-indexer-archives/maven-indexer-6.0.0/indexer-core/apidocs/org/apache/maven/index/ArtifactInfo.html

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

## How to use

The Docker image uses volumes to exchanges files. Prepare a directory with
enough space disk (see warning below) and pass it to docker:

```
$ docker run -v /local/work/dir:/work bbaldassari/maven-index-exporter
```

Please note that the local work dir MUST be an absolute path, as docker won't
mount relative paths as volumes.

For our purpose only the fld file is kept, so if you need other export files
you should simply edit the `extract_indexes.sh` script and comment the lines
that do the cleaning.

### Running as cron

The `run_full_export.py` script located in `resources` provides an easy way to run the
export as a cron batch job, and copy the resulting text export to a specific location.

Simply use and adapt the crontab command as follows:

```
cd /home/boris/resources/ && /home/boris/resources/myvenv/bin/python /home/boris/resources/run_full_export.py https://repo.maven.apache.org/maven2/ /tmp/maven-index\
-exporter/ /var/www/html/maven_index_exporter/ 2>&1 > /home/boris/run_maven_exporter_$(date +"%Y%m%d-%H%M%S").log

```

The script takes three mandatory arguments:

```
Usage: run_full_export.py url work_dir publish_dir
  - url is the base url of the maven repository instance.
      Example: https://repo.maven.apache.org/maven2/
  - work_dir must be an absolute path to the temp directory.
      Example: /tmp/maven-index-exporter/
  - publish_dir must be an absolute path to the final directory.
      Example: /var/www/html/
```

It is recommended to setup a virtual environment to run the script.

```
$ python3 -m venv myvenv
$ source venv/bin/activate
```

Python modules to be installed are provided in the `requirements.txt` file.

### size of generated files

Beware that maven indexes are compressed and text export can become huge.
When executed on the maven central indexes (1.2 GB), the process generates
5.2 GB of intermediate files and 49 GB of final text data on disk:

```
$ du -sh /work/*
49G	/work/export
5,2G	/work/indexes
1,2G	/work/nexus-maven-repository-index.gz
```

## How to test (the quick way)

There is a bash script called `test_docker_image.sh` in the `resources/` directory,
simply execute it. Tests cover the creation of the docker image, and the results after
execution.

```
$ bash test_docker_image.sh
Script started on 20210911_181912.
* Writing log to test_docker_image.log.
* Docker image [maven-index-exporter] doesn't exist.
* Building docker image.
PASS: docker build returned 0.
PASS: Docker image is listed.
PASS: file [/home/boris/Projects/gh_maven-index-exporter/repository_test/export/_1.fld] has been created.
PASS: file [/home/boris/Projects/gh_maven-index-exporter/repository_test/export/_1.fld] has 7 docs.
PASS: file [/home/boris/Projects/gh_maven-index-exporter/repository_test/export/_1.fld] has 26 fields.
PASS: file [/home/boris/Projects/gh_maven-index-exporter/repository_test/export/_1.fld] has sprova4j-0.1.0-sources.jar.
PASS: file [/home/boris/Projects/gh_maven-index-exporter/repository_test/export/_1.fld] has sprova4j-0.1.0.pom.
PASS: file [/home/boris/Projects/gh_maven-index-exporter/repository_test/export/_1.fld] has sprova4j-0.1.1-sources.jar.
PASS: file [/home/boris/Projects/gh_maven-index-exporter/repository_test/export/_1.fld] has sprova4j-0.1.1.pom.
$
```

## How to test (the long road)

This repository has a simple, almost-empty maven-indexer index that can be used to test the docker build. To use it, make sure that the directory `repository_test/` is present and run this command:

```
$ docker run -v $(pwd)/repository_test:/work bbaldassari/maven-index-exporter
```

The exported files will be stored in `repository_test/export/`, and output should look like this:

```
$ docker run -v $(pwd)/repository_test:/work bbaldassari/maven-index-exporter
Docker Script started on 2021-08-27 06:32:22.
# Checks..
* Content of /opt:
total 32156
-rw-------    1 root     root      18000742 Jan  8  2018 clue-6.2.0-1.0.0.jar
-rw-r--r--    1 root     root          2574 Aug 25 18:28 extract_indexes.sh
-rw-------    1 root     root      14914610 Nov 28  2017 indexer-cli-6.0.0.jar
drwxr-xr-x    3 root     root          4096 Jun 29 16:23 java
* Content of /work:
total 36
-rw-r--r--    1 1000     1000           254 Aug 26 09:21 nexus-maven-repository-index.1.gz
-rw-r--r--    1 1000     1000            32 Aug 26 09:21 nexus-maven-repository-index.1.gz.md5
-rw-r--r--    1 1000     1000            40 Aug 26 09:21 nexus-maven-repository-index.1.gz.sha1
-rw-r--r--    1 1000     1000           344 Aug 26 09:21 nexus-maven-repository-index.gz
-rw-r--r--    1 1000     1000            32 Aug 26 09:21 nexus-maven-repository-index.gz.md5
-rw-r--r--    1 1000     1000            40 Aug 26 09:21 nexus-maven-repository-index.gz.sha1
-rw-r--r--    1 1000     1000           193 Aug 26 09:21 nexus-maven-repository-index.properties
-rw-r--r--    1 1000     1000            32 Aug 26 09:21 nexus-maven-repository-index.properties.md5
-rw-r--r--    1 1000     1000            40 Aug 26 09:21 nexus-maven-repository-index.properties.sha1
* Will read files from [/work/nexus-maven-repository-index.gz].
*   Found file [/work/nexus-maven-repository-index.gz].
*   Found indexer [/opt/indexer-cli-6.0.0.jar].
*   Found clue [/opt/clue-6.2.0-1.0.0.jar].
* Java version:.
openjdk version "11.0.11" 2021-04-20
OpenJDK Runtime Environment AdoptOpenJDK-11.0.11+9 (build 11.0.11+9)
OpenJDK 64-Bit Server VM AdoptOpenJDK-11.0.11+9 (build 11.0.11+9, mixed mode)
#############################
Unpacking [/work/nexus-maven-repository-index.gz] to /work/indexes
SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
SLF4J: Defaulting to no-operation (NOP) logger implementation
SLF4J: See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.
Index Folder:      /work
Output Folder:     /work/indexes
Total time:   0 sec
Final memory: 41M/1004M
Unpacking finished on 2021-08-27 06:32:23.
#############################
Exporting indexes /work/indexes to /work/export
no configuration found, using default configuration
Analyzer: 		class org.apache.lucene.analysis.standard.StandardAnalyzer
Query Builder: 		class com.senseidb.clue.api.DefaultQueryBuilder
Directory Builder: 	class com.senseidb.clue.api.DefaultDirectoryBuilder
IndexReader Factory: 	class com.senseidb.clue.api.DefaultIndexReaderFactory
Term Bytesref Display: 	class com.senseidb.clue.api.StringBytesRefDisplay
Payload Bytesref Display: 	class com.senseidb.clue.api.RawBytesRefDisplay
exporting index to text
Exporting finished on 2021-08-27 06:32:23.
#############################
Cleaning useless files.
Size before cleaning:
32.0K	/work/export
28.0K	/work/indexes
4.0K	/work/nexus-maven-repository-index.1.gz
4.0K	/work/nexus-maven-repository-index.1.gz.md5
4.0K	/work/nexus-maven-repository-index.1.gz.sha1
4.0K	/work/nexus-maven-repository-index.gz
4.0K	/work/nexus-maven-repository-index.gz.md5
4.0K	/work/nexus-maven-repository-index.gz.sha1
4.0K	/work/nexus-maven-repository-index.properties
4.0K	/work/nexus-maven-repository-index.properties.md5
4.0K	/work/nexus-maven-repository-index.properties.sha1
* Removing useless exports.
  Keeping only fld text extract.
  Size after cleaning:
8.0K	/work/export
28.0K	/work/indexes
4.0K	/work/nexus-maven-repository-index.1.gz
4.0K	/work/nexus-maven-repository-index.1.gz.md5
4.0K	/work/nexus-maven-repository-index.1.gz.sha1
4.0K	/work/nexus-maven-repository-index.gz
4.0K	/work/nexus-maven-repository-index.gz.md5
4.0K	/work/nexus-maven-repository-index.gz.sha1
4.0K	/work/nexus-maven-repository-index.properties
4.0K	/work/nexus-maven-repository-index.properties.md5
4.0K	/work/nexus-maven-repository-index.properties.sha1
* Make files modifiable by the end-user.
Docker Script execution finished on 2021-08-27 06:32:23.
```

The `_1.fld` file contains the fields for each document:

```
$ head repository_test/export/_1.fld
doc 0
  field 0
    name u
    type string
    value al.aldi|sprova4j|0.1.0|sources|jar
  field 1
    name m
    type string
    value 1626111735737
  field 2
```

### Building the test repository

The test repository `repository_test` can be rebuilt from the `repository_src`
structure using [indexer-cli](https://search.maven.org/remotecontent?filepath=org/apache/maven/indexer/indexer-cli/6.0.0/indexer-cli-6.0.0.jar)
with the following commands:

```
$ cd repository_src
$ java -jar ~/Downloads/indexer-cli-6.0.0.jar -i index/ -d repository_test/ -r repo1 -s -c
SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
SLF4J: Defaulting to no-operation (NOP) logger implementation
SLF4J: See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.
Repository Folder: /home/boris/Projects/maven-index-exporter/repository_src/repo1
Index Folder:      /home/boris/Projects/maven-index-exporter/repository_src/index
Output Folder:     /home/boris/Projects/maven-index-exporter/repository_src/repository_test
Repository name:   index
Indexers: [min, jarContent]
Will create checksum files for all published files (sha1, md5).
Will create incremental chunks for changes, along with baseline file.
Scanning started
Artifacts added:   2
Artifacts deleted: 0
Total time:   1 sec
Final memory: 48M/1012M
$ java -jar ~/Downloads/indexer-cli-6.0.0.jar -i index/ -d repository_test/ -r repo2 -s -c
SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
SLF4J: Defaulting to no-operation (NOP) logger implementation
SLF4J: See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.
Repository Folder: /home/boris/Projects/maven-index-exporter/repository_src/repo2
Index Folder:      /home/boris/Projects/maven-index-exporter/repository_src/index
Output Folder:     /home/boris/Projects/maven-index-exporter/repository_src/repository_test
Repository name:   index
Indexers: [min, jarContent]
Will create checksum files for all published files (sha1, md5).
Will create incremental chunks for changes, along with baseline file.
Scanning started
Artifacts added:   2
Artifacts deleted: 0
Total time:   0 sec
Final memory: 7M/1012M
$ java -jar ~/Downloads/indexer-cli-6.0.0.jar -i index/ -d repository_test/ -r repo3 -s -c
SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
SLF4J: Defaulting to no-operation (NOP) logger implementation
SLF4J: See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.
Repository Folder: /home/boris/Projects/maven-index-exporter/repository_src/repo3
Index Folder:      /home/boris/Projects/maven-index-exporter/repository_src/index
Output Folder:     /home/boris/Projects/maven-index-exporter/repository_src/repository_test
Repository name:   index
Indexers: [min, jarContent]
Will create checksum files for all published files (sha1, md5).
Will create incremental chunks for changes, along with baseline file.
Scanning started
Artifacts added:   1
Artifacts deleted: 2
Total time:   0 sec
Final memory: 8M/1012M
$
```
