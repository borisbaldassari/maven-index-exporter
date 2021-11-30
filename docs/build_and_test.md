
# Build and test Maven index exporter


## How to test (the quick way)

There is a bash script called `test_docker_image.sh` in the `scripts/` directory,
simply execute it. Tests cover the creation of the docker image, its execution, and the
resulting output.

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
