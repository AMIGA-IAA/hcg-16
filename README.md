[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AMIGA-IAA/hcg-16/master)

# 1) Pipeline for HCG-16 Project

This repository hosts a pipeline to reproduce the data reduction and analysis of [Jones et al. 2019](https://ui.adsabs.harvard.edu/abs/2019A%26A...632A..78J/abstract).

Here are the steps to run the pipeline:
```
# First make sure you create and go to a new working directory:
mkdir pipeline-run
cd pipeline-run

# Then execute:
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

If you have already downloaded everything and just want to re-run the pipeline then you can do so with the following command
(Note: the hcg-16 conda environment created above must be active):
```
python pipeline.py make plotting --local --timeit=pipeline.time
```
At present it is advised that you move or delete any output files before re-running the pipeline, as some of these files
won't be overwritten by default and may cause the pipeline to crash or not generate the desired output.

## Pre-requisites
Please make sure you have `docker` installed on your computer before running `run.sh`. [Here](https://docs.docker.com/install/)
are instructions on how to install docker. For the pipeline to execute succesfully it will require approximately 10 GB of free
space. Also be aware that `docker` requires sudo access and may request the password during some steps of the pipeline.

# 2) Plots for HCG-16 Project on the cloud

If you do not wish to run the whole pipeline on your local machine (almost) all the figures of this project can be regenerated
and modified using the cloud service [mybinder](https://mybinder.org/). There is a Jupyter notebook for each figure which can
be run using [this link](https://mybinder.org/v2/gh/AMIGA-IAA/hcg-16/master). This service can take some time to start so please
be patient.


# 3) Plots for HCG-16 Project in local environment

Alternatively, you may regenerate the plots by running the notebooks in your machine. First, you will need to clone the repository, create the conda environment to set up the software environment with all the dependencies: 

```
git clone https://github.com/AMIGA-IAA/hcg-16.git
conda update conda
conda env create --file environment.yml 
conda activate hcg-16
```

You will also need to download the data files that are used in the notebooks by running the following commands in the plot_scripts folder:

```
wget https://b2share.eudat.eu/api/files/878dbee0-01bf-4b85-8ed3-71818cd223bf/HCG16_final_data.tar.gz
tar -xzf HCG16_final_data.tar.gz
```

Finally, you are ready to launch the Jupyter server and open the notebooks:
``` 
jupyter notebook 
```

## Pre-requisites
Please make sure you have `conda` and `git` installed on your computer before cloning the repository and running conda commands. 
 

# 4) Final data and visualisation

If you are only interested in downloading the final reduced data cubes these are located at stored on the [EUDAT B2SHARE](https://b2share.eudat.eu/records/a69a7b2dcc22449e8734552dde4d3906) service (DOI: 10.23728/b2share.a69a7b2dcc22449e8734552dde4d3906). There is also a 3D visualisation of the HI data cube hosted on the [AMIGA webpage](http://amiga.iaa.es/FCKeditor/UserFiles/X3D/HCG16/HCG16.html).
