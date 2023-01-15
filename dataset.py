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
    def get_information(self) -> NormalDataset:
        '''
        getting some basic information about the dataset. The basic information are the name and data type ofeach column
        '''
        result = {}
        for i in self.df.columns:
            result[i] = self.df[i].dtype

        return NormalDataset(pd.DataFrame({'columns':result.keys(), 'data_type':result.values()}))

    def unique_seq_IDs(self) -> NormalDataset:
        #probably there is a smarter way
        '''
        obtaining the list of unique sequence IDs available in the dataset
        '''
        # 960,851 ids of which 350,631 unique
        # 1,640,998 without an id
        result = {}
        for row in self.df.Attribute:
            attributes = get_attributes(row)
            try:
                id = attributes['ID'].split(':')
            except:
                if KeyError:
                    continue

            if id[1] not in result.keys():
                    result[id[1]] = id[0]
            else:
                result[id[1]] += ','+id[0]

        return NormalDataset(pd.DataFrame({'ID':result.keys(),'type':result.values()}))
    
    def type_of_operations(self) -> NormalDataset:
        '''
        obtaining the list of unique type of operations available in the dataset
        '''
        pass

    def features_with_same_source(self, source) -> NormalDataset:
        '''
        counting the number of features provided by the same source
        '''
        n = len(self.df[self.df.Source == source].index) #faster than other methods s.a. len(df) and df.shape[0]
        return NormalDataset(pd.DataFrame({'source':source,'features':n},index=[0]))

    def number_of_entries_for_each_type_of_operation(self):
        '''
        counting the number of entries for each type of operation
        '''
        pass

    def get_chromosomes(self) -> 'GFF3Dataset':
        '''
        deriving a new dataset containing only the information about entire chromosomes. Entries with entirechromosomes comes from source GRCh38
        '''
        return GFF3Dataset(self.df[self.df.Source == 'GRCh38'])

    def fraction_of_unassembled_seq(self):
        '''
        calculating the fraction of unassembled sequences from source GRCh38. Hint: unassembled sequences are of type supercontig while the others are of type chromosome
        '''
        chromosomes = self.get_chromosomes()
        fraction = len(chromosomes.df[chromosomes.df.Type == 'supercontig'].index) / len(chromosomes.df.index)
        return NormalDataset(pd.DataFrame({'fraction of unassembled sequences': fraction},index=[0]))

    def ensembl_havana(self) -> 'GFF3Dataset':
        '''
        obtaining a new dataset containing only entries from source ensembl, havana and ensembl_havana
        '''
        return GFF3Dataset(self.df[(self.df.Source == 'ensembl') | (self.df.Source == 'havana') | (self.df.Source == 'ensembl_havana')])

    def boh(self):
        '''
        counting the number of entries for each type of operation for the dataset containing only entries from source ensembl, havana and ensembl_havana
        '''
        pass

    def get_gene_names(self) -> NormalDataset:
        '''
        returning the gene names from the dataset containing containing only entries from source ensembl, havana and ensembl_havana
        '''
        names = []
        for row in self.ensembl_havana().df.Attribute:
            attributes = get_attributes(row)
            try:
                if 'gene' in attributes['ID']:
                    names.append(attributes['Name'])
            except:
                if KeyError:
                    continue
        return NormalDataset(pd.DataFrame({'Name':names}))
    
def get_attributes(row):
    '''
    allows to get a dictionary containing all the attributes of a row
    '''
    #maybe it is better if it returns a pandas dataframe
    row = row.split(';')
    attributes = {}
    for attribute in row:
        attribute = attribute.split('=')
        attributes[attribute[0]] = attribute [1]
    return attributes