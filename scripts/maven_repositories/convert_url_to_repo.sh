# Copyright (C) 2021 The Software Heritage developers
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information
# SPDX-License-Identifier: GPL-3.0-or-later

download_if_not_there() {
    index=$1
    localfile=$(basename $index)
    echo "- checking $localfile."
    if [[ -e $localfile ]]; then
	echo "- $localfile already exists locally."
    else	
	echo "- $localfile cannot be found locally. Downloading."
	wget $index
    fi
}

for u in `cat urls_missing.txt`; do
    dir=$(echo $u | tr '/' '_')
    dir_full="/data/maven_repositories/$dir"
    mkdir -p $dir_full
    echo "Working in $dir"
    cd $dir_full
    rm nexus-maven-repository-index.properties
    wget $u/.index/nexus-maven-repository-index.properties
    download_if_not_there $u/.index/nexus-maven-repository-index.gz
    for i in `grep 'index.incremental' nexus-maven-repository-index.properties | cut -d- -f2 | cut -d= -f1`; do
	download_if_not_there $u/.index/nexus-maven-repository-index.$i.gz
    done
    cd -
done

