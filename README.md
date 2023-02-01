# Advanced programming project - Genomics 2023
final project of the advanced programming classes, course of Genomics bachelor degree - UniBo.

you can find the project specification [here](MarkdownFiles/Project_specification.md)

you can find the documentation [here](MarkdownFiles/Documentation.md)


we could make our modules available for download on pip, in this way users can use our code on other datasets.
to do so we have to upload our packages on python package index(PyPI)

problems of main branch:
specificity for gff3 files is not so evident (with the gff3 subclass this is solved)
activation of operations is not so pretty (actually a junky operation allows to automate the activation, and the active operations list)
with this design the operation to retrive the entries for operation types of ensemblhavana is useless (who cares?)
operation types are not well defined

problems with GFF3 branch:
same as above but there is a specific subclass for the gff3 datasets.
each time a dataset object is created the crate() method is needed


todo:
- PyPI upload
- uml (giulia) crc cards
- documentation
- graphics
- flask
- html
- css