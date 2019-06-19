[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AMIGA-IAA/hcg-16/master)

# Pipeline for HCG-16 Project

Work in progress. Here are the steps to run the pipeline:
```
curl -O https://raw.githubusercontent.com/AMIGA-IAA/hcg-16/master/run.sh
bash run.sh
```
[run.sh](https://github.com/AMIGA-IAA/hcg-16/blob/master/run.sh) will do automatically the following steps:
* download and install [cgatcore](https://github.com/cgat-developers/cgat-core/blob/master/README.rst), a workflow management system
* download the source code
* download the input data
* run the [pipeline](https://github.com/AMIGA-IAA/hcg-16/blob/master/cgatcore/pipeline.py)

## Pre-requisites
Please make sure you have `docker` installed on your computer before running `run.sh`. For the pipeline to execute succesfully will require approximately 7 GB of free space.

# Plots for HCG-16 Project

If you do not wish to run the whole pipeline on your local machine (almost) all the figures of this project can be regenerated and modified using the cloud service mybinder. There is a Jupyter notebook for each figure which can my run using the link at the top of this file. This service can take some time to start so please be patient.
