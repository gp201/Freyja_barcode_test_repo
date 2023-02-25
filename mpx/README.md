# H3N2 HA pathogen build

Nextstrain tree: https://nextstrain.org/monkeypox/hmpxv1

## Data sources
 - Nextstrain

Download the data.nextstrain.org/files/workflows/monkeypox/alignment.fasta.xz, data.nextstrain.org/files/workflows/monkeypox/metadata.tsv.gz and the tree in newick format from the nextstrain tree.

Ensure the reference seq information (Name and Colelction date) is also present in the metadatafile


## Data processing

1) Simply run the following command:
    ```console
    bash preprocess.sh
    ```
2) Go to the freyja_pathogen_workflow folder and run the bash command that is printed.
    ```console
    cd ../
    ```
