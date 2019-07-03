#!/usr/bin/env python

""" For all unique compound in SuppTable_S2, get 3D structure .pdb files
    created with CompoundStructure.py and output .csv file mapping compound ID
    to compound name

    Author: Roy Nguyen
    Last edited: June 27, 2019
"""


import sys
import os
import datetime
import time
import shutil
import pandas as pd

unique_compound_file = "UniqueCompounds.xlsx"
pdb_output_folder = "Unique-Compound-3D-Structure"
pdb_output_subfolder = "3D-Structure-Files"
pdb_origin_folder = "Compound-3D-Structure"
output_failed_mol = "FailedUniqueCompounds.txt"
single_pdb_file = "UniqueCompounds.pdb"
failed_mol = []

def main():
    start = datetime.datetime.now()
    sys.stdout.write("Start time: " + str(start) + "\n")
    sys.stdout.write("\n")
        
    #unique_cmps = get_unique_cmps()
    #get_pdb_files(unique_cmps)
    build_single_pdb()

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
            compound = df.iloc[i+3,1]
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
    output_subfolder = os.path.join(output_folder, pdb_output_subfolder)
    if not os.path.exists(output_subfolder):
        os.makedirs(output_subfolder)

    for library in unique_cmps.keys():
        sys.stdout.write("Copying .pdb files for " + library + "...\n")
        origin = os.path.join(pdb_folder, library)
        for mol in unique_cmps[library]:
            compound = mol +".pdb"
            pdb_file = os.path.join(origin, compound)
            output = os.path.join(output_subfolder, compound)
            shutil.copy(pdb_file, output)
        sys.stdout.write("Done with " + library + "!\n")
    
    sys.stdout.write("Done!\n")
    sys.stdout.write("\n")
    return

def build_single_pdb():
    '''
    Merge all .pdb files into one single .pdb file
    '''
    cwd = os.getcwd()
    input_folder = os.path.join(cwd, pdb_output_folder)
    input_subfolder = os.path.join(input_folder, pdb_output_subfolder)
    input_files = os.listdir(input_subfolder)
    cmp_data = {"Compound ID": [], "Compound Name": []}
    output_txt = ""
    num_mol = 1
    sys.stdout.write("Processing unique compound .pdb files...\n")
    for input_file in input_files:
        output_txt += "MODEL        " + str(num_mol) + "\n"
        file_path = os.path.join(input_subfolder, input_file)
        with open(file_path, "r") as f:
            for line in f:
                if line == "END\n":
                    if num_mol == len(input_files):
                        output_txt += line
                    else:
                        output_txt += "ENDMDL\n"
                elif "COMPND" in line:
                    # Get data for name mapping file
                    compound = line[10:]
                    div_idx = compound.index(": ")
                    end_idx = compound.index(" \n")
                    cmp_id = compound[:div_idx]
                    cmp_name = compound[div_idx+2:end_idx]
                    cmp_data["Compound ID"].append(cmp_id)
                    cmp_data["Compound Name"].append(cmp_name)
                    # Get data for pdb file
                    idx = line.index(": ")
                    output_txt += line[:idx] + "\n"
                else:
                    output_txt += line
        num_mol += 1

    sys.stdout.write("Writing single .pdb file...\n")
    output = os.path.join(input_folder, single_pdb_file)
    with open(output, "w") as out:
        out.write(output_txt)

    sys.stdout.write("Writing name mapping .csv file...\n")
    output_csv = os.path.join(input_folder, "UniqueCompoundsNames.csv")
    df = pd.DataFrame.from_dict(cmp_data)

    with open(output_csv, "w", newline="") as out:
        df.to_csv(out, index=False)

    sys.stdout.write("Done!\n")
    sys.stdout.write("\n")
    return


if __name__ == "__main__":
    main()