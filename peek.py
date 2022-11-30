import numpy as np
import pandas as pd

header = ['Chromosome number','Source','Type','Start','End','Score','Strand','null','phase'] #rough header
filepath='Homo_sapiens.GRCh38.85.gff3.gz'

#a deep analysis of pandas.read_csv() documentation allows to adapt the capabilities of pandas to our input data
df = pd.read_csv(filepath,
                sep='\t',
                compression='gzip',
                header=None, #there is no header in our input data, we have to make it manually (next line)
                names = header, #to give a name to each column
                nrows = 1000, #only 100 lines, to test the script on a limited dataset
                comment = '#' #lines that start with hashtag are considered comments; so easy in this way
                )

print(df.head())
print("Type ", type(df))
print(df.shape)

print(df.describe()) #useless

for i in header:
    print(df[i])
