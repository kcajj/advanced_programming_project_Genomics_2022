import numpy as np
import pandas as pd

class Dataset():
    '''
    A dataset is the view over the data. As for the reader the software must distinguish
    between a generic tabular data and GFF3 data, which is a peculiar case.
    '''
    def __init__(self, df: pd.DataFrame) -> None:
        self.__df = df
        self.is_gff3 = False
        __registry_of_active_operations = {}
        if self.__df.columns.format() == ['Seqid','Source','Type','Start','End','Score','Strand','Phase','Attribute']:
            self.is_gff3=True
            __registry_of_active_operations = {}
        #if a the dataset is gff3 a lot of operations will be active in the register, otherwise the class is just a wrapper and the operations are not active
        #still don't know how to implement this

    def get_df(self) -> pd.DataFrame:#from the other modules, this has to be the only way to access the pandas dataframe that is inside the dataset class
        return self.__df
    '''
    By means of a dataset object a number of insights over data can be obtained; each insight
    is called an operation.
    '''
    #operations down here
    def get_information(self) -> 'Dataset':
        '''
        getting some basic information about the dataset. The basic information are the name and data type ofeach column
        '''
        #this function gives almost the same output: self.__df.info()
        result = {}
        for i in self.__df.columns:
            result[i] = self.__df[i].dtype

        return Dataset(pd.DataFrame({'columns':result.keys(), 'data_type':result.values()}))

    def unique_seq_IDs(self) -> 'Dataset':
        #probably there is a smarter way, also i don't know to which IDs is it referring
        '''
        obtaining the list of unique sequence IDs available in the dataset
        '''
        # 960,851 ids of which 350,631 unique
        # 1,640,998 without an id
        result = {}
        for row in self.__df.Attribute:
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

        return Dataset(pd.DataFrame({'ID':result.keys(),'type':result.values()}))
    
    def type_of_operations(self) -> 'Dataset':
        '''
        obtaining the list of unique type of operations available in the dataset
        '''
        #how can we classify the operations?
        #multiple options:
        #1: classification on the basis of the purpose
            # data filtering: filter the data based on specific criteria
            # statistics: return a value representing a measure over the dataset
            # data selection: return a column
        #2: classification on the basis of the output
            # dataframe
            # scalar
            # series
            #it is similar to the one above, but, since we have always to return a dataset object
            #and the dataset class accepts only a pd.dataframe object (it is a wrapper around it)
            #maybe it is better to stick with the first classfication.
        pass

    def features_with_same_source(self, source: str) -> 'Dataset':
        '''
        counting the number of features provided by the same source
        '''
        n = len(self.__df[self.__df.Source == source].index) #faster than other methods s.a. len(df) and df.shape[0]
        return Dataset(pd.DataFrame({'source':source,'features':n},index=[0]))

    def number_of_entries_for_each_type_of_operation(self):
        '''
        counting the number of entries for each type of operation
        '''
        pass

    def get_chromosomes(self) -> 'Dataset':
        '''
        deriving a new dataset containing only the information about entire chromosomes. Entries with entirechromosomes comes from source GRCh38
        '''
        return Dataset(self.__df[self.__df.Source == 'GRCh38'])

    def fraction_of_unassembled_seq(self) -> 'Dataset':
        '''
        calculating the fraction of unassembled sequences from source GRCh38. Hint: unassembled sequences are of type supercontig while the others are of type chromosome
        '''
        chromosomes = self.get_chromosomes().__df
        fraction = len(chromosomes[chromosomes.Type == 'supercontig'].index) / len(chromosomes.index)
        return Dataset(pd.DataFrame({'fraction of unassembled sequences': fraction},index=[0]))

    def ensembl_havana(self) -> 'Dataset':
        '''
        obtaining a new dataset containing only entries from source ensembl, havana and ensembl_havana
        '''
        return Dataset(self.__df[(self.__df.Source == 'ensembl') | (self.__df.Source == 'havana') | (self.__df.Source == 'ensembl_havana')])

    def boh(self):
        '''
        counting the number of entries for each type of operation for the dataset containing only entries from source ensembl, havana and ensembl_havana
        '''
        pass

    def get_gene_names(self) -> 'Dataset':
        '''
        returning the gene names from the dataset containing containing only entries from source ensembl, havana and ensembl_havana
        '''
        names = []
        for row in self.ensembl_havana().__df.Attribute:
            attributes = get_attributes(row)
            try:
                if 'gene' in attributes['ID']:
                    names.append(attributes['Name'])
            except:
                if KeyError:
                    continue
        return Dataset(pd.DataFrame({'Name':names}))
    





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


def decorator():
    pass