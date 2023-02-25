import sys
import pandas as pd

# Replace fasta headers with the 'strain' column of a tab-delimited file.
# Usage: python3 rename.py <fasta> <tab-delimited>

fasta = sys.argv[1]
# Read in the tab-delimited file
df = pd.read_csv(sys.argv[2], sep='\t')

# Read in the fasta file
with open(fasta, 'r') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith('>'):
            # Get the strain name from the tab-delimited file
            try:
                strain = df.loc[df['accession'] == line[1:].strip(), 'strain'].values[0]
            except IndexError:
                print('No strain name found for accession id: {}'.format(line[1:].strip()))
                continue
            # Replace the fasta header
            lines[i] = '>' + strain + '\n'
# Write the new fasta file
with open(fasta, 'w') as f:
    f.writelines(lines)
