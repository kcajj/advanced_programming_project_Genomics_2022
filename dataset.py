import numpy as np
import pandas as pd
from unittest.mock import patch
from functions import get_attributes, activate

class Dataset():
    '''
    A dataset is the view over the data. As for the reader the software must distinguish
    between a generic tabular data and GFF3 data, which is a peculiar case.
    '''
    def __init__(self, df: pd.DataFrame) -> None:
        self._df = df
        self._is_gff3 = False
        if self._df.columns.format() == ['Seqid','Source','Type','Start','End','Score','Strand','Phase','Attribute']:
            self._is_gff3 = True
            self._active_operations = {'type_of_operations': [self.type_of_operations,'description'],
                                        'entries_for_each_type_of_operation': [self.entries_for_each_type_of_operation,'description'],
                                        'entries_for_each_type_of_operation_ensemblhavana': [self.entries_for_each_type_of_operation_ensemblhavana,'description']}
        self._operations = {'get_information': [self.get_information,'description'],
                            'unique_seq_IDs': [self.unique_seq_IDs,'description'],
                            'same_source': [self.same_source,'description'],
                            'get_chromosomes': [self.get_chromosomes,'filter'],
                            'fraction_of_unassembled_seq': [self.fraction_of_unassembled_seq,'statistic'],
                            'ensembl_havana': [self.ensembl_havana,'filter'],
                            'get_gene_names': [self.get_gene_names,'description']}
    
    def get_df(self) -> pd.DataFrame: #from the other modules, this has to be the only way to access the pandas dataframe that is inside the dataset class
        return self._df

    def get_active_operations(self):
        '''
        returns all the active operations; it is used to show the user the operation that he can use
        '''
        #for the web app usage this method is suitable, we will show the operations only after having run this
        #invece se questa classe viene usata da altri file di python gli utenti possono chiamare i metodi disattivati
        #forse c'è un modo più intelligente per gestire questa roba delle attivazioni
        #sarebbe figo se l'oggetto non avesse proprio i metodi che non sono attivati
            #possibili soluzioni:
                #metodi privati, diventano accessibili solo se attivati
                #due classi diverse (vedi branch con gff3 subclass)
                #chiamare le operazioni solo dopo essere passati da un altro metodo/lista
                    #ad esempio, obj.operation('get_information') in questo modo i metodi sono privati,
                    #l'operazione è eseguita solo se è nella liste
        #non mi convince nessuno di questi

        #soluzione:
        #ho aggiunto dei print che avvisano che la funzione è disattivata.
        #vengono mostrati solo se la funzione è chiamata da un altro file di python senza che sia attiva.
        if self._is_gff3:
            for operation in self._operations.values():
                with patch('builtins.print'):
                    operation[0]()
            return list(self._active_operations.keys())
        else: print('no active operation')
    
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
        #!!!!!!!!!!!!!!!there is an error in the input that prevents to correctly label the types
        information = {}
        for column_name in self._df.columns:
            information[column_name] = self._df[column_name].dtype

        return Dataset(pd.DataFrame({'columns':information.keys(), 'data_type':information.values()}))

    @activate
    def unique_seq_IDs(self) -> 'Dataset':
        '''
        obtaining the list of unique sequence IDs available in the dataset
        '''
        return Dataset(pd.DataFrame({'unique_IDs':self._df.Seqid.unique()}))

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

        self.get_active_operations() #to update self._active_operations
        operation_types = list(set([value[1] for value in list(self._active_operations.values())]))
        return Dataset(pd.DataFrame({'operation_types':operation_types}))

    @activate
    def same_source(self) -> 'Dataset':
        '''
        counting the number of features provided by the same source
        '''
        return Dataset(self._df.Source.value_counts().to_frame())

    @activate
    def entries_for_each_type_of_operation(self) -> 'Dataset':
        '''
        counting the number of entries for each type of operation
        '''
        self.get_active_operations() #to update self._active_operations
        entries_for_op_types = {}
        for operation_name, operation_and_type in self._active_operations.items():
            type_ = operation_and_type[1]
            if type_ in entries_for_op_types.keys():
                entries_for_op_types[type_].append(operation_name)
            else:
                entries_for_op_types[type_] = [operation_name]
        return Dataset(pd.DataFrame({'operation_types':entries_for_op_types.keys(),'entries':entries_for_op_types.values()}))

    @activate
    def get_chromosomes(self) -> 'Dataset':
        '''
        deriving a new dataset containing only the information about entire chromosomes. Entries with entirechromosomes comes from source GRCh38
        '''
        return Dataset(self._df[self._df.Source == 'GRCh38'])

    @activate
    def fraction_of_unassembled_seq(self) -> 'Dataset':
        '''
        calculating the fraction of unassembled sequences from source GRCh38. Hint: unassembled sequences are of type supercontig while the others are of type chromosome
        '''
        chromosomes = self.get_chromosomes()._df
        fraction = len(chromosomes[chromosomes.Type == 'supercontig'].index) / len(chromosomes.index)
        return Dataset(pd.DataFrame({'fraction of unassembled sequences': fraction},index=[0]))

    @activate
    def ensembl_havana(self) -> 'Dataset':
        '''
        obtaining a new dataset containing only entries from source ensembl, havana and ensembl_havana
        '''
        return Dataset(self._df[(self._df.Source == 'ensembl') | (self._df.Source == 'havana') | (self._df.Source == 'ensembl_havana')])

    @activate
    def entries_for_each_type_of_operation_ensemblhavana(self) -> 'Dataset':
        '''
        counting the number of entries for each type of operation for the dataset containing only entries from source ensembl, havana and ensembl_havana
        '''
        #this operation is useless in our program because the active operations are checked depending on the input
        return self.entries_for_each_type_of_operation()

    @activate
    def get_gene_names(self) -> 'Dataset':
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
        return Dataset(pd.DataFrame({'Name':names}))