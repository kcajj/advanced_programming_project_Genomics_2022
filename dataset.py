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
        if self.__df.columns.format() == ['Seqid','Source','Type','Start','End','Score','Strand','Phase','Attribute']:
            self.is_gff3=True
        #if a the dataset is gff3 a lot of operations will be active in the register, otherwise the class is just a wrapper and the operations are not active
        #still don't know how to implement this
        self.__active_operations = {}
        self.__operations = {'get_information': [self.get_information,'description'],
                            'unique_seq_IDs': [self.unique_seq_IDs,'description'],
                            'type_of_operations': [self.type_of_operations,'description'],
                            'same_source': [self.same_source,'description'],
                            'entries_for_each_type_of_operation': [self.entries_for_each_type_of_operation,'description'],
                            'get_chromosomes': [self.get_chromosomes,'filter'],
                            'fraction_of_unassembled_seq': [self.fraction_of_unassembled_seq,'statistic'],
                            'ensembl_havana': [self.ensembl_havana,'filter'],
                            'entries_for_each_type_of_operation_ensemblhavana': [self.entries_for_each_type_of_operation_ensemblhavana,'description'],
                            'get_gene_names': [self.get_gene_names,'description']}
                    
    def get_df(self) -> pd.DataFrame:#from the other modules, this has to be the only way to access the pandas dataframe that is inside the dataset class
        return self.__df

    #decorator
    def activate(operation):
        def check(self,*args,**kwargs):
            if operation.__name__ not in self.__active_operations.keys():
                try:
                    output = operation(self,*args,**kwargs)
                    if not output.__df.empty:
                        self.__active_operations[operation.__name__] = self.__operations[operation.__name__]
                    return output
                except:
                    pass
            else:
                output = operation(self,*args,**kwargs)
                return output
        return check

    def get_active_operations(self):
        for operation in self.__operations.values():
            operation[0]()
        return self.__active_operations.keys()
    '''
    By means of a dataset object a number of insights over data can be obtained; each insight
    is called an operation.
    '''

    #operations down here
    @activate
    def get_information(self) -> 'Dataset':
        '''
        getting some basic information about the dataset. The basic information are the name and data type ofeach column
        '''
        #this function gives almost the same output: self.__df.info()
        print(self.__df.info())
        result = {}
        for i in self.__df.columns:
            result[i] = self.__df[i].dtype

        return Dataset(pd.DataFrame({'columns':result.keys(), 'data_type':result.values()}))

    @activate
    def unique_seq_IDs(self) -> 'Dataset':
        '''
        obtaining the list of unique sequence IDs available in the dataset
        '''
        return Dataset(pd.DataFrame({'unique_IDs':self.__df.Seqid.unique()}))

    @activate
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

    @activate
    def same_source(self) -> 'Dataset':
        '''
        counting the number of features provided by the same source
        '''
        return Dataset(self.__df.Source.value_counts().to_frame())

    @activate
    def entries_for_each_type_of_operation(self):
        '''
        counting the number of entries for each type of operation
        '''
        pass

    @activate
    def get_chromosomes(self) -> 'Dataset':
        '''
        deriving a new dataset containing only the information about entire chromosomes. Entries with entirechromosomes comes from source GRCh38
        '''
        return Dataset(self.__df[self.__df.Source == 'GRCh38'])

    @activate
    def fraction_of_unassembled_seq(self) -> 'Dataset':
        '''
        calculating the fraction of unassembled sequences from source GRCh38. Hint: unassembled sequences are of type supercontig while the others are of type chromosome
        '''
        chromosomes = self.get_chromosomes().__df
        fraction = len(chromosomes[chromosomes.Type == 'supercontig'].index) / len(chromosomes.index)
        return Dataset(pd.DataFrame({'fraction of unassembled sequences': fraction},index=[0]))

    @activate
    def ensembl_havana(self) -> 'Dataset':
        '''
        obtaining a new dataset containing only entries from source ensembl, havana and ensembl_havana
        '''
        return Dataset(self.__df[(self.__df.Source == 'ensembl') | (self.__df.Source == 'havana') | (self.__df.Source == 'ensembl_havana')])

    @activate
    def entries_for_each_type_of_operation_ensemblhavana(self):
        '''
        counting the number of entries for each type of operation for the dataset containing only entries from source ensembl, havana and ensembl_havana
        '''
        pass

    @activate
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
