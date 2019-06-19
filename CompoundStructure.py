#!/usr/bin/env python

""" For each compound in given library, convert SMILES string into 3D structure
    and output .pdb file

    Author: Roy Nguyen
    Last edited: June 19, 2019
"""

import sys
import os
import datetime
import time
import subprocess
import pandas as pd

pdb_output_folder = "Compound-3D-Structure"

def main():
    start = datetime.datetime.now()
    sys.stdout.write("Start time: " + str(start) + "\n")
    sys.stdout.write("\n")
    cwd = os.getcwd()

    smiles = sys.argv[1]
    single_file = sys.argv[2]
    file_name = form_path(cwd, smiles)
    if single_file.upper() == "TRUE":
        process_structure_library(file_name, smiles)
    else:
        process_structure(file_name, smiles)
        
    end = datetime.datetime.now()
    time_taken = end - start
    sys.stdout.write("Time taken: " + str(time_taken.seconds // 60) + " minutes " 
                    + str(time_taken.seconds % 60) + " seconds. \n")
    sys.stdout.write("Script finished! \n")
    return

def process_structure(file_name, smiles_name):
    '''
    Convert SMILES string of each compound in library 
    into 3D structure (pdb) in multiple output files

    Args:
        file_name (string): path to SMILES list file
        smiles_name (string): name of SMILES list file
    '''
    # Create output folder if not exists
    cwd = os.getcwd()
    library_name = extract_library_name(smiles_name)
    output_folder = form_path(cwd, pdb_output_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_subfolder = form_path(output_folder, library_name)
    if not os.path.exists(output_subfolder):
        os.makedirs(output_subfolder)

    df = pd.read_csv(file_name)
    num_smiles_processed = 0
    for index, row in df.iterrows():
        cmp_id = str(row[0])
        smiles = str(row[2])
        cmp_name = cmp_id + ": " + str(row[1])
        output_name = form_path(output_subfolder, cmp_id)
        cmd = 'obabel -:"' + smiles + '" -opdb -O "' + output_name + '.pdb" --gen3d -c --title "' + cmp_name + '"'
        subprocess.call(cmd)
        num_smiles_processed +=1

    sys.stdout.write("Processed %d compounds \n" % (num_smiles_processed))
    sys.stdout.write("Done with " + library_name + "! \n")
    return

def process_structure_library(file_name, smiles_name):
    '''
    Convert SMILES string of each compound in library 
    into 3D structure (pdb) in one single output file

    Args:
        file_name (string): path to SMILES list file
        smiles_name (string): name of SMILES list file
    '''
    # Create output folder if not exists
    cwd = os.getcwd()
    library_name = extract_library_name(smiles_name)
    output_folder = form_path(cwd, pdb_output_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_subfolder = form_path(output_folder, library_name)
    if not os.path.exists(output_subfolder):
        os.makedirs(output_subfolder)

    output_name = form_path(output_subfolder, library_name)
    cmd = 'obabel -ismi "' + file_name + '" -opdb -O "' + output_name + '.pdb" --gen3d -c'
    subprocess.call(cmd)

    return


def extract_library_name(smiles_file):
    '''
    Get library name from compound SMILES name

    Args:
        smiles_file (string): compound SMILES file name

    Return:
        (string): library name
    '''
    start_index = smiles_file.index("SMILES\\")
    end_index = smiles_file.index("_SMILES")
    library_name = smiles_file[start_index+7:end_index]
    return library_name

def form_path(start, end):
    '''
    Create string representing a path depending on
    Windows/Linux environment

    Args:
        start (string): start of output path
        end (string): string to add to end of start

    Return:
        (string): full path combining start and end
    '''
    path = ""
    if "/" in start:
        path = start + "/" + end
    elif "\\" in start:
        path = start + "\\" + end
    return path

if __name__ == "__main__":
    main()