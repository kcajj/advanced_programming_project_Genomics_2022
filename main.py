from dataset_reader import GFF3DatasetReader
from dataset import Dataset

filepath='Homo_sapiens.GRCh38.85.gff3.gz'
reader = GFF3DatasetReader()
human_genome = reader.read(filepath)

print(human_genome.df.head())
print(human_genome.df.shape)

general_info = human_genome.get_information()
print(general_info.df.head(9))

sequence_IDs = human_genome.unique_seq_IDs()
print(sequence_IDs.df.head(27))
print(sequence_IDs.df.shape)