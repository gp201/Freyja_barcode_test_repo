# H3N2 HA pathogen build

Nextstrain tree: https://nextstrain.org/flu/seasonal/h3n2/ha/2y

## Data sources
 - GISAID

Make sure to download all the ha sequences from 2013 till the latest date.
The fasta header should be of the following format:
```
Isolate name | Isolate ID | Collection date
```

## Data processing

1) Simply run the following command:
    ```console
    bash preprocess.sh
    ```
2) Go to the freyja_pathogen_workflow folder and run the bash command that is printed.
    ```console
    cd ../
    ```



.
├── code
│   ├── clean_fasta.py
│   ├── clean_lineages.py
│   ├── extract_dates.py
│   ├── extract.py
│   ├── generate_metadata_file.py
│   └── rename_tree_nwk.py
├── config
│   └── conda_environment.yml
├── gisaid_seqs
│   ├── gisaid_epiflu_sequence (1).fasta
│   ├── gisaid_epiflu_sequence (2).fasta
│   ├── gisaid_epiflu_sequence (3).fasta
│   ├── gisaid_epiflu_sequence (4).fasta
│   ├── gisaid_epiflu_sequence.fasta
│   └── README
├── nextstrain_flu_seasonal_h3n2_ha_2y_acknowledgements.tsv
├── nextstrain_flu_seasonal_h3n2_ha_2y_timetree.nwk
├── preprocess.sh
├── README.md
└── reference_seq.fasta

3 directories, 18 files
