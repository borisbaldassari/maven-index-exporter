# Copyright (C) 2021 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import docker
import requests
import re


# Check paramaters
if len(sys.argv) != 3:
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
        print("Docker: Could not find %s. Pulling it.", docker_image)
        myimage = client.images.pull(repository=docker_image)
    else:
        print(
            "Docker: Found image %s locally, ID is %s.",
            myimage,
            myimage.attrs["Id"],
        )

    ret = client.containers.run(
        myimage,
        tty=True,
        command=["sh", "/opt/extract_indexes.sh", "/work/"],
        volumes={work_dir: {"bind": "/work", "mode": "rw"}},
    )

    print("Docker log:\n%s", ret.decode())

def _download_indexes(instance_url: str):
    """ Download all required indexes from the .index/ directory
    of the specified instance.
    """
    index_url = urljoin(base_url, ".index/")

    properties_file = join(work_dir, "nexus-maven-repository-index.properties")
    properties_url = urljoin(index_url, "nexus-maven-repository-index.properties")

    # Retrieve properties file.
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
                print(f"File {ind_path} exists, skipping download.")
            else:
                print(
                    (
                        f"File {ind_path} doesn't exist. "
                        f"Downloading file from {ind_url}"
                    )
                )
                # Retrieve incremental gz file
                contentb = requests.get(ind_url).content
                open(ind_path, "wb").write(contentb)

    # Retrieve main index file.
    ind_path = join(work_dir, "nexus-maven-repository-index.gz")
    ind_url = urljoin(index_url, "nexus-maven-repository-index.gz")
    if isfile(ind_path):
        print(f"File {ind_path} exists, skipping download.")
    else:
        print(f"File {ind_path} doesn't exist. Downloading file from {ind_url}")
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
    print("WORKD_DIR exists. Reusing it.")
else:
    try:
        Path(work_dir).mkdir(parents=True, exist_ok=True)
    except OSError as error:
        print(f"Could not create WORK_DIR {work_dir}: {error}.")
        
assert isdir(work_dir)
assert isabs(work_dir)

_download_indexes(base_url)

_docker_run("bbaldassari/maven-index-exporter")


now = datetime.datetime.now()
print("Timestamp:", now.strftime("%Y-%m-%d %H:%M:%S"))

print("Export directory has the following files:")

owd = getcwd()
chdir(join(workdir, "export"))
myfile = None
re_fld = re.compile(r".*\.fld$")
for file in glob.glob("*.*"):
    print("  -", file, "size", sizeof(getsize(file)))
    if (re_fld.match(file)):
        myfile = file
if isfile(myfile):
    print("Found fld file:", myfile)
else:
    print("Cannot find .fld file. Exiting")
    exit(4)

shutil.copy2(myfile, publish_dir)

