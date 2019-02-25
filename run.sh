#!/usr/bin/env bash

### Install/activate conda

[[ -r Miniconda3-latest-Linux-x86_64.sh ]] || curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
[[ -d conda-install ]] || bash Miniconda3-latest-Linux-x86_64.sh -b -p conda-install

if [[ ! `which conda` ]] ; then
    source conda-install/etc/profile.d/conda.sh && \
    conda update --all --yes
fi

### Install cgatcore

if [[ ! `conda env list | grep cgatcore | grep '*'` ]] ; then
    conda create --name cgatcore cgatcore --channel bioconda --channel conda-forge --yes && \
    conda activate cgatcore
fi

### Download pipeline

[[ -r pipeline.py ]] || curl -O https://raw.githubusercontent.com/AMIGA-IAA/hcg-16/master/cgatcore/pipeline.py

### Run pipeline

python pipeline.py make masking --local --timeit=pipeline.time --shell-logfile=pipeline.shell

