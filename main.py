from dataset_reader import GFF3DatasetReader
from dataset import Dataset

filepath='Homo_sapiens.GRCh38.85.gff3.gz'
reader = GFF3DatasetReader()
human_genome = reader.read(filepath)

print(human_genome.df.head())
print(human_genome.df.shape)
print()
print()

general_info = human_genome.get_information()
print(general_info.df.head(9))
print()
print()

sequence_IDs = human_genome.unique_seq_IDs()
print(sequence_IDs.df.head())
print(sequence_IDs.df.shape)
print()
print()

sources=['GRCh38', 'havana', 'mirbase', 'ensembl_havana', 'ensembl', 'insdc']
for i in sources:
    same_source = human_genome.features_with_same_source(i)
    print(same_source.df.head())
    print()

chromosomes = human_genome.get_chromosomes()
print(chromosomes.df.head())
print(chromosomes.df.shape)
print()
print()

subset = human_genome.ensembl_havana()
print(subset.df.head())
print(subset.df.shape)
print()
print()

gene_names = human_genome.get_gene_names()
print(gene_names.df.head())
print(gene_names.df.shape)