


WORKDIR=/work
FILE_IN=$WORKDIR/nexus-maven-repository-index.gz

localtime=$(date +"%Y-%m-%d %H:%M:%S")
echo "Docker Script started on $localtime."
echo "# Checks.."

echo "* Content of /opt:"
ls -l /opt
echo "* Content of $WORKDIR:"
ls -l $WORKDIR

echo "* Will read files from [$FILE_IN]."

if [ ! -r "$FILE_IN" ]; then
    echo "Cannot find file [$FILE_IN]."
    echo "Need an index file to work on. Exiting 4."
    exit 4
else
    echo "*   Found file [$FILE_IN]."
fi

indexer=$(find /opt/ -name "indexer-cli-*.jar")
if [ "$indexer" = "" ]; then
    echo "Cannot find indexer. Exiting 6."
    exit 6
else
    echo "*   Found indexer [$indexer]."
fi

clue=$(find /opt/ -name "clue-*.jar")
if [ "$clue" = "" ]; then
    echo "Cannot find clue. Exiting 8."
    exit 8
else
    echo "*   Found clue [$clue]."
fi

echo "* Java version:."
java -version

echo "#############################"
if [ -d $WORKDIR/indexes ]; then
    echo "Found $WORKDIR/indexes, skipping index generation."
    du -sh $WORKDIR/indexes/
else
    echo "Unpacking [$FILE_IN] to $WORKDIR/indexes"
    java --illegal-access=permit -jar $indexer --unpack $FILE_IN --destination $WORKDIR/indexes/ --type full 2>&1 | grep -v WARNING
fi

localtime=$(date +"%Y-%m-%d %H:%M:%S")
echo "Unpacking finished on $localtime."

echo "#############################"
if [ -d $WORKDIR/export ]; then
    echo "Found $WORKDIR/export, skipping index export."
    ls -lh $WORKDIR/export/
else
    echo "Exporting indexes $WORKDIR/indexes to $WORKDIR/export"
    java --illegal-access=permit -jar $clue $WORKDIR/indexes/ export $WORKDIR/export/ text 2>&1 | grep -v WARNING
fi

localtime=$(date +"%Y-%m-%d %H:%M:%S")
echo "Exporting finished on $localtime."

echo "#############################"

echo "Cleaning useless files."

echo "Size before cleaning:"
du -sh $WORKDIR/*

# We might want or not to delete the indexes
# Remember that when they're not present, everything
# gets recomputed every run..
#echo "* Removing indexes."
#rm -rf $WORKDIR/indexes/

# If files others than the .fld one are required, please comment
# the following lines.
echo "* Removing useless exports."
echo "  Keeping only fld text extract."
rm -f $WORKDIR/export/*.inf
rm -f $WORKDIR/export/*.len
rm -f $WORKDIR/export/*.pst
rm -f $WORKDIR/export/*.si
rm -f $WORKDIR/export/segments*

echo "  Size after cleaning:"
du -sh $WORKDIR/*

echo "* Make files modifiable by the end-user."
chmod -R 777 $WORKDIR/export/
chmod -R 777 $WORKDIR/indexes/

localtime=$(date +"%Y-%m-%d %H:%M:%S")
echo "Docker Script execution finished on $localtime."

