#!/bin/bash

SERVER="http://localhost:8000"
HTML=`wget "${SERVER}/reports/project/" -q -O -`
UUIDS=`echo ${HTML} | perl -0ne 'print "$1\n" while (/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}?)/igs)' - | sort | uniq`

for UUID in ${UUIDS}; do
    echo "http://localhost:8000/reports/project/${UUID}/project/2013/12/"
    phantomjs110 rasterize.js http://localhost:8000/reports/project/${UUID}/project/2013/12/ ./out/${UUID}.pdf
done
