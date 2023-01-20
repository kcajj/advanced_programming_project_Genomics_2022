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