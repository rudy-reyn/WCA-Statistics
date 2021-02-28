#!/usr/bin/env sh
#
#Script to download up to date WCA .tsv files.  

wget https://www.worldcubeassociation.org/results/misc/WCA_export.tsv.zip
mkdir -p export-$(date +"%Y-%m-%d")
mv WCA_export.tsv.zip export-$(date +"%Y-%m-%d")/
cd export-$(date +"%Y-%m-%d")
unzip WCA_export.tsv.zip
rm WCA_export.tsv.zip
rm README.md
rm metadata.json
