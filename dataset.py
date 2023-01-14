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

class NormalDataset(Dataset):
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

class GFF3Dataset(Dataset):
    '''
    A dataset is the view over the data. As for the reader the software must distinguish
    between a generic tabular data and GFF3 data, which is a peculiar case.
    '''
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        
    '''
    By means of a dataset object a number of insights over data can be obtained; each insight
    is called an operation.
    '''
    #operations down here
    def get_information(self):
        '''
        getting some basic information about the dataset. The basic information are the name and data type ofeach column
        '''
        result = {}
        for i in self.df.columns:
            result[i] = self.df[i].dtype

        return NormalDataset(pd.DataFrame({'columns':result.keys(), 'data_type':result.values()}))

    def unique_seq_IDs(self):
        result = []
        for i in self.df.Attribute:
            attributes = get_attributes(i)
            try:
                result.append(attributes['ID'])
            except:
                pass
        return NormalDataset(pd.Series(result))
    
def get_attributes(row):
    '''
    allows to get a dictionary containing all the attributes of a row
    '''
    #maybe it is better if it returns a pandas dataframe
    row = row.split(';')
    attributes = {}
    for attribute in row:
        attribute = attribute.split('=')
        if len(attribute)>2:
            raise Exception('wrong attribute')
        attributes[attribute[0]] = attribute [1]
    return attributes