from dataset_reader import GFF3DatasetReader

filepath='Homo_sapiens.GRCh38.85.gff3.gz'
reader = GFF3DatasetReader()
human_genome = reader.read(filepath)

print(human_genome.get_df().head())
print(human_genome.get_df().shape)
print()
print(human_genome.get_active_operations())
print()

general_info = human_genome.get_information()
print(general_info.get_df().head(9))
print()
print(general_info.get_active_operations())
print()

sequence_IDs = human_genome.unique_seq_IDs()
print(sequence_IDs.get_df().head())
print(sequence_IDs.get_df().shape)
print()
print(sequence_IDs.get_active_operations())
print()

same_source = human_genome.same_source()
print(same_source.get_df().head())
print(same_source.get_active_operations())
print()

chromosomes = human_genome.get_chromosomes()
print(chromosomes.get_df().head())
print(chromosomes.get_df().shape)
print()
print(chromosomes.get_active_operations())
print()

fraction = human_genome.fraction_of_unassembled_seq()
print(fraction.get_df().head())
print(fraction.get_df().shape)
print()
print(fraction.get_active_operations())
print()

subset = human_genome.ensembl_havana()
print(subset.get_df().head())
print(subset.get_df().shape)
print()
print(subset.get_active_operations())
print()

gene_names = human_genome.get_gene_names()
print(gene_names.get_df().head())
print(gene_names.get_df().shape)
print()
print(gene_names.get_active_operations())
print()