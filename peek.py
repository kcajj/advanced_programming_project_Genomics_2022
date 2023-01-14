import numpy as np
import pandas as pd

header = ['Seqid','Source','Type','Start','End','Score','Strand','Phase','Attribute'] #header taken from input_file_README
filepath='Homo_sapiens.GRCh38.85.gff3.gz'

#a deep analysis of pandas.read_csv() documentation allows to adapt the capabilities of pandas to our input data
df = pd.read_csv(filepath,
                sep='\t',
                compression='gzip',
                header=None, #there is no header in our input data, we have to make it manually (next line)
                names = header, #to give a name to each column
                #nrows = 100, #only 100 lines, to test the script on a limited dataset
                comment = '#', #lines that start with hashtag are considered comments; so easy in this way
                na_values = '.'
                )

print(df.head())
print("Type ", type(df))
print(df.shape)

print(df.describe()) #useless
for i in header:
    print()
    print()
    print(i)
    print(df[i].describe())

#to figure out the type of each column
#we retrive the set of all the possible elements of each column (for some of them they will be many)
elements_of_columns = {}
count_na=0
for i in header:
    if i not in ['Start','End','Attribute','Score']:
        for value in df[i].values:
            if not pd.isna(value):
                if i in elements_of_columns:
                    if value not in elements_of_columns[i]:
                        elements_of_columns[i].append(value)
                    else: pass
                else:
                    elements_of_columns[i] = [value]
            else:
                count_na += 1
for index,list in elements_of_columns.items():
    print(index,list)
print(count_na)
"""
Type ['chromosome', 'biological_region', 'gene', 'processed_transcript', 'exon', 'pseudogenic_transcript', 'pseudogene', 'miRNA_gene', 'miRNA', 'lincRNA_gene', 'lincRNA', 'transcript', 'CDS', 'processed_pseudogene', 'snRNA_gene', 'snRNA', 'five_prime_UTR', 'three_prime_UTR', 'aberrant_processed_transcript', 'NMD_transcript_variant', 'RNA', 'snoRNA_gene', 'snoRNA', 'rRNA_gene', 'rRNA', 'V_gene_segment', 'C_gene_segment', 'J_gene_segment', 'VD_gene_segment', 'supercontig', 'mt_gene']
Source ['GRCh38', '.', 'havana', 'mirbase', 'ensembl_havana', 'ensembl', 'insdc']
Strand ['.', '+', '-']
Phase ['.', '0', '1', '2']
score, start, end are numbers
seqid has no sense
attribute is full of things
"""