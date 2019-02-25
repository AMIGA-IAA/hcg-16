#!/usr/bin/env bash

### Install/activate conda

[[ -r Miniconda3-latest-Linux-x86_64.sh ]] || curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
[[ -d conda-install ]] || bash Miniconda3-latest-Linux-x86_64.sh -b -p conda-install
[[ `which conda` ]] || (source conda-install/etc/profile.d/conda.sh && conda update --all --yes)

### Install cgatcore

[[ `conda env list | grep cgatcore | grep '*'` ]] || \
    (conda create --name cgatcore cgatcore --channel bioconda --channel conda-forge --yes && \
     conda activate cgatcore)

### Download pipeline

[[ -d hcg-16-master/ ]] || \
    (wget https://github.com/AMIGA-IAA/hcg-16/archive/master.zip && \
     unzip master.zip && \
     rm master.zip)

### Run pipeline

python hcg-16-master/cgatcore/pipeline.py make masking --local --timeit=pipeline.time --shell-logfile=pipeline.shell

