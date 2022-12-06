import numpy as np
import pandas as pd

class superclassofdatasetreaders():
    '''
    general abstract interface that defines the procedure that a datasetreader is provided with
    '''
    def read():
        pass

class GFF3reader(superclassofdatasetreaders):
    '''
    specific for GFF3 files, it should be compliant with a general abstract interface
    returns a dataset object as output that is a wrapper around a Pandas DataFrame 
    '''
    def read():
        pass

class Dataset():
    '''
    output object of GFF3reader
    it is a wrapper around a pandas dataframe
    '''
    pass