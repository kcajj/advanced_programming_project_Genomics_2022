import pandas as pd
from unittest.mock import patch
from functions import *

class Dataset():
    '''
    A dataset is the view over the data. As for the reader the software must distinguish
    between a generic tabular data and GFF3 data, which is a peculiar case.
    '''
    def __init__(self, df: pd.DataFrame):
        self._df = df
        self._operations = {}
        self._active_operations = {}
        self._subdatasets = {}

    def create(self):
        if self._df.columns.format() == ['Seqid','Source','Type','Start','End','Score','Strand','Phase','Attribute']:
            return GFF3Dataset(self._df)
        else:
            return self

    def get_df(self) -> pd.DataFrame:#from the other modules, this has to be the only way to access the pandas dataframe that is inside the dataset class
        return self._df

    def __update_operations(self):
        '''
        returns all the active operations; it is used to show the user the operation that he can use
        '''
        # the active operations can be called by other python files (but not by out UI) even if they are
        # inactive, so we added the prints in the decorator to show possible errors or empty output
        # to not show those prints after the activation of this function i used this patch method 
        # found it randomly online
        for name, operation in self._operations.items():
            with patch('builtins.print'):
                if type(operation()) == GFF3Dataset:
                    self._subdatasets[name] = operation()

    def get_active_operations(self) -> dict:
        self.__update_operations() #update active operations
        return self._active_operations

    def get_subdatasets(self) -> dict:
        self.__update_operations() #update active operations
        return self._subdatasets

class GFF3Dataset(Dataset):
    def __init__(self, df: pd.DataFrame):
        super().__init__(df)
        self._operations = {'information': self.information,
                            'unique_sequence_IDs': self.unique_sequence_IDs,
                            'unique_types': self.unique_types,
                            'same_source': self.same_source,
                            'entries_for_each_type': self.entries_for_each_type,
                            'chromosomes': self.chromosomes,
                            'fraction_of_unassembled_sequences': self.fraction_of_unassembled_sequences,
                            'ensembl_havana': self.ensembl_havana,
                            'entries_for_each_type_ensemblhavana': self.entries_for_each_type_ensemblhavana,
                            'gene_names': self.gene_names}

    '''
    By means of a dataset object a number of insights over data can be obtained; each insight
    is called an operation.
    '''

    #operations down here
    @activate
    def information(self) -> Dataset:
        '''
        getting some basic information about the dataset. The basic information are the name and data type ofeach column
        '''
        #!!!!!!!!!!!!!!!there is an error in the input that prevents to correctly label the types
        information = {}
        for column_name in self._df.columns:
            # iteration on columns of the df
            information[column_name] = self._df[column_name].dtype

        return Dataset(pd.DataFrame({'data_type':information.values()}, index = information.keys())).create()

    @activate
    def unique_sequence_IDs(self) -> Dataset:
        '''
        obtaining the list of unique sequence IDs available in the dataset
        '''
        return Dataset(pd.DataFrame({'unique_IDs':self._df.Seqid.unique()})).create()
        #self._df['Seqid']

    @activate
    def unique_types(self) -> Dataset:
        '''
        obtaining the list of unique type of operations available in the dataset
        '''
        return Dataset(pd.DataFrame({'unique_types':self._df.Type.unique()})).create()

    @activate
    def same_source(self) -> Dataset:
        '''
        counting the number of features provided by the same source
        '''
        return Dataset(self._df.Source.value_counts().to_frame()).create()

    @activate
    def entries_for_each_type(self) -> Dataset:
        '''
        counting the number of entries for each type of operation
        '''
        return Dataset(self._df.Type.value_counts().to_frame()).create()

    @activate
    def chromosomes(self) -> Dataset:
        '''
        deriving a new dataset containing only the information about entire chromosomes. Entries with entirechromosomes comes from source GRCh38
        '''
        return Dataset(self._df[self._df.Source == 'GRCh38']).create()

    @activate
    def fraction_of_unassembled_sequences(self) -> Dataset:
        '''
        calculating the fraction of unassembled sequences from source GRCh38. Hint: unassembled sequences are of type supercontig while the others are of type chromosome
        '''
        chromosomes = self.chromosomes()._df
        fraction = len(chromosomes[chromosomes.Type == 'supercontig'].index) / len(chromosomes.index)
        return Dataset(pd.DataFrame({'fraction of unassembled sequences': fraction},index=[0])).create()

    @activate
    def ensembl_havana(self) -> Dataset:
        '''
        obtaining a new dataset containing only entries from source ensembl, havana and ensembl_havana
        '''
        return Dataset(self._df[(self._df.Source == 'ensembl') | (self._df.Source == 'havana') | (self._df.Source == 'ensembl_havana')]).create()

    @activate
    def entries_for_each_type_ensemblhavana(self) -> Dataset:
        '''
        counting the number of entries for each type of operation for the dataset containing only entries from source ensembl, havana and ensembl_havana
        '''
        return self.ensembl_havana().entries_for_each_type()

    @activate
    def gene_names(self) -> Dataset:
        '''
        returning the gene names from the dataset containing containing only entries from source ensembl, havana and ensembl_havana
        '''
        names = []
        for row in self.ensembl_havana()._df.Attribute:
            attributes = get_attributes(row)
            try:
                if 'gene' in attributes['ID']:
                    names.append(attributes['Name'])
            except: 
                if KeyError:
                    continue
        return Dataset(pd.DataFrame({'Name':names})).create()