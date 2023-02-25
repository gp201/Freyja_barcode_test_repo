# combine the dates file with the lineages file
# usage: python combine_dates_lineages.py <dates file> <lineages file> <output file>
#
import sys
import pandas as pd

# read in dates file
dates_file = sys.argv[1]
dates = pd.read_csv(dates_file, sep='\t')

# read in lineages file
lineages_file = sys.argv[2]
lineages = pd.read_csv(lineages_file, sep='\t')

# combine dates and lineages
combined = pd.merge(dates, lineages, on='strain', how='inner')

# write out combined file
combined.to_csv(sys.argv[3], sep='\t', index=False, header=True)

# print number of sequences in combined file
print('Number of sequences in combined file: ' + str(len(combined)))

# print number of sequences in dates file
print('Number of sequences in dates file: ' + str(len(dates)))

# print number of sequences in lineages file
print('Number of sequences in lineages file: ' + str(len(lineages)))
