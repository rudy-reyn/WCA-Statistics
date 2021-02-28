# World Cube Association Dataset Scripts

Pandas script to allow a user to search for their rankings as of each competition they've competed in by event, to find their overall peak ranking. The WCA_export_Results.tsv and WCA_export_Competitions.tsv can by found at https://www.worldcubeassociation.org/results/misc/WCA_export.tsv.zip (download link). 

The solves-per-date.py file joined the competition and results dataset to get each competitors best solves at each competition they competed in along with the date, and the results were saved to two csvs. The get-rankings.py file imports the two csvs and allows the user to enter their desired search parameters.

The wca_download.sh script is used to download the tsv datasets to your current working directory and name folder with the date of exporting. 
