def activate(operation):
    '''
    this is a decorator, it checks if an operation can be labelled as active
    '''
    def check(self,*args,**kwargs):
        if operation.__name__ not in self._active_operations.keys():
            #if the operation is not active we have to check if its execution creates any problem
            try:
                output = operation(self,*args,**kwargs) #take the output of the operation
                if not output.get_df().empty: #check if the output is empty
                    self._active_operations[operation.__name__] = self._operations[operation.__name__]
                    return output
                else:
                    #if the function returns no output we do not add it to the active operations
                    #or is it better to add it?
                    print(f'The operation {operation.__name__} has produced no results')
            except:
                #if the function creates a problem we do not add it to the active operations
                print(f'The operation {operation.__name__} operation is not active on this object')
        else:
            #if the operation is active we just execute it
            output = operation(self,*args,**kwargs)
            return output
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