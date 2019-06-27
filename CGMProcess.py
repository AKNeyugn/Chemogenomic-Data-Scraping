#!/usr/bin/env python

""" Find genes overlapping between compound libraries. 
    Initially designed to create 1 single CGM from different CGMs, 
    but task dropped.

    Author: Roy Nguyen
    Last edited: June 27, 2019
"""


import sys
import os
import datetime
import time
import shutil
import pandas as pd

data_folder = "Data-Files"

def main():
    start = datetime.datetime.now()
    sys.stdout.write("Start time: " + str(start) + "\n")
    sys.stdout.write("\n")

    libraries = sys.argv[1:]
    find_overlap_genes(libraries)

    end = datetime.datetime.now()
    time_taken = end - start
    sys.stdout.write("Time taken: " + str(time_taken.seconds // 60) + " minutes " 
                    + str(time_taken.seconds % 60) + " seconds. \n")
    sys.stdout.write("Script finished! \n")
    return
        
def find_overlap_genes(libraries):
    '''
    '''
    cwd = os.getcwd()
    data_folder_path = os.path.join(cwd, data_folder)
    list_total_genes = []
    for library in libraries:
        files_path = os.path.join(data_folder_path, library)
        list_files = os.listdir(files_path)
        for data_file in list_files:
            gene_name = extract_gene_name(data_file)
            list_total_genes.append(gene_name)

    non_overlap = set(list_total_genes)
    overlap = []
    for gene in non_overlap:
        if list_total_genes.count(gene) > 1:
            overlap.append(gene)

    print(len(list_total_genes))  
    print(len(non_overlap))
    print(len(overlap))
    print(overlap)
    return

def extract_gene_name(file_name):
    '''
    Get gene name from data file name

    Args:
        file_name (string): name of data file for gene
    
    Return:
        (string): name of gene
    '''
    end_idx = file_name.index(".csv")
    gene_name = file_name[:end_idx].upper()
    return gene_name


if __name__ == "__main__":
    main()