#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy,matplotlib,pandas
from general_functions import *
import matplotlib.pyplot as plt
from astropy import units as u
from astropy.coordinates import SkyCoord


# In[ ]:


font = {'size'   : 14, 'family' : 'serif', 'serif' : 'cm'}
plt.rc('font', **font)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['lines.linewidth'] = 1
plt.rcParams['axes.linewidth'] = 1

#Set to true to save pdf versions of figures
save_figs = True


# The files used to make the following plot are:

# In[ ]:


mask_sofia = 'HCG16_CD_rob2_MS_mask.fits'
cube_casa = 'HCG16_CD_rob2_MS.pbcor.fits'
spec_gbt = 'GBT_HCG16_spec.ascii'
cube_hipass = 'H290_abcde_luther_chop.fits'
mask_sofia_hipass = 'HIPASS_cube_sofia_mask.fits'
sofia_params_hipass = 'HIPASS_cube_params.session'


# 1. A $3.5\sigma$ mask of HCG 16 made with SoFiA after smoothing over various kernel sizes. This file was generated in the *masking* step of the workflow. The SoFiA parameters file which makes this file is [HCG16_CD_rob2_MS.3.5s.dil.session](sofia/HCG16_CD_rob2_MS.3.5s.dil.session).
# 2. The primary beam corrected, multi-scale CLEAN HI cube generated in the *imaging* step using CASA. The script [imaging.py](casa/imaging.py) contains the commands used to generate it.
# 3. The Green Bank Telescope spectrum of HCG 16 from the paper [Borthakur et al. 2010](iopscience.iop.org/article/10.1088/0004-637X/710/1/385/meta). Provided by S. Borthakur.
# 4. The HIPASS ([HI Parkes All Sky Survey](https://www.atnf.csiro.au/research/multibeam/release/)) cube covering the region of HCG 16 [(Barnes et al. 2001)](https://academic.oup.com/mnras/article/322/3/486/952500).
# 5. The SoFiA-generated mask of covering the HIPASS sub-cube containing HCG 16. This file was generated in the *masking* step of the workflow. The SoFiA parameters file which makes this file is [HIPASS_cube_params.session](sofia/HIPASS_cube_params.session).
# 6. The SoFiA parameters file for the mask (item 5).

# The mask and the cube need to be combined to eliminate regions of the cube which only contribute noise. Then the spatial dimensions of the cube must be collapsed to make a 1-dimensional spectrum.

# In[ ]:


#Read in the SoFiA mask
mask,mask_ra,mask_dec,mask_vel = read_fitscube(mask_sofia,mask=True)
#Read in the primary beam corrected HI cube
cube,cube_ra,cube_dec,cube_vel,bmaj,bmin,pa,beam_factor,cube_dx,cube_dy,cube_dv = read_fitscube(cube_casa,True,True)
#Mask the cube
masked_cube = numpy.multiply(cube,mask)
#Sum over the spatial dimensions to generate the integrated spectrum
VLA_spec = numpy.nansum(numpy.nansum(masked_cube,axis=1),axis=1)/beam_factor


# Read in the GBT spectrum and convert its frequency axis to a velocity axis.

# In[ ]:


#Read the spectrum
GBT_spec = pandas.read_csv(spec_gbt,delim_whitespace=True,names=['freq','flux'])
#2nd column is actually antenna temperature, need to be divided by 1.65 to get Jy
GBT_spec['flux'] = GBT_spec['flux']/1.65
#Convert the frequency axis to a velocity axis
GBT_spec['vel'] = c*(f0-GBT_spec['freq'])/GBT_spec['freq']


# The GBT beam does not cover the whole field of view of HCG 16, therefore to make a fair comparison the HI cube from the VLA must be weighted based on the beam response shape of the GBT beam, centred on the pointing centre of that observation. We approximate the GBT beam by a Gaussian with HPBW of 9.1 arcmin.

# In[ ]:


#Define the pointing centre of the GBT observation of Borthakur et al. 2010
GBT_pointing = SkyCoord('02h09m31.3s', '-10d09m30s', frame='icrs', equinox='J2000', unit='deg')
#Make empty array of pixel weights
pix_wts = numpy.zeros(numpy.shape(cube[0]))
#Set values for the length of the axes
leni,lenj = numpy.shape(pix_wts)

#Calculate the beam response in every pixel
for i in range(leni):
    #Define the pixel positions of a column of pixels in the WCS
    pix_pos = SkyCoord(numpy.repeat(cube_ra[i],len(cube_dec)), cube_dec, frame='icrs', equinox='J2000', unit='deg')
    #Calculate the separations from the pointing centre
    sep = GBT_pointing.separation(pix_pos)
    #Weight by the beam response (2.3548 is the factor to convert HPBW to STD)
    pix_wts[i] = gaussian(sep.arcmin,0.,9.1/2.3548)
    
#Apply the pixel weighting to the masked cube and sum to get the weighted spectrum
VLA_spec_wt = numpy.nansum(numpy.nansum(masked_cube*pix_wts,axis=1),axis=1)/beam_factor


# Read in the HIPASS cube, mask it and collapse it to form the spectrum.

# In[ ]:


#Read in the SoFiA mask for the HIPASS cube
HIP_mask,HIP_mask_ra,HIP_mask_dec,HIP_mask_vel = read_fitscube(mask_sofia_hipass,mask=True)
#Read in the HIPASS cube
HIP_cube,HIP_cube_ra,HIP_cube_dec,HIP_cube_vel,HIP_bmaj,HIP_bmin,HIP_pa,HIP_beam_factor,HIP_cube_dx,HIP_cube_dy,HIP_cube_dv = read_fitscube(cube_hipass,True,True)

#Read parameters file from SoFiA execution
#Find definition of the sub-region of the cube
param_file = open(sofia_params_hipass,'r')
for line in param_file:
    if 'import.subcube\t' in line:
        box = line.split('=')[1]
        box = box[2:-2]
        box = numpy.array(box.split(','),dtype='int')
param_file.close()

#Mask the sub-cube
HIP_masked_subcube = numpy.multiply(HIP_mask,HIP_cube[box[4]:box[5],box[2]:box[3],box[0]:box[1]])

#Sum over the spatial dimensions to generate the integrated spectrum
HIP_cube_spec = numpy.nansum(numpy.nansum(HIP_masked_subcube,axis=1),axis=1)/HIP_beam_factor


# Finally generate the plot.

# In[ ]:


#Initialise figure
fig = plt.subplots(figsize=(8.27,2.*3))

#Plot the GBT and HIPASS spectra
plt.step(GBT_spec['vel'],GBT_spec['flux'],c='g',where='mid',label='GBT')
plt.plot(HIP_mask_vel,HIP_cube_spec,lw=1,ls='-',c='orange',drawstyle='steps-mid',label='HIPASS')

#Plot the VLA spectra
plt.step(cube_vel,VLA_spec,c='k',lw=2,where='mid',label='VLA')
plt.plot(cube_vel,VLA_spec_wt,c='k',lw=2,ls='--',drawstyle='steps-mid',label='VLA in GBT beam')

#set plot range and draw axis line at 0 flux
plt.xlim(v_grp-500.,v_grp+500.)
plt.ylim(-0.02,0.22)
plt.axhline(c='k',lw=1)

#Add vertical lines showing the optical redshifts
plt.axvline(v_hcg16a,ls='--',c='k')
plt.axvline(v_hcg16b,ls='--',c='k')
plt.axvline(v_hcg16c,ls='--',c='k')
plt.axvline(v_hcg16d,ls='--',c='k')
plt.axvline(v_hcg16n,ls='--',c='k')
plt.axvline(v_hcg16p,ls='--',c='k')

#Annotate the lines
plt.annotate('HCG 16c',[v_hcg16c-165.,0.195],fontsize='14')
plt.annotate('HCG 16b',[v_hcg16c-165.,0.185],fontsize='14')
plt.annotate('HCG 16d',[v_hcg16c-165.,0.175],fontsize='14')

plt.plot([v_hcg16c-25.,v_hcg16c],[0.197,0.21],c='k')
plt.plot([v_hcg16c-25.,v_hcg16b],[0.187,0.20],c='k')
plt.plot([v_hcg16c-25.,v_hcg16d],[0.177,0.19],c='k')

plt.annotate('PGC 8210',[4120.,0.09],fontsize='14')
plt.annotate('NGC 848',[4120.,0.08],fontsize='14')
plt.annotate('HCG 16a',[4120.,0.07],fontsize='14')

plt.plot([4120.-5.,v_hcg16p],[0.094,0.1],c='k')
plt.plot([4120.-5.,v_hcg16n],[0.084,0.09],c='k')
plt.plot([4120.-5.,v_hcg16a],[0.074,0.08],c='k')

#Label axes
plt.xlabel(r'$v_\mathrm{opt}/\mathrm{km\,s^{-1}}$')
plt.ylabel(r'Flux Density/Jy')

#Make legend
plt.legend(fontsize='12')

#Save
if save_figs:
    plt.savefig("Fig4-HCG16_spectrum.pdf",bbox_inches='tight')

