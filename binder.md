
Notes about binder
==================

In September 2022 running this repository on mybinder.org failed.

After asking for [support](https://discourse.jupyter.org/t/mamba-env-update-instead-of-mamba-env-create/)
we were asked to use [conda-lock](https://conda-incubator.github.io/conda-lock/) to solve the issue.

Below are the steps to work with `conda-lock`:

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p conda-install
source conda-install/etc/profile.d/conda.sh 
conda install mamba -c conda-forge --yes
mamba create -n conda-lock -c conda-forge conda-lock --yes
conda activate conda-lock
conda-lock --file=hcg-16.yml --platform=linux-64 --kind=explicit --mamba
```

This creates a `conda-linux-64.lock` file that can be installed with:

```bash
mamba create --name hcg-16 --file conda-linux-64.lock
```

This is what we have included in binder's `postBuild` script to solve the issue.
