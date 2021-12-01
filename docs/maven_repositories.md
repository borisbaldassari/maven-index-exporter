

A list of remote Maven repositories using [Maven Indexer](https://maven.apache.org/maven-indexer/) for their catalogue.


# Introduction

In the Maven ecosystem, dependencies and artefacts required to develop Java projects can be automatically downloaded from remote Maven repositories using a set of unique identifiers (aka coordinates): the groupId, artefactId and version. 

Maven repositories use a standard directory structure for their hosting, which enables to easily identify and download any artefact with its (groupId, artefactid, version) coordinates. Although it is technically not *required*, Maven repositories often provide an index of all the files they host, mostly for IDEs ( e.g. Eclipse, IntelliJ IDEA, or NetBeans). These index files are usually generated with [Maven Indexer](https://maven.apache.org/maven-indexer/) and consist of gzipped Lucene indexes stored in a `.index/` directory at the root of the repository. 

The largest and most used Maven repository is of course [Maven Central](https://search.maven.org/), but there are many, many [other repositories](https://mvnrepository.com/repos/central) available around. These are set up by individuals, companies and organisations to provide their own builds or domain-specific repositories. Since it is by no means necessary to register repositories, and as far as we know, there is no exhaustive list of Maven repositories.

The resources in this directory are an attempt to identify a list of Maven repository servers, as complete as possible. We also publish a list of servers that provide public indexes that can be analysed and exported with the [Maven index exporter](https://github.com/borisbaldassari/maven-index-exporter) Docker image.

# Method

## Build a list of URLs from poms

We started from a dump of all pom files hosted on Maven Central (6.9 million files XML files at the time of collection). For each pom we looked for XML nodes that can represent Maven repositories; starting from the root of the document and using XPath expressions we specifically looked for:

* `.//m:repositories/m:repository/`
* `.//m:pluginRepository`
* `.//m:distributionManagement/m:snapshotRepository`
* `.//m:distributionManagement/m:repository`

The transformation can be reproduced with the scripts in the `scripts/` directory:

```
time bash extract_repositories_from_stock.sh list_poms.txt | tee extract.log
```

The full execution took 61 hours and produced a list of "only" 928808 lines. Each line  provides the origin of the URL in the POM, the repository id, and the URL itself. 

```
distrib_snapshot,ossrh,https://oss.sonatype.org/content/repositories/snapshots
distrib_repo,ossrh,https://oss.sonatype.org/service/local/staging/deploy/maven2/
```

## Download properties

In the resulting set, there are many duplicates, non-existent, private or invalid URLs. 

To make sure that we only list publicly available servers we tried to download the Maven index properties file from every server. This properties file is mandatory in Maven indexer; it can be found at `.index/nexus-maven-repository-index.properties` and contains the list of incremental updates to the index. 

The sequence of actions is as follows:

* Remove printed comments, sort and remove duplicate lines:

```
grep -Ev "^# " extract.log | sort -u > extract_uniq.txt
```

* Extract the list of URLs (3rd column) and filter all but http(s) links:

```
cat result_uniq.txt | cut -d, -f 3 | grep -E '^http' > list_urls.txt
```

* The output list has 7145 lines URLs to test. For each item, we try to get the file in `<url>/.index/nexus-maven-repository-index.properties`. If it yields a file, save it.

```shell
SUFFIX="/.index/nexus-maven-repository-index.properties"

for url in `cat list_urls.txt`; do
    echo "Testing URL [$url]."
    full_url="${url}${SUFFIX}"
    name=$(echo $url | cut -d/ -f 3- | tr '/' '_')
    full_name="${name}.properties"
    echo "  Writing to [$full_name]."
    wget -O servers/"$full_name" --tries=2 $full_url &
done
```

* This downloads in the `servers/` directory 3820 properties files. Most of them are empty or contain invalid information, leaving only files that contain an actual list of Maven indexer compressed files.
* Rebuild the list of URLs by removing 404s (i.e. servers that did not create a file).  Remove trailing slashes to prevent duplicates, sort and make unique:

```shell
for f in `ls ../servers/`; do
	url=$(echo ${f%.properties} | tr '_' '/');      
    grep ${url%/} list_urls_full.txt;
done | sed 's:/*$::' | sort -u > list_urls_final.txt
```

The result is a list of 339 unique URLs: to be downloaded here: 

[list_urls_final.txt](https://files.nuclino.com/files/e75205b3-354e-4794-a43a-d9f98ad08039/list_urls_final.txt)

## Checking compatibility

To ensure that these repositories can be actually parsed with the Maen index exporter, there is no better way than parsing them and generating the index and text export. For this, we first need to download all indexes from all servers:

```
bash scripts/convert_url_to_repo.sh
```

This will rely on the list of directories downloaded previously, and generate a series of subdirectories for each server, with the index files. If the index files already exist they won't be downloaded again.

The next step is to execute the docker image from [bbaldassari/maven-index-exporter](https://github.com/borisbaldassari/maven-index-exporter) to export all text indexes in `<repo>/export/`.

```shell
mkdir -p ../maven_repositories/
for i in `ls`; do 
	time docker run -v /data/work/$i:/work bbaldassari/maven-index-exporter | tee ../logs/$i.log; 
    mv $i/ ../maven_repositories/; 
done
```

This again filters out some servers that use a Maven Indexer version different from the Docker image's compatibility.


# Result

The final list contains only Maven repositories that:

* use Maven Indexer for their indexing,
* are publicly available,
* are still available as of 2021-11-20, and
* can be extracted using the Maven index exporter Docker image.

Please note that there will probably be a huge amount of artefact duplicates, as several server names can map to to the same repository, and some repositories might mirror existing content.

List of downloads:

* The curated list of maven repositories (333 servers): [list_maven_servers_with_indexes.txt](maven_repositories/list_maven_servers_with_indexes.txt)
* A list of compressed text exports for the above maven repositories (as of 2021-11-28): https://icedrive.net/1/01BQpqC6rA
  We will add more downloads as they are generated, so stay tuned.

