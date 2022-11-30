import numpy as np
import pandas as pd

header={0:'Chromosome number',1:'Source',2:'Type',3:'Start',4:'End',5:'Score',6:'Strand',7:'null',8:'phase',}
filepath='Homo_sapiens.GRCh38.85.gff3.gz'
df = pd.read_csv(filepath,
                compression='gzip',
                header=None,
                sep='\t',
                quotechar='"',
                #on_bad_lines='skip', #this is the main problem
                skiprows=200,
                nrows=1000, #only 100 lines, to test the script on a limited dataset
                #lineterminator='\r',
                engine='python'
                )

print(df.head())
print("Type-", type(df))
print(df.shape)

print(df.describe()) #useless

#let's give a tag to each column.
df_renamed = df.rename(columns={0: header[0],
                                1: header[1],
                                2: header[2],
                                3: header[3],
                                4: header[4],
                                5: header[5],
                                6: header[6],
                                7: header[7],
                                8: header[8]},
                                inplace=False)

print(df_renamed.head())

#there are a lot of lines that start with #
""" for i in df_renamed[header[0]]:
    if '#' in i:
        print(i) """
#remove lines that start with ###
index_bad = df_renamed['###' == df_renamed[header[0]]].index
print(index_bad)
df_renamed.drop(index_bad, inplace=True)
print(df_renamed.head()) #58245 righe nulle

for i in df_renamed[header[0]]:
    if '#' in i:
        print(i)