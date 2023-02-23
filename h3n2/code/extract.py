# extract sequences from fasta file
# usage: python extract.py <fasta file> <file contating list of files>
# output: fasta file with sequences extracted

import sys
from Bio import SeqIO
import pandas as pd
from tqdm import tqdm
tqdm.pandas()

# read in fasta file
# fasta_file = '/home/praneeth/Scripps/Andersen_lab/freyja_pathogens/h3n2_ha/combined_seqs_clean.fasta'
fasta_file = sys.argv[1]
# read in list of sequences to extract
# extract_file = '/home/praneeth/Scripps/Andersen_lab/freyja_pathogens/h3n2_ha/nextstrain_flu_seasonal_h3n2_ha_2y_acknowledgements.tsv'
extract_file = sys.argv[2]
# read in fasta file
fasta_sequences = SeqIO.parse(open(fasta_file),'fasta')
# read in list of sequences to extract
extract_list = pd.read_csv(extract_file, header=0, sep='\t')
# create a dataframe with the sequences and complete sequence names
fasta_sequences_df = pd.DataFrame(columns=['complete_seq_name', 'trimmed_seq_name'])
fasta_sequences_df['complete_seq_name'] = [str(seq.id) for seq in fasta_sequences]
fasta_sequences_df['trimmed_seq_name'] = fasta_sequences_df['complete_seq_name'].apply(lambda x: x.split('|')[0])

# fuzzy match sequences names using Lexical Matching
# https://stackoverflow.com/questions/17388213/find-the-closest-string-match

from difflib import SequenceMatcher

def lexical_match(a, b):
    return SequenceMatcher(None, a, b).ratio()

# process fuzzy match using dataframes and apply function
def fuzzy_match(seq, seq_list, rank):
    # initialize dataframe
    df = pd.DataFrame(columns=['seq_list', 'match'])
    # add sequences to dataframe
    df['seq_list'] = seq_list
    # add match column
    df['match'] = df['seq_list'].apply(lambda x: lexical_match(seq, x))
    # return sequence with highest match + rank
    return df.sort_values(by='match', ascending=False)['seq_list'].values[rank-1]

def get_fasta_names(seq, rank=1):
    seq_id = fuzzy_match(seq, list(fasta_sequences_df['trimmed_seq_name'].values), rank)
    return fasta_sequences_df[fasta_sequences_df['trimmed_seq_name'] == seq_id]['complete_seq_name'].values[0]

def add_row_number_to_EPI_ID(seq, number):
    seq_name = seq.split('|')
    seq_name[1] = seq_name[1] + '_' + str(number)
    return '|'.join(seq_name)

extracted_sequences_names = pd.DataFrame(columns=['trimmed_seq_name', 'complete_seq_name'])
extracted_sequences_names['trimmed_seq_name'] = extract_list['strain'].values

# split dataframe into chunks and use multiprocess to speed up process
# https://stackoverflow.com/questions/26520781/apply-function-to-each-row-in-a-pandas-dataframe-using-multiprocessing

import multiprocessing

# split dataframe into chunks
# https://stackoverflow.com/questions/26520781/apply-function-to-each-row-in-a-pandas-dataframe-using-multiprocessing

def split_dataframe(df, chunk_size):
    num_chunks = len(df) // chunk_size + 1
    return np.array_split(df, num_chunks)

num_of_cores = multiprocessing.cpu_count()

# create a pool of workers based on the number of cores
pool = multiprocessing.Pool(processes=num_of_cores*2)
# split dataframe into chunks
chunks = split_dataframe(extracted_sequences_names, 1000)
# apply function to each chunk
extracted_sequences_names['complete_seq_name'] = pd.concat(pool.map(lambda x: x.progress_apply(lambda y: get_fasta_names(y['trimmed_seq_name']), axis=1), chunks))
# close pool
pool.close()
pool.join()

# extracted_sequences_names['complete_seq_name'] = extracted_sequences_names['trimmed_seq_name'].progress_apply(get_fasta_names)

# check if the total number of duplicate sequences is less than 1% of the total number of sequences
# sum all value counts greater than 1
extracted_sequences_names.to_csv('extracted_sequences_temp.tsv', sep='\t', index=False)
# if sum(extracted_sequences_names['complete_seq_name'].value_counts() > 1) > 0.01 * len(extracted_sequences_names):
#     raise Exception('More than 1% of the sequences are duplicates. Please check the sequences names and try again.')
# else:
#     extracted_sequences_names['complete_seq_name'] = extracted_sequences_names.progress_apply(lambda x: add_row_number_to_EPI_ID(x['complete_seq_name'], x.name) if extracted_sequences_names['complete_seq_name'].value_counts()[x['complete_seq_name']] > 1 else x['complete_seq_name'], axis=1)

extracted_sequences_names['complete_seq_name'] = extracted_sequences_names.progress_apply(lambda x: add_row_number_to_EPI_ID(x['complete_seq_name'], x.name) if extracted_sequences_names['complete_seq_name'].value_counts()[x['complete_seq_name']] > 1 else x['complete_seq_name'], axis=1)


# find duplicates and replace with second highest match
# extracted_sequences_names['complete_seq_name'] = extracted_sequences_names['complete_seq_name'].progress_apply(lambda x: get_fasta_names(x, 2) if extracted_sequences_names['complete_seq_name'].value_counts()[x] > 1 else x)
# save extracted sequences names to file
extracted_sequences_names.to_csv('extracted_sequences.tsv', sep='\t', index=False)

extracted_sequences_names['EPI_ID'] = extracted_sequences_names['complete_seq_name'].apply(lambda x: x.split('|')[1])

is_accepted_sequence = False

with open(fasta_file, 'r') as f:
    # open file to write to
    with open('extracted_sequences.fasta', 'w') as g:
        tqdm_f = tqdm(f.readlines(), bar_format='{l_bar}{bar:30}{r_bar}{bar:-30b}', desc='Removing duplicates from fasta file...')
        for line in tqdm_f:
            # if line is a header
            if line[0] == '>':
                # if name is not in list
                if line.split('|')[1] in extracted_sequences_names['EPI_ID'].values:
                    # write header to file
                    g.write(line)
                    is_accepted_sequence = True
                # if name is in list
                else:
                    # skip header
                    is_accepted_sequence = False
                    continue
            # if line is a sequence
            elif is_accepted_sequence:
                # write sequence to file
                g.write(line)
