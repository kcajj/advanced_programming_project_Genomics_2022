from dataset_reader import GFF3DatasetReader

filepath='Homo_sapiens.GRCh38.85.gff3.gz'
reader = GFF3DatasetReader()
human_genome = reader.read(filepath)

print(human_genome.get_df().head())
print(human_genome.get_df().shape)
print()
print()

general_info = human_genome.get_information()
print(general_info.get_df().head(9))
print()
print()

output = general_info.get_df()
print(output.columns[0])
for index,value in output.iterrows():
    print(index, value[0])
print()
print()

sequence_IDs = human_genome.unique_seq_IDs()
print(sequence_IDs.get_df().head())
print(sequence_IDs.get_df().shape)
print()
print()

same_source = human_genome.same_source()
print(same_source.get_df().head())
print(same_source.get_df().shape)
print()
print()

chromosomes = human_genome.get_chromosomes()
print(chromosomes.get_df().head())
print(chromosomes.get_df().shape)
print()
print()

fraction = human_genome.fraction_of_unassembled_seq()
print(fraction.get_df().head())
print(fraction.get_df().shape)
print()
print()

subset = human_genome.ensembl_havana()
print(subset.get_df().head())
print(subset.get_df().shape)
print()
print()

gene_names = human_genome.get_gene_names()
print(gene_names.get_df().head())
print(gene_names.get_df().shape)
print()
print()

types = human_genome.type_of_operations()
print(types.get_df().head())
print(types.get_df().shape)
print()
print()

entries_for_types = human_genome.entries_for_each_type_of_operation()
print(entries_for_types.get_df().head())
print(entries_for_types.get_df().shape)
print()
print()

entries_for_types_ensemblehavana = human_genome.entries_for_each_type_of_operation_ensemblhavana()
print(entries_for_types_ensemblehavana.get_df().head())
print(entries_for_types_ensemblehavana.get_df().shape)
print()
print()