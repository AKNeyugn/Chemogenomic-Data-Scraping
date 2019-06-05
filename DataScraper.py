#!/usr/bin/env python

""" For each compound library available on http://chemgrid.org/cgm/index.php,
    download all compounds vs mutant .csv data files and create chemogenomic
    matrix

    Author: Roy Nguyen
    Last edited: June 4, 2019
"""

import sys
import os
import datetime
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd


main_url_start = "http://chemgrid.org/cgm/screens.php?sublib="
main_url_end = "&submit=Choose+DB"
data_url_parts = ["http://chemgrid.org/cgm/do_plot.php?p=1&pID=1&l=", "&sp=",
                "&pn=0&r=", "&cid=0&s=", "&out=csv&fn=./uploads/plot_", "_", "_",
                "__pn0"]    # constant parts of data file download link
library_indices = [1,2,3,4,5,7,8]    # url index of each CGM library
data_output_folder = "Data-Files/"
cgm_output_folder = "CGM/"

def main():
    start = datetime.datetime.now()
    sys.stdout.write("Start time: " + str(start) + "\n")
    sys.stdout.write("\n")

    #scraper()
    libraries = os.listdir(data_output_folder)
    for library in libraries:
        dir_name = data_output_folder + library
        create_cgm(dir_name)

    end = datetime.datetime.now()
    time_taken = end - start
    sys.stdout.write("\n")
    sys.stdout.write("Time taken: " + str(time_taken.seconds // 60) + " minutes " 
                    + str(time_taken.seconds % 60) + " seconds. \n")
    sys.stdout.write("Script finished! \n")
    return

def scraper():
    '''
    For each compound library, download all mutant .csv data files
    '''
    for i in library_indices:
        folder_name = data_output_folder
        main_url = main_url_start + str(i) + main_url_end
        main_response = requests.get(main_url)
        main_page_content = BeautifulSoup(main_response.content, "html.parser")
        table = main_page_content.find_all("table")[2]

        # Create output folder for library
        library_name = table.find_all("tr")[1].find_all("td")[1].get_text()
        folder_name += library_name
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        strain_list = table.find_all("tr")
        strain_range = len(strain_list)
        num_mutants_processed = 0
        sys.stdout.write("Parsing " + library_name + " library... \n")
        for j in range(strain_range):
            if j != 0:
                strain_info = strain_list[j].find_all("td")
                strain_name = strain_info[0].get_text()
                # Filter out SPE0xxxx (compound) strains in Maybridge library
                if "SPE0" not in strain_name:
                    num_species = strain_info[2].get_text()
                    num_plates = strain_info[3].get_text()
                    num_bioactive = strain_info[6].get_text()
                    num_toxic = strain_info[7].get_text()
                    data_url = data_url_former(library_name, strain_name, num_species, num_plates)

                    # Write data into local .csv file
                    data = requests.get(data_url)
                    file_name = strain_name + "_" + num_bioactive + "_" + num_toxic
                    output_name = folder_name + "/" + file_name + ".csv"
                    with open(output_name, "w", newline="") as f:
                        writer = csv.writer(f)
                        reader = csv.reader(data.text.splitlines())

                        for row in reader:
                            writer.writerow(row)
                    num_mutants_processed += 1
                
            sys.stdout.write("Processed %d mutants \r" % (j))
            sys.stdout.flush()
        
        sys.stdout.write("Downloaded %d mutant data files! \n" % (num_mutants_processed))

    return

def create_cgm(folder_name):
    '''
    Create a chemical genomic matrix (compounds vs mutants) from data files
    in folder_name and output into a Excel file

    Args:
        folder_name (string): name of folder containing mutant data files
    '''
    # Create output folder if not exists
    if not os.path.exists(cgm_output_folder):
        os.makedirs(cgm_output_folder)

    library_name = folder_name[folder_name.index("/")+1:]
    sys.stdout.write("Creating CGM for " + library_name + "... \n")
    list_data = os.listdir(folder_name)
    output_name = cgm_output_folder + library_name + "_CGM.csv"
    output = pd.DataFrame()
    
    for i in range(len(list_data)):
        file_name = folder_name + "/" + list_data[i]
        df = pd.read_csv(file_name)
        indices = df[df.columns[0]]
        mutant_name = list_data[i][:list_data[i].index(".csv")]
        tmp_output = pd.DataFrame(list(df[df.columns[2]]), columns=[mutant_name], index=indices)
        output = pd.concat([output, tmp_output], axis=1, sort=False)

    output.to_csv(output_name)
    return


def data_url_former(library_name, strain_name, num_species, num_plates):
    '''
    Form .csv data file download link

    Args:
        library_name (string): name of compound library
        strain_name (string): name of mutant
        num_species (string): number of species for mutant
        num_plates (string): number of plates for mutant

    Return:
        (string): .csv data file download link
    '''
    data_url = ""
    data_url += data_url_parts[0] + library_name
    data_url += data_url_parts[1] + num_species
    data_url += data_url_parts[2] + num_plates
    data_url += data_url_parts[3] + strain_name
    data_url += data_url_parts[4] + num_species
    data_url += data_url_parts[5] + library_name
    data_url += data_url_parts[6] + strain_name
    data_url += data_url_parts[7]

    return data_url

if __name__ == "__main__":
    main()