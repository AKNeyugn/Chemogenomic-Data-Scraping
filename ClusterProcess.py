#!/usr/bin/env python

""" Process K-means cluster analysis results for given compound library CGM,
    and output .json file mapping each compound to cluster.

    Author: Roy Nguyen
    Last edited: July 4, 2019
"""


import sys
import os
import datetime
import time
import json
import pandas as pd

cluster_list = "output.txt"
output_folder = "Cluster-Maps"

def main():
    start = datetime.datetime.now()
    sys.stdout.write("Start time: " + str(start) + "\n")
    sys.stdout.write("\n")

    library = sys.argv[1]
    process_clusters(library)

    end = datetime.datetime.now()
    time_taken = end - start
    sys.stdout.write("Time taken: " + str(time_taken.seconds // 60) + " minutes " 
                    + str(time_taken.seconds % 60) + " seconds. \n")
    sys.stdout.write("Script finished! \n")
    return

def process_clusters(library):
    '''
    Process cluster results and output .json file mapping compounds to clusters

    Args:
        library (string): path to library CGM file
    '''
    cwd = os.getcwd()
    cgm_file = os.path.join(cwd, library)
    clusters = os.path.join(cwd, cluster_list)
    library_name = library[library.index("\\")+1:library.index("_CGM")]
    
    # Get list of cluster numbers
    cluster_num = []
    with open(clusters, "r") as cl:
        for char in cl.read():
            if char != " " and char != "\n":
                cluster_num.append(char)

    # Get list of molecules
    df = pd.read_csv(cgm_file)
    cluster_mol = list(df["supplier_obj_id"])

    # Map molecule to cluster
    cluster_map = {}
    map_keys = sorted(list(set(cluster_num)))
    cm_keys = cluster_map.keys()
    for key in map_keys:
        if key not in cm_keys:
            cluster_map[key] = []
    for i in range(len(cluster_mol)):
        cluster_map[cluster_num[i]].append(cluster_mol[i])

    sys.stdout.write("Mapped " + str(len(cluster_num)) + " compounds!\n")
    sys.stdout.write("Outputting .json file...\n")
    output_file = library_name + "_ClusterMap.json"
    output_path = os.path.join(cwd, output_folder)
    output = os.path.join(output_path, output_file)
    with open(output, 'w') as fp:
        json.dump(cluster_map, fp)

    sys.stdout.write("Done!\n")
    sys.stdout.write("\n")        
    return


if __name__ == "__main__":
    main()