DBPATH=/var/www/PMIS/server/project/default.db
BACKUPDIR=/var/backups/pmis
FILENAME=default`date +"%Y%m%d"`.db
cp $DBPATH $BACKUPDIR/$FILENAME
