def activate(operation):
    '''
    this is a decorator, it checks if an operation can be labelled as active
    '''
    def check(self,*args,**kwargs):
        if (self._is_gff3) and (operation.__name__ not in self._active_operations.keys()):
            #if the dataset is GFF3 and the operation is not active we have to check if its execution 
            #does not create problems and if it returns some information and then we can activate it
            try:
                output = operation(self,*args,**kwargs)
                if not output._df.empty: #if the operation returns some information it is activated
                    self._active_operations[operation.__name__] = self._operations[operation.__name__]
                    return output
                else:
                    print(f'The operation {operation.__name__} has produced no results')
            except: #if the execution returns an exception the operation is not activated
                #se la funzione è stata chiamata dal metodo get active operations questa riga non deve essere eseguita
                print(f'The operation {operation.__name__} operation is not active on this object')
                #we could also add the operation to an (inactive register)

        elif self._is_gff3: #if the dataset is GFF3 and the operation is already active we can execute it
            output = operation(self,*args,**kwargs)
            return output
        else:
            pass #if the dataset is not a GFF3 file we are not interested in performing operations
            #actually the get_information and operation types could be available
    return check

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