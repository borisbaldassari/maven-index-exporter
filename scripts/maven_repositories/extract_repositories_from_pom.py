# Copyright (C) 2021 The Software Heritage developers
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information
# SPDX-License-Identifier: GPL-3.0-or-later

# This script reads a pom file and looks for the following XML attributes:
#   //repositories/repository
#   //pluginRepository/
#   //distributionManagement/snapshotRepository
#   //distributionManagement/repository
# It then prints them on a single line with their type, id and url.

import sys
import pprint
import xml.etree.ElementTree as ET

if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "file_pom.xml")
    exit()

file_in = sys.argv[1]
nsmap = {'m': 'http://maven.apache.org/POM/4.0.0'}

# Parse pom
print("# Parsing file", file_in)
root = ET.parse(file_in).getroot()

for repo in root.findall('.//m:repositories/m:repository/', nsmap):
    id  = repo.find('./m:id', nsmap)
    if id:
        myid = id.text
        url  = repo.find('./m:url', nsmap)
        if url:
            myurl = url.text
            print(f"repo,{myid},{myurl}")

for repo in root.findall('.//m:pluginRepository', nsmap):
    id  = repo.find('./m:id', nsmap).text
    url  = repo.find('./m:url', nsmap).text
    print(f"plugin,{id},{url}")

for repo in root.findall('.//m:distributionManagement/m:snapshotRepository', nsmap):
    id  = repo.find('./m:id', nsmap).text
    url  = repo.find('./m:url', nsmap).text
    print(f"distrib_snapshot,{id},{url}")
    
for repo in root.findall('.//m:distributionManagement/m:repository', nsmap):
    id  = repo.find('./m:id', nsmap).text
    url  = repo.find('./m:url', nsmap).text
    print(f"distrib_repo,{id},{url}")

