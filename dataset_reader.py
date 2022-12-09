from abc import ABC,abstractmethod
import numpy as np
import pandas as pd

class superclassofdatasetreaders(ABC):
    '''
    general abstract interface that defines the procedure that a datasetreader is provided with
    '''
    @abstractmethod
    def read(self, filepath):
        pass

class Dataset():
    '''
    output object of GFF3reader
    it is a wrapper around a pandas dataframe
    '''
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

class gff3reader(superclassofdatasetreaders):
    '''
    specific for GFF3 files, it should be compliant with a general abstract interface
    returns a dataset object as output that is a wrapper around a Pandas DataFrame
    '''
    def read(self, filepath) -> Dataset:
        self.filepath = filepath
        df = pd.read_csv(filepath) #pd.DataFrame
        return Dataset(df)

filepath='Homo_sapiens.GRCh38.85.gff3.gz'
reader = gff3reader()
ds = reader.read(filepath)
print(ds.df.head())