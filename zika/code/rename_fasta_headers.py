# Rename fasta by splitting the header by a delimiter and taking the first part and write to a new file.
# Usage: python3 rename_fasta.py -i input.fasta -o output.fasta -d delimiter

import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Rename fasta by splitting the header by a delimiter and taking the first part and replacing the header with the first part')
parser.add_argument('-i', '--input', help='Input fasta file', required=True)
parser.add_argument('-o', '--output', help='Output fasta file', required=True)
parser.add_argument('-d', '--delimiter', help='Delimiter to split the header by', required=True)
args = parser.parse_args()

# Open as a text file
with open(args.input, 'r') as input_file:
    with open(args.output, 'w') as output_file:
        for line in tqdm(input_file, desc='Renaming headers: '):
            if line.startswith('>'):
                # Split the header by the delimiter and take the first part
                header = line.split(args.delimiter)[0]
                output_file.write(header + '\n')
            else:
                output_file.write(line)
