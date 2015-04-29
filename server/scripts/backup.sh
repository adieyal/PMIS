DBPATH=/var/www/pmis/server/project/default.db
BACKUPDIR=/var/backups
DIR=`date +"%Y%m%d"`
cd /tmp
mkdir -p $DIR
cp $DBPATH $DIR &&
redis-dump > $DIR/redis-dump.json &&
tar cvmpfz $BACKUPDIR/$DIR.tgz $DIR &&
rm -r $DIR
