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

### Install/activate conda

if [[ -d conda-install ]] ; then
    log " Conda installed. "
else
    if [[ -r Miniconda3-latest-Linux-x86_64.sh ]] ; then
        log " Conda  downloaded. "
    else
        log " Downloading conda... "
        curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh >& /dev/null
    fi
    log " Install conda... "
    bash Miniconda3-latest-Linux-x86_64.sh -b -p conda-install >& /dev/null
fi

if [[ "${CONDA_EXE}" ]] ; then
    log " Conda activated. "
else
    log " Activate conda... "
    source conda-install/etc/profile.d/conda.sh && \
    conda update --all --yes
fi

### Install cgatcore

if [[ "${CONDA_DEFAULT_ENV}" == "cgatcore" ]] ; then
    log " cgatcore environment loaded. "
else
    log " Activate cgatcore environment... "
    conda create --name cgatcore cgatcore --channel bioconda --channel conda-forge --yes && \
    conda activate cgatcore
fi

### Download pipeline

if [[ -r pipeline.py ]] ; then
    log " Pipeline downloaded. "
else
    log " Download pipeline... "
    curl -O https://raw.githubusercontent.com/AMIGA-IAA/hcg-16/master/cgatcore/pipeline.py
fi

### Run pipeline

if [[ -r pipeline.time ]] ; then
    log " Pipeline finished. "
else
    log " Run pipeline... "
    python pipeline.py make masking --local --timeit=pipeline.time
fi
