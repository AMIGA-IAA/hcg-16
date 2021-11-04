[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AMIGA-IAA/hcg-16/master)

# 1) Pipeline for HCG-16 Project

This repository hosts a pipeline to reproduce the data reduction and analysis of [Jones et al. 2019](https://ui.adsabs.harvard.edu/abs/2019A%26A...632A..78J/abstract).

Here are the steps to run the pipeline:

First make sure you create and go to a new working directory:
```
mkdir pipeline-run
cd pipeline-run
```
Then execute:
```
curl -O https://raw.githubusercontent.com/AMIGA-IAA/hcg-16/master/run.sh
bash run.sh
```

[run.sh](https://github.com/AMIGA-IAA/hcg-16/blob/master/run.sh) will do automatically the following steps:
* download and install [miniconda](https://docs.conda.io/en/latest/miniconda.html)
* download and install [cgatcore](https://github.com/cgat-developers/cgat-core/), a workflow management system
* construct a [conda python environment](https://github.com/AMIGA-IAA/hcg-16/blob/master/environment.yml) with which to run the code
* download this repository with the source code of the analysis
* download the [input data](https://b2share.eudat.eu/records/f8fcd84bcd454bdc8ea0ec2d69bdfe9a)
* run the [pipeline](https://github.com/AMIGA-IAA/hcg-16/blob/master/cgatcore/pipeline.py)

If you have already downloaded everything and just want to re-run the pipeline then you can do so with the following command
(Note: the hcg-16 conda environment created above must be active):
```
python pipeline.py make plotting --local --timeit=pipeline.time
```
At present it is advised that you move or delete any output files before re-running the pipeline, as some of these files
won't be overwritten by default and may cause the pipeline to crash or not generate the desired output.

## Pre-requisites
For the pipeline to execute succesfully it will require approximately 20 GB of free
space. Approximately 10 GB will be used in the directory where the pipeline is executed, and about 9 GB will be used in `~/.udocker`.

# 2) Plots for HCG-16 Project on the cloud

If you do not wish to run the whole pipeline on your local machine (almost) all the figures of this project can be regenerated
and modified using the cloud service [mybinder](https://mybinder.org/). There is a Jupyter notebook for each figure which can
be run using [this link](https://mybinder.org/v2/gh/AMIGA-IAA/hcg-16/master). This service can take some time to start so please
be patient.

In order to test integration with [EGI Notebooks](https://marketplace.eosc-portal.eu/services/egi-notebooks) in the context of the [European Open Science Cloud](https://eosc-portal.eu/) the Jupyter notebooks have also been uploaded to [EUDAT](https://b2share.eudat.eu/records/adf6e2e942b04561a8640c449b48c14a) and they are now discoverable via the beta instance of [OpenAIRE](https://beta.explore.openaire.eu/search/software?pid=10.23728%2Fb2share.adf6e2e942b04561a8640c449b48c14a).

# 3) Plots for HCG-16 Project in local environment

Alternatively, you may regenerate the plots by running the notebooks in your machine. 

First, you will need to clone the repository:
```
git clone https://github.com/AMIGA-IAA/hcg-16.git
cd hcg-16
```
Download and install conda (if conda is already available on your system you may skip this step):
```
curl -o Miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-4.6.14-Linux-x86_64.sh
bash Miniconda.sh -b -p conda-install
source conda-install/etc/profile.d/conda.sh
```
Create and activate the conda environment:
```
conda env create --file environment.yml 
conda activate hcg-16
```

You will also need to download the data files that are used in the notebooks by running the following commands:

```
cd plot_scripts
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

If you are only interested in downloading the final reduced data cubes these are stored on the [EUDAT B2SHARE](https://b2share.eudat.eu/records/a69a7b2dcc22449e8734552dde4d3906) service (DOI: 10.23728/b2share.a69a7b2dcc22449e8734552dde4d3906). The single cube on which most of the analysis depends is also available from [CDS](http://vizier.u-strasbg.fr/viz-bin/getCatFile?-plus=-%2b&J/A%2bA/632/A78/./fits/HCG16_CD_rob2_MS.pbcor.fits).There is also a 3D visualisation of the HI data cube hosted on the [AMIGA webpage](http://amiga.iaa.es/FCKeditor/UserFiles/X3D/HCG16/HCG16.html).
