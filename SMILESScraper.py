#!/usr/bin/env python

""" Get the name and canonical SMILES of all compounds in given library

    Author: Roy Nguyen
    Last edited: June 14, 2019
"""

import sys
import os
import datetime
import time
from multiprocessing import Pool
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
import pandas as pd

cmp_output_folder = "Compounds-SMILES"
cmp_search_url_start = "http://chemgrid.org/cgm/tmp_compound.php?cid="
cmp_name_url_start = "http://chemgrid.org/cgm/tmp_table.php?search=1&l=0&c=&id="
known_error = {
    "SPE01505035": "https://pubchem.ncbi.nlm.nih.gov/compound/16667706",
    "SPE01505950": "https://pubchem.ncbi.nlm.nih.gov/compound/16698648",
    "LOPAC 00420": "https://pubchem.ncbi.nlm.nih.gov/compound/6604070"
}

def main():
    start = datetime.datetime.now()
    sys.stdout.write("Start time: " + str(start) + "\n")
    sys.stdout.write("\n")
    cwd = os.getcwd()

    cgm = sys.argv[1]
    file_name = form_path(cwd, cgm)
    smiles_scraper(file_name, cgm)
        
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
    list_cmps_id = df[df.columns[0]]    # Comment and replace to debug specific compounds

    p = Pool(8)
    results = p.map(smiles_parse, list_cmps_id)
    p.terminate()
    p.join()
    
    output = pd.DataFrame(results, columns=["Supplier ID", "Name", "Canonical SMILES"])
    
    with open(output_name, "w", newline="") as ref:
        output.to_csv(ref, index=False)
    
    sys.stdout.write("Done! \n")
    sys.stdout.write("\n")
    return

def smiles_parse(cmp_id):
    '''
    Parse compound info webpage for name and canonical SMILES

    Args:
        cmp_id (string): supplier ID of compound

    Return:
        (tuple): tuple containing supplier ID, name and canonical
                SMILES of compound
    '''
    session = HTMLSession()

    # Deal with compounds with known incomplete SMILES
    if cmp_id in known_error.keys():    
        search_url = known_error[cmp_id]
        search_response = session.get(search_url)
        search_response.html.render(timeout=120)

        # Get canonical SMILES of compound
        smiles = search_response.html.xpath("//section[contains(@id, 'Canonical-SMILES')]//p")[0].text
        
        # Get name of compound
        if cmp_id == "SPE01505035":
            ind = 2
        elif cmp_id == "SPE01505950":
            ind = 1
        elif cmp_id == "LOPAC 00420":
            ind = 4
        cmp_name = search_response.html.xpath("//div[contains(@class, 'truncated-columns')]//p")[ind].text
    else:
        search_name = format_cmp_id(cmp_id)
        search_url = cmp_search_url_start + search_name
        search_response = session.get(search_url)
        search_response.html.render(timeout=120)
        
        # Get canonical SMILES of compound
        smiles_raw = search_response.html.xpath("//tr")[15].xpath("//td")[1].text
        smiles = ""
        for part in smiles_raw.split("\n"):
            smiles += part
        
        # Get name of compound
        cmp_name_raw = search_response.html.xpath("//h4")[0].text
        if cmp_name_raw == "":
            # Parse another compound search result page for name
            name_url = cmp_name_url_start + search_name
            name_response = requests.get(name_url)
            name_response_content = BeautifulSoup(name_response.content, "html.parser")
            table = name_response_content.find_all("table")[2]
            info_list = table.find_all("tr")[1]
            cmp_name = info_list.find_all("td")[5].get_text()
        else:
            cmp_name = ""
            for part in cmp_name_raw.split("\n"):
                cmp_name += part

    search_response.close()
    session.close()
    return (cmp_id, cmp_name, smiles)


def extract_library_name(cgm_file):
    '''
    Get library name from CGM file name

    Args:
        cgm_file (string): CGM file name

    Return:
        (string): library name
    '''
    start_index = cgm_file.index("CGM\\")
    end_index = cgm_file.index("_CGM")
    library_name = cgm_file[start_index+4:end_index]
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