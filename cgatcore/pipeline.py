#!/usr/bin/env python

from ruffus import *
import sys
import os
import shutil
import cgatcore.experiment as E
from cgatcore import pipeline as P

PARAMS = P.get_parameters("pipeline.yml")

@originate('dependency_check.done')
def dependency_check(outfile):
    deps = ["wget", "unzip", "tar", "udocker", "time"]
    for cmd in deps:
        if shutil.which(cmd) is None:
            raise EnvironmentError("Required dependency \"{}\" not found".format(cmd))
    open(outfile, 'a').close()

@follows(dependency_check)
@originate('download_code.done')
def download_code(outfile):
    statement = '''wget {} && touch download_code.done'''.format(PARAMS['input']['code'])
    P.run(statement)

@follows(dependency_check)
@originate('download_data.done')
def download_data(outfile):
    statement = '''wget {} && touch download_data.done'''.format(PARAMS['input']['data'])
    P.run(statement)

@transform(download_code, suffix('download_code.done'), 'prepare_code.done')
def prepare_code(infile, outfile):
    statement = '''unzip master.zip &&
    rm master.zip &&
    touch prepare_code.done'''
    P.run(statement)

@transform(download_data, suffix('download_data.done'), 'prepare_data.done')
def prepare_data(infile, outfile):
    statement = '''tar xzf hcg16-data.tar.gz &&
    rm hcg16-data.tar.gz &&
    touch prepare_data.done'''
    P.run(statement)

@follows(prepare_code, prepare_data)
@merge('AW*.xp1', 'calibration.log')
def calibration(infiles, outfile):
    statement = '''\\time -o calibration.time -v
    udocker run -v "$(pwd)":/data -t amigahub/casa:v1.0 --nogui --logfile calibration.log -c hcg-16-master/casa/calibration_flag.py
    1> calibration.stdout
    2> calibration.stderr'''
    P.run(statement)

@transform(calibration, suffix('calibration.log'), 'imaging.log')
def imaging(infile, outfile):
    statement = '''\\time -o imaging.time -v
    udocker run -v "$(pwd)":/data -t amigahub/casa:v1.0 --nogui --logfile imaging.log -c hcg-16-master/casa/imaging.py
    1> imaging.stdout
    2> imaging.stderr'''
    P.run(statement)

@split(imaging, ['HCG16_CD_rob2_MS.3.5s.dil', 'HCG16_CD_rob2_MS.5.0s.nodil', 'HIPASS_cube_params'])
def masking(infile, outfiles):
    for mask in outfiles:
        statement = '''\\time -o masking.{}.time -v
        udocker run -v "$(pwd)":/data -t amigahub/sofia:v1.0 hcg-16-master/sofia/{}.session
        1> masking.{}.stdout
        2> masking.{}.stderr'''.format(mask, mask, mask, mask, mask)
        P.run(statement)
        open(mask, 'a').close()

@originate('HCG16_DECaLS_cutout.jpeg')
def get_decals_jpeg(outfile):
    statement = '''
    wget "{}" -O HCG16_DECaLS_cutout.jpeg
    '''.format(PARAMS['decals']['jpeg'])
    P.run(statement)

@originate('HCG16_DECaLS_r_cutout.fits')
def get_decals_fits(outfile):
    statement = '''
    wget "{}" -O HCG16_DECaLS_r_cutout.fits
    '''.format(PARAMS['decals']['fits'])
    P.run(statement)

@follows(imaging, masking, get_decals_jpeg, get_decals_fits)
@merge(imaging, 'plotting.done')
def plotting(infiles, outfile):
    statement = '''\\time -o plotting.time -v
    cp hcg-16-master/plot_scripts/*.ipynb . &&
    cp hcg-16-master/plot_scripts/*.py . &&
    cp hcg-16-master/sofia/HIPASS_cube_params.session . &&
    for n in `ls *.ipynb`; do jupyter nbconvert --to python $n; newname=$(echo $n | sed 's/.ipynb/.py/g'); python $newname; done &&
    touch plotting.done
    '''
    P.run(statement)

@files(None, 'reset.log')
def cleanup(infile, outfile):
    statement = '''rm -rf HCG16_C* HCG16_D*
    hcg-16-master/ HCG16_source_mask/ AW*.xp1
    *gcal* *bcal* *.last *.log *.time *.stdout *.stderr *.done
    rflag* ctmp* delays.cal/ flux.cal/ gaincurve.cal/ *dil
    *fits *ascii S* N* E_clump* PGC8210* H* cd_bridge* Fig* Tab2* general_functions.py __pycache__/'''
    P.run(statement)

def main(argv=None):
    if argv is None:
        argv = sys.argv
    P.main(argv)

if __name__ == "__main__":
    sys.exit(P.main(sys.argv))
