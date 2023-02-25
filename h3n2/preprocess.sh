# exit when any command fails
set -e
# print each command before executing
set -x

# # ENV name
# RUN_ENV=freyja-h3n2-pathogen

# if { conda env list | grep $RUN_ENV; } >/dev/null 2>&1; then 
#     echo "Updaing conda env $RUN_ENV"
#     eval "$(conda shell.bash hook)"
#     conda env update -name $RUN_ENV -f env/conda_environment.yml
# else
#     echo "Installing conda env $RUN_ENV"
#     eval "$(conda shell.bash hook)"
#     conda env create -f env/conda_environment.yml
# fi

# eval "$(conda shell.bash hook)"
# conda activate $RUN_ENV

# download sequences from GISAID with the EPI_ID
cat gisaid_seqs/*.fasta > combined_seqs.fasta
python3 code/clean_fasta.py combined_seqs.fasta combined_seqs_clean.fasta
python3 code/extract.py combined_seqs_clean.fasta nextstrain_flu_seasonal_h3n2_ha_2y_acknowledgements.tsv
python3 code/rename_tree_nwk.py nextstrain_flu_seasonal_h3n2_ha_2y_timetree.nwk extracted_sequences.tsv extracted_sequences.fasta

# get the lineages
git clone https://github.com/nextstrain/seasonal-flu.git
cd seasonal-flu
python3 assign_clades.py --sequences ../extracted_sequences_renamed.fasta --lineage h3n2 > ../lineages.tsv
cd ..
python3 code/clean_lineages.py lineages.tsv
python3 code/extract_dates.py extracted_sequences_renamed.fasta dates.tsv
python3 code/generate_metadata_file.py dates.tsv clean_lineages.tsv metadata.tsv

# get current directory and place it in a variable
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Clone the Freyja pathogen workflow
git clone https://github.com/gp201/Freyja_pathogen_workflow.git
cd Freyja_pathogen_workflow

eval "$(conda shell.bash hook)"
conda deactivate

# print and run the below command

bash run_nf.sh $DIR/ $DIR/extracted_sequences_renamed.fasta $DIR/metadata.tsv --strain_column "strain" --skip_clade_annotations true --align_to_reference true --reference $DIR/reference_seq.fasta --tree_file $DIR/nextstrain_flu_seasonal_h3n2_ha_2y_timetree_renamed.nwk
