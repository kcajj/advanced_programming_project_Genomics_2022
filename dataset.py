from abc import ABC,abstractmethod
import numpy as np
import pandas as pd

class Dataset(ABC):
    '''
    output object of GFF3reader
    it is a wrapper around a pandas dataframe
    '''
    @abstractmethod
    def __init__(self, df: pd.DataFrame) -> None:
        pass

class GFF3Dataset(Dataset):
    '''
    A dataset is the view over the data. As for the reader the software must distinguish
    between a generic tabular data and GFF3 data, which is a peculiar case.
    '''
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        if not ['Seqid','Source','Type','Start','End','Score','Strand','Phase','Attribute'] == list(self.df.columns.values):
            raise ValueError('Invalid file type. Expected gff3 data frame')
    '''
    By means of a dataset object a number of insights over data can be obtained; each insight
    is called an operation.
    '''
    #operations down here
    def firstoperation():
        pass