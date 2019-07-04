[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AMIGA-IAA/hcg-16/master)

# Pipeline for HCG-16 Project

Work in progress. Here are the steps to run the pipeline:
```
curl -O https://raw.githubusercontent.com/AMIGA-IAA/hcg-16/master/run.sh
bash run.sh
```
[run.sh](https://github.com/AMIGA-IAA/hcg-16/blob/master/run.sh) will do automatically the following steps:
* download and install [conda](https://docs.conda.io/en/latest/)
* download and install [cgatcore](https://github.com/cgat-developers/cgat-core/blob/master/README.rst), a workflow management system
* construct a conda python environment with which to run the code
* download the source code
* download the input data
* run the [pipeline](https://github.com/AMIGA-IAA/hcg-16/blob/master/cgatcore/pipeline.py)

If you have already downloaded everything and just want to re-run the pipeline then you can do so with the following command (Note: the hcg-16 conda environment created above must be active):
```
python pipeline.py make plotting --local --timeit=pipeline.time
```
A present it is advised that you move or delete any output files before re-running the pipeline, as some of these files won't be overwritten by default and may cause the pipeline to crash or not generate the desired output.

## Pre-requisites
Please make sure you have `docker` installed on your computer before running `run.sh`. For the pipeline to execute succesfully it will require approximately 10 GB of free space. Also be aware that `docker` requires sudo access and may request the password during some steps of the pipeline.

# Plots for HCG-16 Project

If you do not wish to run the whole pipeline on your local machine (almost) all the figures of this project can be regenerated and modified using the cloud service [mybinder](https://mybinder.org/). There is a Jupyter notebook for each figure which can my run using [this link](https://mybinder.org/v2/gh/AMIGA-IAA/hcg-16/master). This service can take some time to start so please be patient.
