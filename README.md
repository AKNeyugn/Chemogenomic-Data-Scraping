# Wildenhain-Data-Scraper

For each compound library available on http://chemgrid.org/cgm/index.php, download all compounds vs mutant .csv data files and create chemogenomic matrix.

Script expected runtime: ~8 minutes (if running data files download script)

Module requirements:
- pandas (pip install pandas)
- beautifulsoup (pip install beautifulsoup4)
- requests (pip install requests)

How to run: python DataScraper.py

Outputs:
- Data-Files folder with sub-folders for each compound library containing compounds vs mutant .csv data files
- CGM folder with chemogenomic matrix .csv files for each compound library