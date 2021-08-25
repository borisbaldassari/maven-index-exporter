# Copyright (C) 2021 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import docker
import requests
import re
import glob
import sys
import datetime
from os import getcwd, chdir
from os.path import getsize, isdir, isfile, isabs, join
from pathlib import Path
from urllib.parse import urljoin
from shutil import copy2


# Check paramaters
if len(sys.argv) != 4:
    print("Usage:", sys.argv[0], "url work_dir publish_dir")
    print("  - url is the base url of the maven repository instance.")
    print("      Example: https://repo.maven.apache.org/maven2/")
    print("  - work_dir must be an absolute path to the temp directory.")
    print("      Example: /tmp/maven-index-exporter/")
    print("  - publish_dir must be an absolute path to the final directory.")
    print("      Example: /var/www/html/maven_index_exporter/")
    exit()
    
base_url = sys.argv[1]
work_dir = sys.argv[2]
publish_dir = sys.argv[3]

def _docker_run(docker_image: str):
    """ Start the container for the maven index export, using the image
    'bbaldassari/maven-index-exporter'. If needed the image is pulled from
    docker hub. If it already exists, simply use the local one.
    """
    # Initialise the docker client.
    client = docker.from_env()

    myimage = None
    for image in client.images.list(name=docker_image):
        myimage = image
        break
    
    if myimage is None:
        print(f"Docker: Could not find {docker_image}. Pulling it.")
        myimage = client.images.pull(repository=docker_image)
    else:
        print("Docker: Found image {myimage} locally, ID is {myimage.attrs['Id']}.")
        
    ret = client.containers.run(
        myimage,
        tty=True,
        command=["sh", "/opt/extract_indexes.sh", "/work/"],
        volumes={work_dir: {"bind": "/work", "mode": "rw"}},
    )

    print(f"Docker log:\n{ret.decode()}")

def _download_indexes(instance_url: str):
    """ Download all required indexes from the .index/ directory
    of the specified instance.
    """
    print(f"# Downloading all required indexes")

    index_url = urljoin(instance_url, ".index/")

    properties_name = "nexus-maven-repository-index.properties"
    properties_file = join(work_dir, properties_name)
    properties_url = urljoin(index_url, properties_name)

    # Retrieve properties file.
    print(f"  - Downloading {properties_file}.")
    content = requests.get(properties_url).content.decode()
    open(properties_file, "w").write(content)

    diff_re = re.compile("^nexus.index.incremental-[0-9]+=([0-9]+)")
    for line in content.split("\n"):
        diff_group = diff_re.match(line)
        if diff_group is not None:
            ind_name = "nexus-maven-repository-index." + diff_group.group(1) + ".gz"
            ind_path = join(work_dir, ind_name)
            ind_url = urljoin(index_url, ind_name)
            if isfile(ind_path):
                print(f"  - File {ind_path} exists, skipping download.")
            else:
                print(
                    (
                        f"  - File {ind_path} doesn't exist. "
                        f"Downloading file from {ind_url}."
                    )
                )
                # Retrieve incremental gz file
                contentb = requests.get(ind_url).content
                open(ind_path, "wb").write(contentb)

    # Retrieve main index file.
    ind_path = join(work_dir, "nexus-maven-repository-index.gz")
    ind_url = urljoin(index_url, "nexus-maven-repository-index.gz")
    if isfile(ind_path):
        print(f"  - File {ind_path} exists, skipping download.")
    else:
        print(f"  - File {ind_path} doesn't exist. Downloading file from {ind_url}")
        contentb = requests.get(ind_url).content
        open(ind_path, "wb").write(contentb)



###############################################
# Start execution
###############################################

now = datetime.datetime.now()
print(f"Script: {sys.argv[0]}")
print("Timestamp:", now.strftime("%Y-%m-%d %H:%M:%S"))
print(f"* URL: {base_url}")
print(f"* Work_Dir: {work_dir}")

# Check work_dir and create it if needed.
if isdir(work_dir):
    print("Work_Dir {work_dir} exists. Reusing it.")
else:
    try:
        print("Cannot find work_dir {work_dir}. Creating it.")
        Path(work_dir).mkdir(parents=True, exist_ok=True)
    except OSError as error:
        print(f"Could not create work_dir {work_dir}: {error}.")
        
assert isdir(work_dir)
assert isabs(work_dir)

# Grab all the indexes
# Only fetch the new ones, existing files won't be re-downloaded.
_download_indexes(base_url)

# Run Docker on the downloaded indexes.
_docker_run("bbaldassari/maven-index-exporter")

print("Export directory has the following files:")
owd = getcwd()
chdir(join(work_dir, "export"))
myfile = None
re_fld = re.compile(r".*\.fld$")
for file in glob.glob("*.*"):
    print("  -", file, "size", getsize(file))
    if (re_fld.match(file)):
        myfile = file

# Now copy the results to the desired location: publish_dir.
if isfile(myfile):
    print("Found fld file:", myfile)
else:
    print("Cannot find .fld file. Exiting")
    exit(4)

print(f"Copying files to {publish_dir}..")
try:
    copy2(myfile, publish_dir)
except OSError as error:
        print(f"Could not publish results in {publish_dir}: {error}.")

now = datetime.datetime.now()
print(f"Script finished on", now.strftime("%Y-%m-%d %H:%M:%S"))
        
