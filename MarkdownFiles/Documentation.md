# Documentation

The project consists in a web application that is able to manipulate a GFF3 dataset ('Homo_sapiens.GRCh38.85.gff3.gz') that contains all of the features of the human genome.

The backend script is written in python, 4 different modules interact together to allow the correct reading and handling of the dataset.
The user interface is implemented through flask, it allows to use all of the functionalities of the application and to have a deep view of software design.

## software analysis



## software design
broad view fo the software, with interaction between classes

UML diagram

each class described deeply

### Dataset Reader
#### This is the documentation of the module dataset_reader.py

We start by importing from the module **abc** the class **ABC** and the method **abstractmethod**. Subsequently we import two libraries:
- **numpy** as *np*
- **pandas** as *pd*
Lastly we import the class **DataSet** from the module **dataset**

We also find a total of two classes:

##### -  DatasetReader: 
The **DatasetReader** class is an abstract class that defines the interface for reading dataset files. 

###### Methods:
- **read**: is an abstract method that must be implemented by subclasses to define how to read a dataset file. 

##### -  GFF3DatasetReader: 
The **GFF3DatasetReader** class is is a subclass of *DatasetReader* that is specifically designed to read GFF3 files, it should be compliant with a general abstract interface. It returns a dataset object as output that is a wrapper around a Pandas DataFrame.

###### Methods:
- **read**: it reads a GFF3 file and returns a *Dataset* object.
            The method first checks if the file has the **.gff3.gz** extension. If it does not, a *ValueError* is raised with the message **"Invalid file type. Expected .gff3.gz file."**
            The method then uses the *pd.read_csv* function from the Pandas library to read the GFF3 file. 


#### implementation
maybe some information about the code used to write the class?

### Dataset
#### This is the documentation of the module dataset.py

We start by importing two libraries:
- **numpy** as *np*
- **pandas** as *pd*
Subsequently from the submodule **mock** of the module **unittest** we import the variable **patch**. Lastly from the module **functions** we import two functions, **get_attributes** and **activate**.

Again we find two classes:

##### - Dataset:
The **Dataset** class provides a view over the data. It is used to distinguish between a generic tabular data and GFF3 data, which is a special case.

###### Properties:
-  **df** the data representation in the form of a Pandas dataframe
- **active_operations** a dictionary of **active** operations
- **operations** a dictionary of **avaible** operations


###### Methods:
- **create**: it returns a new instance of *GFF3Dataset* if the data frame's columns match the format ('Seqid','Source','Type','Start','End','Score','Strand','Phase','Attribute'), otherwise returns self.

- **get_df**: it returns the internal data frame.

- **get_active_operations**: it returns all active operations. It is used to show the user the oepration that he can use. 

##### - GFF3Dataset:
The **GFF3Dataset** class is a subclass of *Dataset*. It provides several operations that can be performed on GFF3 data.

###### Properties:
-  **df** the data representation in the form of a Pandas dataframe
- **active_operations** a dictionary of **active** operations
- **operations** a dictionary of **avaible** operations

###### Methods:
- **information**: it returns basic information about the dataset: name and data type of each column.

- **unique_sequence_IDs**: it returns a list of unique sequence IDs available in the dataset.

- **unique_types**: it returns a list of unique types of operations available in the dataset.

- **same_source**: it counts the number of **features** provided by the same source.

- **entries_for_each_type**: it counts the number of **entries** for each type of operation.

- **chromosomes**: it derives a new dataset containing only the information about entire chromosomes. Entries with entirechromosomes comes from source **GRCh38**.

- **fraction_of_unassembled_sequences**: it returns the fraction of unassembled sequences in the dataset.

- **ensembl_havana**: it returns a new dataset containing only entries from source **ensembl**, **havana** and **esembl_havana**.

- **entries_for_each_type_ensemblhavana**: it counts the number of entries for each type of operation for the dataset containing only entries from source **ensembl**, **havana** and **ensembl_havana**

- **gene_names**: it returns the gene names from the dataset containing containing only entries from source **ensembl**, **havana** and **ensembl_havana**.


#### implementation
maybe some information about the code used to write the class?
