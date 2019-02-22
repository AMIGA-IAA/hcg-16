#!/usr/bin/env python

from ruffus import *
import sys
import os
import cgatcore.experiment as E
from cgatcore import pipeline as P

# TODO
# * task to pull/build docker containers

@originate('master.zip')
def download_code(outfile):
    statement = '''wget https://github.com/AMIGA-IAA/hcg-16/archive/master.zip'''
    P.run(statement)

@originate('hcg16-data.tar.gz')
def download_data(outfile):
    statement = '''wget https://trng-b2share.eudat.eu/api/files/8181b888-24c1-4680-968f-a701ba2221d2/hcg16-data.tar.gz'''
    P.run(statement)

@transform(download_code, suffix('master.zip'), 'prepare_code.done')
def prepare_code(infile, outfile):
    statement = '''unzip master.zip && rm master.zip && touch prepare_code.done'''
    P.run(statement)

@transform(download_data, suffix('hcg16-data.tar.gz'), 'prepare_data.done')
def prepare_data(infile, outfile):
    statement = '''tar xzf hcg16-data.tar.gz && rm hcg16-data.tar.gz && touch prepare_data.done'''
    P.run(statement)

@follows(prepare_code, prepare_data)
@merge('AW*.xp1', 'calibration.log')
def calibration(infiles, outfile):
    statement = '''/usr/bin/time -o calibration.time -v
    sudo docker run -v "$(pwd)":/data -t casa --nogui -c hcg-16-master/casa/calibration_flag.py --logfile calibration.log
    1> calibration.stdout
    2> calibration.stderr'''
    P.run(statement)
    # workaround until we get --logfile option to work with casa
    open(outfile, 'a').close()

@transform(calibration, suffix('calibration.log'), 'imaging.log')
def imaging(infile, outfile):
    statement = '''/usr/bin/time -o imaging.time -v
    sudo docker run -v "$(pwd)":/data -t casa --nogui -c hcg-16-master/casa/imaging.py --logfile imaging.log
    1> imaging.stdout
    2> imaging.stderr'''
    P.run(statement)
    # workaround until we get --logfile option to work with casa
    open(outfile, 'a').close()

@split(imaging, ['3.5s', '5.0s'])
def masking(infile, outfiles):
    for mask in outfiles:
        statement = '''/usr/bin/time -o masking.{}.time -v
        sudo docker run -v "$(pwd)":/data -t sofia hcg-16-master/sofia/HCG16_CD_rob2_MS.{}.nodil.session
        1> masking.{}.stdout
        2> masking.{}.stderr'''.format(mask, mask, mask, mask, mask)
        P.run(statement)

@files(None, 'reset.log')
def cleanup(infile, outfile):
    statement = '''sudo rm -rf HCG16_C* HCG16_D*
    *gcal* *bcal* *.last *.log *.time *.stdout *.stderr
    rflag* ctmp* delays.cal/ flux.cal/ gaincurve.cal/'''
    P.run(statement)

def main(argv=None):
    if argv is None:
        argv = sys.argv
    P.main(argv)

if __name__ == "__main__":
    sys.exit(P.main(sys.argv))
