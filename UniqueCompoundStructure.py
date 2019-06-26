#!/usr/bin/env python

""" For all unique compound in SuppTable_S2, get 3D structure .pdb files
    created with CompoundStructure.py

    Author: Roy Nguyen
    Last edited: June 25, 2019
"""


import sys
import os
import datetime
import time
import shutil
import pandas as pd

unique_compound_file = "UniqueCompounds.xlsx"
pdb_output_folder = "Unique-Compound-3D-Structure"
pdb_origin_folder = "Compound-3D-Structure"
output_failed_mol = "FailedUniqueCompounds.txt"
failed_mol = []

def main():
    start = datetime.datetime.now()
    sys.stdout.write("Start time: " + str(start) + "\n")
    sys.stdout.write("\n")
        
    unique_cmps = get_unique_cmps()
    get_pdb_files(unique_cmps)

    end = datetime.datetime.now()
    time_taken = end - start
    sys.stdout.write("Time taken: " + str(time_taken.seconds // 60) + " minutes " 
                    + str(time_taken.seconds % 60) + " seconds. \n")
    sys.stdout.write("Script finished! \n")
    return

def get_unique_cmps():
    '''
    Extract list of unique compounds in SuppTable file and sort them by library

    Return:
        (dict): dict containing unique compounds sorted by library
    '''
    unique_cmps = {}
    sys.stdout.write("Extracting unique compounds...\n")
    with pd.ExcelFile(unique_compound_file) as xls:
        df = pd.read_excel(xls, sheet_name=0, keep_default_na=False, na_values=[""])
        cmps = df.iloc[3:,1]
        for i in range(len(cmps)):
            library = df.iloc[i+3,0]
            if library not in unique_cmps.keys():
                unique_cmps[library] = []
            compound_id = df.iloc[i+3,1]
            compound_name = df.iloc[i+3,2]
            compound = compound_id + ": " + compound_name
            unique_cmps[library].append(compound)
    
    sys.stdout.write("Done!\n")
    sys.stdout.write("\n")
    return unique_cmps

def get_pdb_files(unique_cmps):
    '''
    For each unique compound, get .pdb files into output folder

    Args:
        unique_cmps (dict):  dict containing unique compounds 
            sorted by library
    '''
    cwd = os.getcwd()
    pdb_folder = os.path.join(cwd, pdb_origin_folder)
    output_folder = os.path.join(cwd, pdb_output_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for library in unique_cmps.keys():
        sys.stdout.write("Copying .pdb files for " + library + "...\n")
        origin = os.path.join(pdb_folder, library)
        for mol in unique_cmps[library]:
            cmp_id = extract_id(mol)
            compound = cmp_id+".pdb"
            pdb_file = os.path.join(origin, compound)
            output = os.path.join(output_folder, compound)
            shutil.copy(pdb_file, output)
        sys.stdout.write("Done with " + library + "!\n")
    
    sys.stdout.write("Done!\n")
    sys.stdout.write("\n")
    return


def extract_id(compound):
    '''
    Extract compound id from full compound name 

    Args:
        compound (string): full compound name (id + name)

    Return:
        (string): compound id
    '''
    end_idx = compound.index(": ")
    cmp_id = compound[:end_idx]
    return cmp_id


if __name__ == "__main__":
    main()