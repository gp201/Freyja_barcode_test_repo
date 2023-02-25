# Clean lineages file

import sys
import pandas as pd

# read in lineages file
lineages_file = sys.argv[1]
lineages = pd.read_csv(lineages_file, sep='\t', names=['strain', 'lineage'])

# format column 2
lineages['lineage'] = lineages['lineage'].str.split(',').str[-1].str.strip()


# write out lineages file
lineages.to_csv('clean_lineages.tsv', sep='\t', index=False, header=True)
