# extract dates from fasta names
# usage: python extract_dates.py <fasta file> <output file>

import sys
import pandas as pd
from tqdm import tqdm
from Bio.SeqIO.FastaIO import SimpleFastaParser

# read in fasta file
fasta_file = sys.argv[1]
output_file = sys.argv[2]

# extract dates from fasta names
dates = {}
with open(fasta_file, 'r') as handle:
    for values in tqdm(SimpleFastaParser(handle), desc='Extracting dates'):
        name, sequence = values
        date = name.split('|')[-1]
        dates[name] = date

# write out dates
dates = pd.DataFrame.from_dict(dates, orient='index').reset_index()
dates.columns = ['strain', 'date']
dates.to_csv(output_file, sep='\t', index=False, header=True)
