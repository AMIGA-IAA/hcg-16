#!/usr/bin/env bash

# exit when a command fails
set -o errexit

# exit if any pipe commands fail
set -o pipefail

# exit when your script tries to use undeclared variables
#set -o nounset

# trace what gets executed
#set -o xtrace

# Bash traps
# http://aplawrence.com/Basics/trapping_errors.html
# https://stelfox.net/blog/2013/11/fail-fast-in-bash-scripts/

#set -o errtrace

SCRIPT_NAME="$0"
SCRIPT_PARAMS="$@"

function error_handler() {
    echo
    echo " ########################################################## "
    echo
    echo " An error occurred in:"
    echo
    echo " - line number: ${1}"
    shift
    echo " - exit status: ${1}"
    shift
    echo " - command: ${@}"
    echo
    echo " The script will abort now. User input was: "
    echo
    echo " ${SCRIPT_NAME} ${SCRIPT_PARAMS}"
    echo
    echo " ########################################################## "
}

trap 'error_handler ${LINENO} $? ${BASH_COMMAND}' ERR INT TERM

# log installation information
function log() {
    echo "# run.sh log | `hostname` | `date` | $1 "
}

# report error and exit
function report_error() {
    echo
    echo $1
    echo
    echo "Aborting."
    echo
    exit 1
}

# function to deactivate inherited conda installation
function deactivate_conda() {

  EXISTS_CONDA=$(which conda) || $(echo "")

  if [[ "${EXISTS_CONDA}" ]] ; then
    log " Deactivate inherited conda... "

    CONDA_PATH=$(dirname $(dirname ${EXISTS_CONDA}))
    PATH_LIST=$(echo ${PATH} | tr ':' ' ')
    NEW_PATH=/usr/local/bin

    # loop to get rid of conda paths in PATH
    for e in $(echo ${PATH_LIST});
    do
      if [[ "${e}" != ${CONDA_PATH}* ]] && [[ "${e}" != "/usr/local/bin" ]] ; then
        NEW_PATH=${NEW_PATH}:${e}
      fi
    done

    # reconfig PATH
    PATH=${NEW_PATH}

    # loop to unset CONDA environment variables
    for e in $(env | grep CONDA | sed 's/=.*//g');
    do
      unset ${e}
    done

  fi
}

### Deactivate inherited conda from existing environment

deactivate_conda

### curl or wget?

DOWNLOAD_CMD="curl"

EXISTS_CURL=$(which curl) || $(echo "")

if [[ -z "${EXISTS_CURL}" ]] ; then
    DOWNLOAD_CMD="wget"
    DOWNLOAD_CMD_CONDA="wget -O"
else
    DOWNLOAD_CMD="curl -O"
    DOWNLOAD_CMD_CONDA="curl -o"
fi

### Install/activate specific conda for this project

# Check if pipeline has already installed conda
if [[ -r conda-install/etc/profile.d/conda.sh ]] ; then
    log " Conda already installed. "
else
    ### At this point we need to install miniconda
    if [[ -r Miniconda.sh ]] ; then
        log " Conda already downloaded. "
    else
        log " Downloading conda... "
        $DOWNLOAD_CMD_CONDA Miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh >& /dev/null
    fi
    log " Install conda... "
    bash Miniconda.sh -b -p conda-install >& /dev/null
fi
log " Activate conda... "
source conda-install/etc/profile.d/conda.sh

### Use mamba to speed up dependency resolution
### https://github.com/mamba-org/mamba

EXISTS_MAMBA=$(which mamba) || $(echo "")

if [[ -z "${EXISTS_MAMBA}" ]] ; then
    log " Install mamba... "
    conda install mamba -c conda-forge --yes
else
    log " mamba already available. "
fi

### Install conda environment

if [[ -r hcg-16.yml ]] ; then
    log " Conda environment downloaded. "
else
    log " Download conda environment... "
    $DOWNLOAD_CMD https://raw.githubusercontent.com/AMIGA-IAA/hcg-16/master/hcg-16.yml
fi

EXISTS_ENV=$(conda env list | grep "hcg-16 ") || $(echo "")

if [[ "${CONDA_DEFAULT_ENV}" == "hcg-16" ]] ; then
    log " hcg-16 environment loaded. "
elif [[ "${EXISTS_ENV}" != "" ]] ; then
    log " Activate hcg-16 environment..."
    conda activate hcg-16
else
    log " Install hcg-16 environment... "
    mamba env create --file hcg-16.yml && \
    conda activate hcg-16
fi

### Download pipeline

if [[ -r pipeline.py ]] ; then
    log " Pipeline downloaded. "
else
    log " Download pipeline... "
    $DOWNLOAD_CMD https://raw.githubusercontent.com/AMIGA-IAA/hcg-16/master/cgatcore/pipeline.py
fi

if [[ -r pipeline.yml ]] ; then
    log " Pipeline config downloaded. "
else
    log " Download pipeline config... "
    $DOWNLOAD_CMD https://raw.githubusercontent.com/AMIGA-IAA/hcg-16/master/cgatcore/pipeline.yml
fi

### Run pipeline

if [[ -r pipeline.time ]] ; then
    log " Pipeline finished. "
else
    log " Run pipeline... "
    python pipeline.py make plotting --local --timeit=pipeline.time
fi
