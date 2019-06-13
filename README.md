# Wildenhain-Data-Scraper

# DataScraper.py

For each compound library available on http://chemgrid.org/cgm/index.php, download all compounds vs mutant .csv data files and create chemogenomic matrix.

Script expected runtime: ~8 minutes

Module requirements:
- pandas (pip install pandas)
- beautifulsoup (pip install beautifulsoup4)
- requests (pip install requests)

How to run: python DataScraper.py

Outputs:
- Data-Files folder with sub-folders for each compound library containing compounds vs mutant .csv data files
- CGM folder with chemogenomic matrix .csv files for each compound library

Note: In CGM output file, y-axis are the compounds in the library & x-axis are the mutants treated against the compounds. Mutants labels are as follows: name of strain _ number of bioactive compounds _ number of toxic compounds. Numbers and name are taken from http://chemgrid.org/cgm/index.php

Note: Some library name clarifications
- Spectrum    = Microsource Spectrum 2003
- SPECMTS3    = Microsource Spectrum 2005
- Spectrum_ED = Microsource Spectrum 2008
- Bioactive = Yeast Bioactive I
- Cytotoxic = Yeast Bioactive II

# SMILESScraper.py

NOTE: Cannot run on Linux lab computer because of requests_html module requirement

Get the name and canonical SMILES of all compounds in given library.

Script expected runtime: <10 minutes

Module requirements:
- pandas (pip install pandas)
- requests (pip install requests)
- requests_html (pip install requests_html) NOTE: Only supported by python3.6+
- beautifulsoup (pip install beautifulsoup4)

How to run: python SMILESScraper.py library_cgm_file
- library_cgm_file: path from current working directory to CGM file of library to process (eg. CGM\\Bioactive_CGM.csv)

Note: Need CGM output files from DataScraper.py to run

# CompoundStructure.py

For each compound in given library, convert SMILES string into 3D structure and output .pdb file

Script expected runtime: <12 minutes

Moduel requirements:
- pandas (pip install pandas)

How to run: python CompoundStructure.py library_SMILES_file
- library_SMILES_file: path from current working directory to SMILES file of library to process (eg. Compound-SMILES\\Bioactive_SMILES.csv)

Note: Need SMILES output files from SMILESScraper.py