# clean fasta file by removing duplicated sequences
# Path: h3n2_ha/code/clean_fasta.py

import sys
from tqdm import tqdm

fasta_seqs = sys.argv[1]
fasta_seqs_clean = sys.argv[2]

clean_fasta_names = []

is_accepted_sequence = False

with open(fasta_seqs, 'r') as f:
    # open file to write to
    with open(fasta_seqs_clean, 'w') as g:
        tqdm_f = tqdm(f.readlines(), bar_format='{l_bar}{bar:30}{r_bar}{bar:-30b}', desc='Removing duplicates from fasta file...')
        for line in tqdm_f:
            # if line is a header
            if line[0] == '>':
                # if name is not in list
                if line[1:] not in clean_fasta_names:
                    # add name to list
                    clean_fasta_names.append(line[1:])
                    # write header to file
                    g.write(line)
                    is_accepted_sequence = True
                # if name is in list
                else:
                    is_accepted_sequence = False
                    # skip header
                    continue
            # if line is a sequence
            elif is_accepted_sequence:
                # write sequence to file
                g.write(line)
