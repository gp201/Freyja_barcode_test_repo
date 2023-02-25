# exit when any command fails
set -e
# print each command before executing
set -x

# ENV name
# RUN_ENV=freyja-zika-pathogen


# # Setup conda env
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

python3 rename_fasta.py -i zika_genomes.fasta -d ' ' -o renamed_zika_genomes.fasta

# get current directory and place it in a variable
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Clone the Freyja pathogen workflow
git clone https://github.com/gp201/Freyja_pathogen_workflow.git
cd Freyja_pathogen_workflow

eval "$(conda shell.bash hook)"
conda deactivate

# print and run the below command
echo "cannot run since phyclip is not installed"
# bash run_nf.sh $DIR/ $DIR/renamed_zika_genomes.fasta $DIR/zika_dates.csv --strain_column "name" --skip_clade_annotations true --align_to_reference true --reference $DIR/reference_seq.fasta --tree_file $DIR/nextstrain_flu_seasonal_h3n2_ha_2y_timetree_renamed.nwk

