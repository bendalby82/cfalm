#!/bin/bash
RELEASEINFO=release/releaseinfo.txt
RELEASENAME=$(git tag -l 'cfalm*' | head -n 1)

rm -rf release
mkdir -p release

cp manifest.yml release/
cp README.md release/
cp -R appstatus release/
cp -R appstatusview release/

rm -rf release/appstatus/venv

echo 'Release created on: '$(date) >> $RELEASEINFO
echo '' >> $RELEASEINFO
echo 'Last commit:' >> $RELEASEINFO 
git log -n 1 --pretty=oneline >> $RELEASEINFO

zip -r $RELEASENAME.zip release
