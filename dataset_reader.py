from abc import ABC,abstractmethod
import numpy as np
import pandas as pd
from dataset import Dataset

class DatasetReader(ABC):
    '''
    general abstract interface that defines the procedure that a datasetreader is provided with
    '''
    @abstractmethod
    def read(self, filepath: str):
        pass

class GFF3DatasetReader(DatasetReader):
    '''
    specific for GFF3 files, it should be compliant with a general abstract interface
    returns a dataset object as output that is a wrapper around a Pandas DataFrame
    '''
    def read(self, filepath: str) -> Dataset:
        if not filepath.endswith('.gff3.gz'):
            raise ValueError('Invalid file type. Expected .gff3.gz file.')
        try:
            df = pd.read_csv(filepath,
                            sep='\t',
                            compression='gzip',
                            header=None, #there is no header in our input data, we have to make it manually (next line)
                            names = ['Seqid','Source','Type','Start','End','Score','Strand','Phase','Attribute'], #to give a name to each column
                            nrows = 100, #only 100 lines, to test the script on a limited dataset
                            comment = '#', #lines that start with hashtag are considered comments; so easy in this way
                            na_values = '.'
                            )
        except FileNotFoundError:
            print(f"{filepath} not found")
        except:
            print(f"An error occured while reading the file")
        return Dataset(df).create()