import numpy as np
import pandas as pd
from unittest.mock import patch

class Dataset():
    '''
    A dataset is the view over the data. As for the reader the software must distinguish
    between a generic tabular data and GFF3 data, which is a peculiar case.
    '''
    def __init__(self, df: pd.DataFrame) -> None:
        self.__df = df
        self.__is_gff3 = False
        if self.__df.columns.format() == ['Seqid','Source','Type','Start','End','Score','Strand','Phase','Attribute']:
            self.__is_gff3 = True
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
    
    def get_df(self) -> pd.DataFrame: #from the other modules, this has to be the only way to access the pandas dataframe that is inside the dataset class
        return self.__df

    def __activate(operation):
        '''
        this is a decorator, it checks if an operation can be labelled as active
        '''
        def check(self,*args,**kwargs):
            if (self.__is_gff3) and (operation.__name__ not in self.__active_operations.keys()):
                #if the dataset is GFF3 and the operation is not active we have to check if its execution 
                #does not create problems and if it returns some information and then we can activate it
                try:
                    output = operation(self,*args,**kwargs)
                    if not output.__df.empty: #if the operation returns some information it is activated
                        self.__active_operations[operation.__name__] = self.__operations[operation.__name__]
                        return output
                    else:
                        print(f'The operation {operation.__name__} has produced no results')
                except: #if the execution returns an exception the operation is not activated
                    #se la funzione è stata chiamata dal metodo get active operations questa riga non deve essere eseguita
                    print(f'The operation {operation.__name__} operation is not active on this object')
                    #we could also add the operation to an (inactive register)

            elif self.__is_gff3: #if the dataset is GFF3 and the operation is already active we can execute it
                output = operation(self,*args,**kwargs)
                return output
            else:
                pass #if the dataset is not a GFF3 file we are not interested in performing operations
        return check

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
        for operation in self.__operations.values():
            with patch('builtins.print'):
                operation[0]()
        return list(self.__active_operations.keys())
    
    '''
    By means of a dataset object a number of insights over data can be obtained; each insight
    is called an operation.
    '''
    #operations down here
    @__activate
    def get_information(self) -> 'Dataset':
        '''
        getting some basic information about the dataset. The basic information are the name and data type ofeach column
        '''
        #!!!!!!!!!!!!!!!there is an error in the input that prevents to correctly label the types
        information = {}
        for column_name in self.__df.columns:
            information[column_name] = self.__df[column_name].dtype

        return Dataset(pd.DataFrame({'columns':information.keys(), 'data_type':information.values()}))

    @__activate
    def unique_seq_IDs(self) -> 'Dataset':
        '''
        obtaining the list of unique sequence IDs available in the dataset
        '''
        return Dataset(pd.DataFrame({'unique_IDs':self.__df.Seqid.unique()}))

    @__activate
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

        self.get_active_operations() #to update self.__active_operations
        operation_types = list(set([value[1] for value in list(self.__active_operations.values())]))
        return Dataset(pd.DataFrame({'operation_types':operation_types}))

    @__activate
    def same_source(self) -> 'Dataset':
        '''
        counting the number of features provided by the same source
        '''
        return Dataset(self.__df.Source.value_counts().to_frame())

    @__activate
    def entries_for_each_type_of_operation(self) -> 'Dataset':
        '''
        counting the number of entries for each type of operation
        '''
        self.get_active_operations() #to update self.__active_operations
        entries_for_op_types = {}
        for operation_name, operation_and_type in self.__active_operations.items():
            type_ = operation_and_type[1]
            if type_ in entries_for_op_types.keys():
                entries_for_op_types[type_].append(operation_name)
            else:
                entries_for_op_types[type_] = [operation_name]
        return Dataset(pd.DataFrame({'operation_types':entries_for_op_types.keys(),'entries':entries_for_op_types.values()}))

    @__activate
    def get_chromosomes(self) -> 'Dataset':
        '''
        deriving a new dataset containing only the information about entire chromosomes. Entries with entirechromosomes comes from source GRCh38
        '''
        return Dataset(self.__df[self.__df.Source == 'GRCh38'])

    @__activate
    def fraction_of_unassembled_seq(self) -> 'Dataset':
        '''
        calculating the fraction of unassembled sequences from source GRCh38. Hint: unassembled sequences are of type supercontig while the others are of type chromosome
        '''
        chromosomes = self.get_chromosomes().__df
        fraction = len(chromosomes[chromosomes.Type == 'supercontig'].index) / len(chromosomes.index)
        return Dataset(pd.DataFrame({'fraction of unassembled sequences': fraction},index=[0]))

    @__activate
    def ensembl_havana(self) -> 'Dataset':
        '''
        obtaining a new dataset containing only entries from source ensembl, havana and ensembl_havana
        '''
        return Dataset(self.__df[(self.__df.Source == 'ensembl') | (self.__df.Source == 'havana') | (self.__df.Source == 'ensembl_havana')])

    @__activate
    def entries_for_each_type_of_operation_ensemblhavana(self) -> 'Dataset':
        '''
        counting the number of entries for each type of operation for the dataset containing only entries from source ensembl, havana and ensembl_havana
        '''
        #this operation is useless in our program because the active operations are checked depending on the input
        return self.entries_for_each_type_of_operation()

    @__activate
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