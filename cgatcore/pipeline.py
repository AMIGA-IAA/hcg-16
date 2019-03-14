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
    deps = ["wget", "unzip", "tar", "docker", "time"]
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
    statement = '''/usr/bin/time -o calibration.time -v
    sudo docker run -v "$(pwd)":/data -t amigahub/casa:v1.0 --nogui --logfile calibration.log -c hcg-16-master/casa/calibration_flag.py
    1> calibration.stdout
    2> calibration.stderr'''
    P.run(statement)

@transform(calibration, suffix('calibration.log'), 'imaging.log')
def imaging(infile, outfile):
    statement = '''/usr/bin/time -o imaging.time -v
    sudo docker run -v "$(pwd)":/data -t amigahub/casa:v1.0 --nogui --logfile imaging.log -c hcg-16-master/casa/imaging.py
    1> imaging.stdout
    2> imaging.stderr'''
    P.run(statement)

@split(imaging, ['3.5s.dil', '5.0s.nodil'])
def masking(infile, outfiles):
    for mask in outfiles:
        statement = '''/usr/bin/time -o masking.{}.time -v
        sudo docker run -v "$(pwd)":/data -t amigahub/sofia:v1.0 hcg-16-master/sofia/HCG16_CD_rob2_MS.{}.session
        1> masking.{}.stdout
        2> masking.{}.stderr'''.format(mask, mask, mask, mask, mask)
        P.run(statement)
        open(mask, 'a').close()

@follows(imaging, masking)
@merge(imaging, 'plotting.done')
def plotting(infiles, outfile):
    statement = '''/usr/bin/time -o plotting.time -v
    python hcg-16-master/plot_scripts/absorption_spec.py &&
    python hcg-16-master/plot_scripts/global_mom0.py &&
    python hcg-16-master/plot_scripts/global_mom1.py &&
    touch plotting.done
    '''
    P.run(statement)

@files(None, 'reset.log')
def cleanup(infile, outfile):
    statement = '''sudo rm -rf HCG16_C* HCG16_D*
    hcg-16-master/ HCG16_source_mask/ AW*.xp1
    *gcal* *bcal* *.last *.log *.time *.stdout *.stderr *.done
    rflag* ctmp* delays.cal/ flux.cal/ gaincurve.cal/ *dil'''
    P.run(statement)

def main(argv=None):
    if argv is None:
        argv = sys.argv
    P.main(argv)

if __name__ == "__main__":
    sys.exit(P.main(sys.argv))
