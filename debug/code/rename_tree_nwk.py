import dendropy
import sys
from tqdm import tqdm
import pandas as pd

tree_file = sys.argv[1]
mapping_file = sys.argv[2]
fasta_file = sys.argv[3]

# tree_file = '/home/praneeth/Scripps/Andersen_lab/freyja_pathogens/h3n2_ha/nextstrain_flu_seasonal_h3n2_ha_2y_timetree.nwk'
# mapping_file = '/home/praneeth/Scripps/Andersen_lab/freyja_pathogens/h3n2_ha/extracted_sequences_names_2.tsv'
# fasta_file = '/home/praneeth/Scripps/Andersen_lab/freyja_pathogens/h3n2_ha/combined_seqs_clean.fasta'

# print dendropy version
print(dendropy.__version__)
# print dendropy location
print(dendropy.__file__)

# read in tree
tree = dendropy.Tree.get(path=tree_file, schema='newick', suppress_leaf_node_taxa=False, suppress_internal_node_taxa=True, case_sensitive_taxon_labels=True, preserve_underscores=True)

# read in mapping file
mapping_df = pd.read_csv(mapping_file, header=0, sep='\t')


tqdm_leaf_nodes = tqdm(tree.leaf_nodes(), bar_format='{l_bar}{bar:30}{r_bar}{bar:-30b}', desc='Renaming leaf nodes...')

# rename fasta headers and tree leaf nodes
# use the saved mapping file to rename the fasta headers

# rename leaf nodes
failed_seqs = []
for leaf in tqdm_leaf_nodes:
    try:
        leaf.taxon.label = mapping_df[mapping_df['trimmed_seq_name'] == leaf.taxon.label]['complete_seq_name'].values[0].split('|')[1]
    except IndexError:
        # drop leaf node
        failed_seqs.append(leaf.taxon.label)
        tree.prune_taxa_with_labels([leaf.taxon.label])

# print failed sequences
print('Failed sequences: ', failed_seqs)

# write out tree
tree.write(path='nextstrain_flu_seasonal_h3n2_ha_2y_timetree_renamed.nwk',
           schema='newick')

# TODO-GP: rename fasta headers.

# clean fasta file by removing duplicated sequences
# Path: h3n2_ha/code/clean_fasta.py

with open(fasta_file, 'r') as f:
    # open file to write to
    with open('extracted_sequences_renamed.fasta', 'w') as g:
        tqdm_f = tqdm(f.readlines(), bar_format='{l_bar}{bar:30}{r_bar}{bar:-30b}', desc='Renaming fasta headers...')
        for line in tqdm_f:
            # if line is a header
            if line[0] == '>':
                # replace the header with the EPI_ID
                line = '>' + line.split('|')[1] + '\n'
            g.write(line)
