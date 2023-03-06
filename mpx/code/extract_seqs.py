# Extract seqs from a fasta file based on the metadata in a tab-delimited file and write them to a new fasta file.
# Usage: python3 extract_seqs.py <fasta> <tab-delimited> <column> <value>

import sys
import pandas as pd
from Bio import SeqIO

fasta = sys.argv[1]
# Read in the tab-delimited file
df = pd.read_csv(sys.argv[2], sep='\t')
reference_seq_file = sys.argv[3]

# Read in the fasta file
records = SeqIO.parse(fasta, 'fasta')
# extract all accesion ids into a list from the metadata file.
accession_ids = df['accession'].tolist()
# extract all seqs from the fasta file that match the accession ids in the metadata file.
extracted_records = [record for record in records if record.id.split('|')[0].strip() in accession_ids]
# write the extracted seqs to a new fasta file.
SeqIO.write(extracted_records, 'extracted_seqs.fasta', 'fasta')

# format date column in metadata file
df['date'] = df['date'].apply(lambda x: x.split(' ')[0])
# read reference sequence from fasta file
with open(reference_seq_file, 'r') as f:
    # extract the accession id and date from the fasta header (format >accession_id|date)
    ref_seq, date = f.readline()[1:].strip().split('|')
# add reference sequence to the metadata file
df = pd.concat([df, pd.DataFrame({'strain': ref_seq, 'accession': ref_seq, 'date': date}, index=[0])])
# write the formatted metadata file to a new file
df.to_csv('formatted_metadata.tsv', sep='\t', index=False)
