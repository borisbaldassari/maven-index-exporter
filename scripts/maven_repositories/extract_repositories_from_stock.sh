# Copyright (C) 2021 The Software Heritage developers
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information
# SPDX-License-Identifier: GPL-3.0-or-later

# This script reads all pom files listed in a text file and feed them to a
# python script to extract XML nodes of interest to find servers.

file_pom=$1

# Optional: set if file_pom contains relative paths.
#dir=/my/poms/dir

if [ -z  "${file_pom}" ]; then
    echo "Usage: $0 list_poms.txt"
    exit
fi

echo "# Appending to result.txt"

# Uncomment to add headers to csv (and to overwrite any existing file)
#echo "type,id,url" > result.txt
for p in `cat $file_pom`; do
    pom="${dir}$p"
    python3 ./extract_repositories_from_pom.py $pom >> result.txt
done

#echo "# Generating result_uniq.txt"
#tail --lines=+2 result.txt | grep -Ev "^# " | sort -u > result_uniq.txt
