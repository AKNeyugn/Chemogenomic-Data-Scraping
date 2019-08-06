#!/usr/bin/env python

""" 

    Author: Roy Nguyen
    Last edited: July 24, 2019
"""


from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import numpy as np
import sys
import os
import datetime
import requests
import csv
import pandas as pd
import seaborn as sns
sns.set_style('darkgrid')
sns.set_palette('muted')
sns.set_context("notebook", font_scale=1.5,
                rc={"lines.linewidth": 2.5})

def main():
    start = datetime.datetime.now()
    sys.stdout.write("Start time: " + str(start) + "\n")
    sys.stdout.write("\n")
    cwd = os.getcwd()

    arg = sys.argv[1]
    analysis(arg)
    #fashion_scatter()

    end = datetime.datetime.now()
    time_taken = end - start
    sys.stdout.write("Time taken: " + str(time_taken.seconds // 60) + " minutes " 
                    + str(time_taken.seconds % 60) + " seconds. \n")
    sys.stdout.write("Script finished! \n")
    return

def analysis(arg):
    '''
    '''
    df = pd.read_csv(arg)
    index = df['supplier_obj_id']
    del df['supplier_obj_id']
    my_data = df.to_numpy()
    labels = (my_data < -4).astype(int)
    #print(labels)
    #print(my_data.shape)
    #print(my_data)

    scaler = MinMaxScaler(feature_range=[0, 1])
    data_rescaled = scaler.fit_transform(my_data[1:, 0:101])

    #Fitting the PCA algorithm with our Data
    '''
    pca = PCA().fit(data_rescaled)
    #Plotting the Cumulative Summation of the Explained Variance
    plt.figure()
    plt.plot(np.cumsum(pca.explained_variance_ratio_))
    plt.xlabel('Number of Components')
    plt.ylabel('Variance (%)') #for each component
    plt.title('Dataset Explained Variance')
    #plt.show()
    '''
    
    pca = PCA(n_components=40)
    pca_result = pca.fit_transform(my_data)

    pca_df = pd.DataFrame(pca_result, columns=['PCA%i' % i for i in range(40)], index=df.index)
    #print(pca_df)

    #fashion_scatter(pca_df, labels)

    # Set style of scatterplot
    sns.set_context("notebook", font_scale=1.1)
    sns.set_style("ticks")

    # Create scatterplot of df
    sns.lmplot(x='Score1',
               y='Score2',
               data=pca_df,
               fit_reg=False,
               legend=True,
               size=9,
               hue='Label',
               scatter_kws={"s":200, "alpha":0.3})

    plt.title('PCA Results', weight='bold').set_fontsize('14')
    plt.xlabel('Prin Comp 1', weight='bold').set_fontsize('10')
    plt.ylabel('Prin Comp 2', weight='bold').set_fontsize('10')
    return 

def fashion_scatter(x, colors):
    # choose a color palette with seaborn.
    num_classes = len(np.unique(colors))
    palette = np.array(sns.color_palette("hls", num_classes))

    # create a scatter plot.
    f = plt.figure(figsize=(8, 8))
    ax = plt.subplot(aspect='equal')
    sc = ax.scatter(x[:,0], x[:,1], lw=0, s=40, c=palette[colors.astype(np.int)])
    plt.xlim(-25, 25)
    plt.ylim(-25, 25)
    ax.axis('off')
    ax.axis('tight')

    # add the labels for each digit corresponding to the label
    txts = []

    for i in range(num_classes):

        # Position of each label at median of data points.

        xtext, ytext = np.median(x[colors == i, :], axis=0)
        txt = ax.text(xtext, ytext, str(i), fontsize=24)
        txt.set_path_effects([
            PathEffects.Stroke(linewidth=5, foreground="w"),
            PathEffects.Normal()])
        txts.append(txt)

    return f, ax, sc, txts

if __name__ == "__main__":
    main()
