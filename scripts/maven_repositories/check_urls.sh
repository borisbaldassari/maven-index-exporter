# Copyright (C) 2021 The Software Heritage developers
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information
# SPDX-License-Identifier: GPL-3.0-or-later

SUFFIX="/.index/nexus-maven-repository-index.properties"

for url in `cat list_urls.txt`; do
    echo "Testing URL [$url]."
    full_url="${url}${SUFFIX}"
    name=$(echo $url | cut -d/ -f 3- | tr '/' '_')
    full_name="${name}.properties"
    echo "  Writing to [$name $full_name]."
    wget -O ../servers/"$full_name" --tries=2 $full_url &
done
