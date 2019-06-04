"""
"""

import sys
import os
from bs4 import BeautifulSoup
import requests
import csv


main_url_start = "http://chemgrid.org/cgm/screens.php?sublib="
main_url_end = "&submit=Choose+DB"
data_url_parts = ["http://chemgrid.org/cgm/do_plot.php?p=1&pID=1&l=", "&sp=",
                "&pn=0&r=", "&cid=0&s=", "&out=csv&fn=./uploads/plot_", "_", "_",
                "__pn0"]
library_indices = [1,2,3,4,5,7,8]    # url index of each CGM library

def main():
    scraper()

    sys.stdout.write("Done!")
    return

def scraper():
    '''
    '''
    for i in library_indices:
        main_url = main_url_start + str(i) + main_url_end
        main_response = requests.get(main_url)
        folder_name = ""
        if i == 1:
            main_page_content = BeautifulSoup(main_response.content, "html.parser")
            table = main_page_content.find_all("table")[2]
            folder_name = table.find_all("tr")[1].find_all("td")[1].get_text()
            strain_list = table.find_all("tr")
            strain_range = len(strain_list)
            sys.stdout.write("Parsing " + folder_name + " library... \n")
            for j in range(strain_range):
                if j != 0:
                    strain_info = strain_list[j].find_all("td")
                    library_name = strain_info[1].get_text()
                    strain_name = strain_info[0].get_text()
                    num_species = strain_info[2].get_text()
                    num_plates = strain_info[3].get_text()
                    data_url = data_url_former(library_name, strain_name, num_species, num_plates)
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





'''
url = "http://chemgrid.org/cgm/do_plot.php?p=1&pID=1&l=Lopac&sp=4932&pn=0&r=16&cid=0&s=MT2481-pdr1pdr3&out=csv&fn=./uploads/plot_4932_Lopac_MT2481-pdr1pdr3__pn0"

data = requests.get(url)
with open("out.csv", "w") as f:
    writer = csv.writer(f)
    reader = csv.reader(data.text.splitlines())

    for row in reader:
        writer.writerow(row)
        '''