
# Run Maven index exporter


## Running the full export

The `run_full_export.py` script located in `scripts/` provides an easy way to run the
export as a cron batch job, and copy the resulting text export to a specific location.


## Running the image only

The Docker image uses volumes to exchanges files. Prepare a directory with
enough space disk (see warning below) and pass it to docker:

```
$ docker run -v /local/work/dir:/work bbaldassari/maven-index-exporter
```

Please note that the local work dir MUST be an absolute path, as docker won't
mount relative paths as volumes.

For our purpose only the fld file is kept, so if you need other export files
you should simply edit the `extract_indexes.sh` script and comment the lines
that do the cleaning. Then rebuild the Docker image and run it.


## Running as cron

The `run_full_export.py` script located in `scripts/` provides an easy way to run the
export as a cron batch job, and copy the resulting text export to a specific location.

Simply use and adapt the crontab command as follows:

```
cd /home/boris/maven-index-exporter/scripts/ && /home/boris/maven-index-exporter/scripts/myvenv/bin/python /home/boris/maven-index-exporter/scripts/run_full_export.py https://repo.maven.apache.org/maven2/ /tmp/maven-index\
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
