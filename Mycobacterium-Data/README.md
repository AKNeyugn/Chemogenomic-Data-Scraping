# Mycobacterium-Data

**Paper:** Johnson et al. 2019. "Large-Scale Chemical–Genetics Yields New *M. tuberculosis* Inhibitor Classes." *Nature* 571 (July): 72-78.
https://doi.org/10.1038/s41586-019-1315-z

# CompoundStructure.py

For each compound in given library, convert SMILES string into 3D structure and output .pdb file.

**Module requirements:**

- OpenBabel (http://openbabel.org/wiki/Main_Page)
- pandas (pip install pandas)

**How to run:** *python CompoundStructure.py library_SMILES_file single_file*
- library_SMILES_file: path from current working directory to SMILES file of library to process (eg. Data-Files\compounds.csv)
- single_file: "true" if want output to be single file containing all compounds info for each library

**Outputs:**
- *Compound-3D-Structure* folder containing seperate .pdb files of each compounds in given library
- if running with single_file = "true", *Compound-3D-Structure* folder will also contain .pdb file containing all compounds info for each library

**Note:**
Expected compounds with failed 3D structure conversion due to missing SMILES:
- U14272896
- U20739209
- U21835532
- U32963902
- U84341231
- nan

The files for these compounds are manually moved to seperate *nan-SMILES* folder

**Note:**
.pdb file containing all compounds info is not uploaded to repository due to its large size

# CGMProcess.py

Read both chemogenomic data files (A-M and N-Z) and create CGM .csv file.

If run with inputs for both z_score_cutoff and p_value_cutoff, cell values in CGM will be binary (1 if input values pass z_score AND p_value cutoffs, 0 otherwise). In this case, output file will be named "Full_CGM_*z_score_cutoff*_*p_value_cutoff*.csv";

Otherwise, will create 2 CGM files: one where cell values are z_scores and another where cell values are p_values. In this case, z_score matrix will be name "Full_CGM_Z_score.csv" and p_value matrix will be named "Full_CGM_P_value.csv"

**Module requirements:**

- pandas (pip install pandas)

**How to run:** *python CGMProcess.py z_score_cutoff p_value_cutoff*
- z_score_cutoff: cutoff for z_score
- p_value_cutoff: cutoff for p_value 

**Outputs:**
- *CGM* folder containing .csv files

**Note:**
Need to input both z_score_cutoff and p_value_cutoff to have CGM with filtered binary values

**Note:**
CGM output is a compound vs gene matrix, where x-axis = gene and y-axis = compound

**Note:**

*A-M (input):*

- Total # rows: 4636478
- Unique compound rows with non n/a compound_stem and experiments at 50 micromolar: 47202
- Unique strain rows: 98

*N-Z (input):*

- Total # rows: 2696727
- Unique compound rows with non n/a compound_stem and experiments at 50 micromolar: 47202
- Unique strain rows: 57

*Full (output):*

- Total # rows (compounds): 47246
- Total # columns (strains): 155
- Unique compound rows with non n/a compound_stem and experiments at 50 micromolar: 47202

**Note:**
Input files, as well as output files, are not uploaded to repository due to their large size
