#!/usr/bin/env python

""" For each compound in given library, convert SMILES string into 3D structure
    and output .pdb file

    Author: Roy Nguyen
    Last edited: July 19, 2019
"""

import sys
import os
import datetime
import time
import subprocess
import pandas as pd

pdb_output_folder = "Compound-3D-Structure"
output_subfolder = "3D-Structure-Files"
single_pdb_file = "Mycobacterium_Compounds.pdb"

def main():
    start = datetime.datetime.now()
    sys.stdout.write("Start time: " + str(start) + "\n")
    sys.stdout.write("\n")
    cwd = os.getcwd()

    smiles = sys.argv[1]
    single_file = sys.argv[2]
    file_name = os.path.join(cwd, smiles)
    #if single_file.upper() == "TRUE":
    #    process_structure_library(file_name, smiles)
    #else:
    #    process_structure(file_name, smiles)

    build_single_pdb()
        
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
    output_folder = os.path.join(cwd, pdb_output_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_sub = os.path.join(cwd, output_subfolder)
    if not os.path.exists(output_subfolder):
        os.makedirs(output_subfolder)

    df = pd.read_csv(file_name)
    num_smiles_processed = 0
    for index, row in df.iterrows():
        cmp_id = str(row[0])
        smiles = str(row[1])
        output_name = os.path.join(output_sub, cmp_id)
        cmd = 'obabel -:"' + smiles + '" -opdb -O "' + output_name + '.pdb" --gen3d -c --title "' + cmp_id + '"'
        subprocess.call(cmd, shell=True)
        num_smiles_processed +=1

    sys.stdout.write("Processed %d compounds \n" % (num_smiles_processed))
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
    output_folder = os.path.join(cwd, pdb_output_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_sub = os.path.join(cwd, output_subfolder)
    if not os.path.exists(output_subfolder):
        os.makedirs(output_subfolder)

    output_name = os.path.join(output_sub, "Mycobacterium_Compounds")
    cmd = 'obabel -ismi "' + file_name + '" -opdb -O "' + output_name + '.pdb" --gen3d -c'
    subprocess.call(cmd, shell=True)

    return

def build_single_pdb():
    '''
    Merge all .pdb files into one single .pdb file
    '''
    cwd = os.getcwd()
    input_folder = os.path.join(cwd, pdb_output_folder)
    input_subfolder = os.path.join(input_folder, output_subfolder)
    input_files = sorted(os.listdir(input_subfolder))
    output_txt = ""
    num_mol = 1
    sys.stdout.write("Processing .pdb files...\n")
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
                    compound = line[10:]
                    output_txt += compound + "\n"
                else:
                    output_txt += line
        num_mol += 1

    sys.stdout.write("Writing single .pdb file...\n")
    output = os.path.join(input_folder, single_pdb_file)
    with open(output, "w") as out:
        out.write(output_txt)

    sys.stdout.write("Done!\n")
    sys.stdout.write("\n")
    return


if __name__ == "__main__":
    main()