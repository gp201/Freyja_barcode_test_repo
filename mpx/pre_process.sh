# exit when any command fails
set -e
# print each command before executing
set -x


# # ENV name
# RUN_ENV=freyja-mpx-pathogen

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

# download sequences from nextstrain
wget https://data.nextstrain.org/files/workflows/monkeypox/alignment.fasta.xz
# unzip the file
unxz alignment.fasta.xz

python3 code/extract_seqs.py alignment.fasta nextstrain_monkeypox_hmpxv1_metadata.tsv
python3 code/rename_fasta.py extracted_seqs.fasta nextstrain_monkeypox_hmpxv1_metadata.tsv
cat reference_seq.fasta extracted_seqs.fasta > combined_seqs.fasta

# get current directory and place it in a variable
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Clone the Freyja pathogen workflow
git clone https://github.com/gp201/Freyja_pathogen_workflow.git
cd Freyja_pathogen_workflow

eval "$(conda shell.bash hook)"
conda deactivate

# print and run the below command
bash run_nf.sh $DIR/ $DIR/combined_seqs.fasta $DIR/formatted_metadata.tsv --align_to_reference true --reference $DIR/reference_seq.fasta --align_mode mafft --strain_column "strain" --date_column "Date" --skip_clade_annotations true --tree_file $DIR/nextstrain_monkeypox_hmpxv1_timetree.nwk
