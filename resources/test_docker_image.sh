#!/bin/bash

# Copyright (C) 2021 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

DOCKER_IMAGE="maven-index-exporter"
LOG=test_docker_image.log

# This script builds the docker image for maven-index-exporter, and 
# executes it on a known set of indexes and checks the results in order
# to test the full tool chain.

echo "Script started on `date +%Y%m%d_%H%M%S`."
echo "* Writing log to $LOG."

# Find location of script directory
OLD_DIR=$(pwd)
REPO_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd $OLD_DIR

WORK_DIR=$REPO_DIR/repository_test
EXPORT_DIR=$WORK_DIR/export

# First clean up and remove any docker image with our own name
docker rmi $DOCKER_IMAGE >>$LOG 2>&1
RET=$?
if [[ $RET -eq 0 ]]; then
    echo "* Docker image [$DOCKER_IMAGE] deleted."
elif [[ $RET -eq 1 ]]; then
    echo "* Docker image [$DOCKER_IMAGE] doesn't exist."
else
    echo "Error when deleting docker image [$DOCKER_IMAGE]."
fi


# Build the image and tag it as $DOCKER_IMAGE
cd $REPO_DIR/docker
echo "* Building docker image."
docker build . -t $DOCKER_IMAGE --no-cache >>$LOG
RET=$?
if [[ $RET -eq 0 ]]; then
    echo "PASS: docker build returned 0."
else 
    echo "FAIL: docker build returned $RET."
    exit 20
fi

# Assert docker image has been created.
COUNT=$(docker images | grep -E "^$DOCKER_IMAGE\s" | wc -l)
if [[ $COUNT -eq 0 ]]; then 
    echo "FAIL: Docker image cannot be listed."
    exit 10
else 
  echo "PASS: Docker image is listed."
fi

# Run the image on the maven indexes.
docker run -v $WORK_DIR:/work $DOCKER_IMAGE >>$LOG 2>&1

# Assert exported text files are there, with the correct content.
EXPORT_FILE=$(ls $EXPORT_DIR/*.fld)
if [[ -e $EXPORT_FILE ]]; then 
    echo "PASS: file [$EXPORT_FILE] has been created."
else 
    echo "FAIL: file [$EXPORT_FILE] has NOT been created."
    exit 20
fi

DOCS=$(grep -E "^doc" $EXPORT_FILE | wc -l)
if [[ $DOCS -eq 7 ]]; then 
    echo "PASS: file [$EXPORT_FILE] has 7 docs."
else 
    echo "FAIL: file [$EXPORT_FILE] has $DOCS docs, should be 7."
    exit 20
fi

FIELDS=$(grep -E "^  field" $EXPORT_FILE | wc -l)
if [[ $FIELDS -eq 26 ]]; then 
    echo "PASS: file [$EXPORT_FILE] has 26 fields."
else 
    echo "FAIL: file [$EXPORT_FILE] has $FIELDS fields, should be 26."
    exit 20
fi

FIELDS=$(grep "value al.aldi|sprova4j|0.1.0|sources|jar" $EXPORT_FILE | wc -l)
if [[ $FIELDS -eq 1 ]]; then 
    echo "PASS: file [$EXPORT_FILE] has sprova4j-0.1.0-sources.jar."
else 
    echo "FAIL: file [$EXPORT_FILE] has NOT sprova4j-0.1.0-sources.jar."
    exit 20
fi

FIELDS=$(grep "value al.aldi|sprova4j|0.1.0|NA|pom" $EXPORT_FILE | wc -l)
if [[ $FIELDS -eq 1 ]]; then 
    echo "PASS: file [$EXPORT_FILE] has sprova4j-0.1.0.pom."
else 
    echo "FAIL: file [$EXPORT_FILE] has NOT sprova4j-0.1.0.pom."
    exit 20
fi

FIELDS=$(grep "value al.aldi|sprova4j|0.1.1|sources|jar" $EXPORT_FILE | wc -l)
if [[ $FIELDS -eq 1 ]]; then 
    echo "PASS: file [$EXPORT_FILE] has sprova4j-0.1.1-sources.jar."
else 
    echo "FAIL: file [$EXPORT_FILE] has NOT sprova4j-0.1.1-sources.jar."
    exit 20
fi

FIELDS=$(grep "value al.aldi|sprova4j|0.1.1|NA|pom" $EXPORT_FILE | wc -l)
if [[ $FIELDS -eq 1 ]]; then 
    echo "PASS: file [$EXPORT_FILE] has sprova4j-0.1.1.pom."
else 
    echo "FAIL: file [$EXPORT_FILE] has NOT sprova4j-0.1.1.pom."
    exit 20
fi

# Cleanup
rm -rf $EXPORT_DIR
cd $OLD_DIR
