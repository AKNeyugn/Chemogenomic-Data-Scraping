#!/usr/bin/env python

"""
"""

import sys
import os
import datetime
from multiprocessing import Pool
from requests_html import HTMLSession
import requests
import csv
import pandas as pd


cgm_output_folder = "CGM"
cmp_output_folder = "Compounds-SMILES"
cmp_search_url_start = "http://chemgrid.org/cgm/tmp_compound.php?cid="

def main():
    start = datetime.datetime.now()
    sys.stdout.write("Start time: " + str(start) + "\n")
    sys.stdout.write("\n")
    cwd = os.getcwd()

    # Create compound info .csv files for each compound library
    '''
    cgms = os.listdir(cgm_output_folder)
    for cgm in cgms:
        tmp_file_name = form_path(cwd, cgm_output_folder)
        file_name = form_path(tmp_file_name, cgm)
        smiles_scraper(file_name, cgm)
        '''

    smiles_scraper("C:\\Users\\anhkh\\Documents\\UBC\\COOP\\S2019 CARDONA LAB\Wildenhain-Data-Scraper\\CGM\\Cytotoxic_CGM.csv", "Cytotoxic_CGM.csv")

    end = datetime.datetime.now()
    time_taken = end - start
    sys.stdout.write("Time taken: " + str(time_taken.seconds // 60) + " minutes " 
                    + str(time_taken.seconds % 60) + " seconds. \n")
    sys.stdout.write("Script finished! \n")
    return

def smiles_scraper(file_name, cgm_name):
    '''
    For all compounds in each CGM, get their actual name and 
    canonical SMILES and output into .csv file

    Args:
        file_name (string): path to CGM file to process
        cgm_name (string): name of CGM file
    '''
    # Create output folder if not exists
    cwd = os.getcwd()
    output_folder = form_path(cwd, cmp_output_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    library_name = extract_library_name(cgm_name)
    output_file_name = library_name + "_SMILES.csv"
    output_name = form_path(output_folder, output_file_name)
    output = pd.DataFrame()

    sys.stdout.write("Creating compound info file for " + library_name + "... \n")
    df = pd.read_csv(file_name)
    list_cmps_id = df[df.columns[0]]

    p = Pool(4)
    results = p.map(smiles_parse, list_cmps_id)
    p.close()
    p.join()
    
    output = pd.DataFrame(results, columns=["Supplier ID", "Name", "Canonical SMILES"])
    
    with open(output_name, "w", newline="") as ref:
        output.to_csv(ref, index=False)
    
    sys.stdout.write("Done! \n")
    sys.stdout.write("\n")
    return

def smiles_parse(cmp_id):
    '''
    '''
    session = HTMLSession()
    search_name = format_cmp_id(cmp_id)
    search_url = cmp_search_url_start + search_name
    search_response = session.get(search_url)
    search_response.html.render()
    # Get name of compound
    cmp_name_parts = search_response.html.xpath("//h4")[0].text.split("\n")
    cmp_name = ""
    for part in cmp_name_parts:
        cmp_name += part
    # Get canonical SMILES of compound
    smiles = search_response.html.xpath("//tr")[15].xpath("//td")[1].text
    return (cmp_id, cmp_name, smiles)


def extract_library_name(cgm_file):
    '''
    Get library name from CGM file name

    Args:
        cgm_file (string): CGM file name

    Return:
        (string): library name
    '''
    end_index = cgm_file.index("_CGM")
    library_name = cgm_file[:end_index]
    return library_name

def format_cmp_id(cmp_id):
    '''
    Replace space in compound ID string to "%20" 
    '''
    search_name = cmp_id.replace(" ", "%20")

    return search_name

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