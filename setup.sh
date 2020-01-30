# ts_transfer packages
conda create --name assignment1 python=3.6
source ~/anaconda3/etc/profile.d/conda.sh
conda activate assignment1

# basic
conda install -c anaconda numpy==1.16.1
conda install -c anaconda pandas==0.25.2

# visualization
conda install -c conda-forge matplotlib==3.1.1

# census
pip install CensusData

#psycopg2
conda install -c anaconda psycopg2

conda install -c conda-forge jupyterlab
ipython kernel install --user --name=assignment1
conda deactivate
