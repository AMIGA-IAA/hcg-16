#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy,matplotlib,pandas
from general_functions import *
import matplotlib.pyplot as plt


# In[ ]:


font = {'size'   : 14, 'family' : 'serif', 'serif' : 'cm'}
plt.rc('font', **font)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['lines.linewidth'] = 1
plt.rcParams['axes.linewidth'] = 1

#Set to true to save pdf versions of figures
save_figs = True


# The files used to make the following plots are:

# In[ ]:


obj_list = ['HCG16a','HCG16b','HCG16c','HCG16d','NGC848','PGC8210',
            'NW_tail','NE_tail','E_clump','S_clump','SE_tail',
            'cd_bridge','NGC848S_tail','NGC848S_loop'] 
#+".fits" or +"_mask.fits"


# For each galaxy or feature there is a mini-cube of the HI emission of that object "name.fits" and a mask covering all the emission assigned to that objects "name_mask.fits". The masks were created manually using the SlicerAstro software (not included in the workflow) and were downloaded along with the raw data from the EUDAT service [B2SHARE](http://b2share.eudat.eu). The exact location of the data are given in the [pipeline.yml](pipeline.yml) file. The mini-cubes were generated in CASA (in the *imaging* step of the workflow), which is described in the script [imaging.py](casa/imaging.py).

# Use the mask and mini-cubes to generate a spectrum of each objects and measure the integrated flux, HI mass, mean velocity, and velocity dispersion.

# In[ ]:


#Initialise blank arrays/lists
spec = []
vel = []
flux = numpy.zeros(len(obj_list))
mhi = numpy.zeros(len(obj_list)) 
mean_vel = numpy.zeros(len(obj_list)) 
vel_disp = numpy.zeros(len(obj_list)) 

for i in range(len(obj_list)):
    obj = obj_list[i]
    
    #Read in the cube and build its axes
    cube,cube_ra,cube_dec,cube_vel,bmaj,bmin,pa,beam_factor,cube_dx,cube_dy,cube_dv = read_fitscube(obj+'.fits',True,True)
    #Read in the mask
    mask,mask_ra,mask_dec,mask_vel = read_fitscube(obj+'_mask.fits')
    #Apply the mask to the cube
    masked_cube = mask*cube
    #Collapse the spatial dimensions of the masked cube to make a spectrum
    spec.append(numpy.nansum(numpy.nansum(masked_cube,axis=1),axis=1)/beam_factor)
    #Copy the velocity axis
    vel.append(cube_vel)
    #Calculate the integrated flux
    flux[i] = numpy.sum(spec[i]*abs(cube_dv))
    #Convert the flux to an HI mass
    mhi[i] = numpy.log10(235600.*dist*dist*flux[i])
    #Measure the mean velocity
    mean_vel[i] = numpy.nansum(spec[i]*cube_vel)/numpy.nansum(spec[i])
    #Measure the velocity dispersion
    vel_disp[i] = numpy.sqrt(numpy.nansum(numpy.absolute(spec[i])*((cube_vel-mean_vel[i])**2.))/numpy.nansum(spec[i]))


# Use the scaling relation of [Jones et al. 2018](www.aanda.org/articles/aa/abs/2018/01/aa31448-17/aa31448-17.html) to predict the expected HI mass of each galaxy based on it's B-band luminosity.

# In[ ]:


#Build empty arrays and fill with NaNs
Bcmag = numpy.zeros(len(obj_list)) + numpy.nan
err_Bcmag = numpy.zeros(len(obj_list)) + numpy.nan

#B-band magnitude values from AMIGA private database
Bcmag[0:6] = [12.91, 13.25, 13.30, 13.67, 13.37, 15.17]
err_Bcmag[0:6] = [0.12,0.13,0.05,0.05,0.10,0.44]

#Make HI deficiency estimates
pred_mhi,err_pred_mhi = logMHI_pred(numpy.array(Bcmag),dist,numpy.array(err_Bcmag),err_dist)
hi_def = pred_mhi - mhi


# Compile all the information calculated above to build a pandas data frame and generate a table equivalent to Table 2 of the paper.

# In[ ]:


#Make pandas dataframe from dictionary
hi_data = {'Object': obj_list,
           'Flux [Jy km/s]': numpy.round(flux,2),
           'Mean Vel. [km/s]': numpy.round(mean_vel,0),
           'Vel. Disp. [km/s]': numpy.round(vel_disp,0),
           'log MHI [Msol]': numpy.round(mhi,2),
           'HI Def.': numpy.round(hi_def,2),
           'HI Def. Error': numpy.round(err_pred_mhi,2)}

hi_data = pandas.DataFrame(hi_data)
hi_data = hi_data.set_index('Object')

hi_data[['Flux [Jy km/s]','Mean Vel. [km/s]','Vel. Disp. [km/s]','log MHI [Msol]','HI Def.','HI Def. Error']]


# Plot the separated spectra as in Figures 4 and 5 of the paper.

# In[ ]:


fig,axarr = plt.subplots(nrows=3, ncols=2, sharex=True, figsize=(2.*8.27,3*4.))

vel_min = 3600.
vel_max = 4350.

plt_vel = numpy.zeros(len(vel[0])+2)
plt_spec = numpy.zeros(len(vel[0])+2)
plt_vel[1:-1] = vel[0]
plt_spec[1:-1] = spec[0]
plt_vel[0] = 2.*vel[0][0] - vel[0][1]
plt_vel[-1] = 2.*vel[0][-1] - vel[0][-2]

ax = axarr[0,0]
ax.step(plt_vel,1000.*plt_spec,label='HCG 16a',color='k',where='mid')
ax.set_ylabel('Flux Density [mJy]')
ax.set_xlim(vel_min,vel_max)
ax.set_ylim(0.,11.)
ax.axvline(v_hcg16a,ls='--',c='k')
ax.axvline(m98_v_hcg16a_cen,ls='dashdot',c='b')
ax.axvline(m98_v_hcg16a_cen+m98_v_hcg16a_max,ls='dotted',c='b')
ax.axvline(m98_v_hcg16a_cen+m98_v_hcg16a_min,ls='dotted',c='b')
ax.axvline(r91_v_hcg16a_cen,ls='dashdot',c='r')
ax.axvline(r91_v_hcg16a_cen-r91_vmax_hcg16a,ls='dotted',c='r')
ax.axvline(r91_v_hcg16a_cen+r91_vmax_hcg16a,ls='dotted',c='r')
ax.annotate('HCG 16a',xy=[0.05,0.9],xycoords='axes fraction')

plt_vel = numpy.zeros(len(vel[1])+2)
plt_spec = numpy.zeros(len(vel[1])+2)
plt_vel[1:-1] = vel[1]
plt_spec[1:-1] = spec[1]
plt_vel[0] = 2.*vel[1][1] - vel[1][1]
plt_vel[-1] = 2.*vel[1][-1] - vel[1][-2]

ax = axarr[1,0]
ax.step(plt_vel,1000.*plt_spec,label='HCG 16b',color='k',where='mid')
ax.set_ylabel('Flux Density [mJy]')
ax.set_xlim(vel_min,vel_max)
ax.set_ylim(0.,11.)
ax.axvline(v_hcg16b,ls='--',c='k')
ax.axvline(m98_v_hcg16b_cen,ls='dashdot',c='b')
ax.axvline(m98_v_hcg16b_cen+m98_v_hcg16b_max,ls='dotted',c='b')
ax.axvline(m98_v_hcg16b_cen+m98_v_hcg16b_min,ls='dotted',c='b')
ax.axvline(r91_v_hcg16b_cen,ls='dashdot',c='r')
ax.annotate('HCG 16b',xy=[0.05,0.9],xycoords='axes fraction')

plt_vel = numpy.zeros(len(vel[5])+2)
plt_spec = numpy.zeros(len(vel[5])+2)
plt_vel[1:-1] = vel[5]
plt_spec[1:-1] = spec[5]
plt_vel[0] = 2.*vel[5][1] - vel[5][1]
plt_vel[-1] = 2.*vel[5][-1] - vel[5][-2]

ax = axarr[2,0]
ax.step(plt_vel,1000.*plt_spec,label='PGC8210',color='k',where='mid')
ax.set_ylabel('Flux Density [mJy]')
ax.set_xlabel('$v_{\mathrm{opt}}$ [km/s]')
ax.set_xlim(vel_min,vel_max)
ax.set_ylim(0.,11.)
ax.axvline(v_hcg16p,ls='--',c='k')
ax.annotate('PGC 8210',xy=[0.05,0.9],xycoords='axes fraction')

plt_vel = numpy.zeros(len(vel[2])+2)
plt_spec = numpy.zeros(len(vel[2])+2)
plt_vel[1:-1] = vel[2]
plt_spec[1:-1] = spec[2]
plt_vel[0] = 2.*vel[2][1] - vel[2][1]
plt_vel[-1] = 2.*vel[2][-1] - vel[2][-2]

ax = axarr[0,1]
ax.step(plt_vel,1000.*plt_spec,label='HCG 16c',color='k',where='mid')
ax.set_ylabel('Flux Density [mJy]')
ax.set_xlim(vel_min,vel_max)
ax.set_ylim(0.,60.)
ax.axvline(v_hcg16c,ls='--',c='k')
ax.axvline(m98_v_hcg16c_cen,ls='dashdot',c='b')
ax.axvline(m98_v_hcg16c_cen+m98_v_hcg16c_max,ls='dotted',c='b')
ax.axvline(m98_v_hcg16c_cen+m98_v_hcg16c_min,ls='dotted',c='b')
ax.axvline(r91_v_hcg16c_cen,ls='dashdot',c='r')
ax.annotate('HCG 16c',xy=[0.05,0.9],xycoords='axes fraction')

plt_vel = numpy.zeros(len(vel[3])+2)
plt_spec = numpy.zeros(len(vel[3])+2)
plt_vel[1:-1] = vel[3]
plt_spec[1:-1] = spec[3]
plt_vel[0] = 2.*vel[3][1] - vel[3][1]
plt_vel[-1] = 2.*vel[3][-1] - vel[3][-2]

ax = axarr[1,1]
ax.step(plt_vel,1000.*plt_spec,label='HCG 16d',color='k',where='mid')
ax.set_ylabel('Flux Density [mJy]')
ax.set_xlim(vel_min,vel_max)
ax.set_ylim(0.,60.)
ax.axvline(v_hcg16d,ls='--',c='k')
ax.axvline(m98_v_hcg16d_cen+m98_v_hcg16d_max,ls='dotted',c='b')
ax.axvline(m98_v_hcg16d_cen+m98_v_hcg16d_min,ls='dotted',c='b')
ax.axvline(r91_v_hcg16d_cen,ls='dashdot',c='r')
ax.axvline(r91_v_hcg16d_cen-r91_vmax_hcg16d,ls='dotted',c='r')
ax.axvline(r91_v_hcg16d_cen+r91_vmax_hcg16d,ls='dotted',c='r')
ax.annotate('HCG 16d',xy=[0.05,0.9],xycoords='axes fraction')

plt_vel = numpy.zeros(len(vel[4])+2)
plt_spec = numpy.zeros(len(vel[4])+2)
plt_vel[1:-1] = vel[4]
plt_spec[1:-1] = spec[4]
plt_vel[0] = 2.*vel[4][1] - vel[4][1]
plt_vel[-1] = 2.*vel[4][-1] - vel[4][-2]

ax = axarr[2,1]
ax.step(plt_vel,1000.*plt_spec,label='NGC 848',color='k',where='mid')
ax.set_ylabel('Flux Density [mJy]')
ax.set_xlabel('$v_{\mathrm{opt}}$ [km/s]')
ax.set_xlim(vel_min,vel_max)
ax.set_ylim(0.,60.)
ax.axvline(v_hcg16n,ls='--',c='k')
ax.annotate('NGC 848',xy=[0.05,0.9],xycoords='axes fraction')

if save_figs:
    plt.savefig('Fig5-HCG16_galaxy_spectra_indv.pdf',bbox_inches='tight')


# In[ ]:


fig,axarr = plt.subplots(nrows=4, ncols=2, sharex=True, figsize=(2.*8.27,4*4.))

plt_vel = numpy.zeros(len(vel[10])+2)
plt_spec = numpy.zeros(len(vel[10])+2)
plt_vel[1:-1] = vel[10]
plt_spec[1:-1] = spec[10]
plt_vel[0] = 2.*vel[10][0] - vel[10][1]
plt_vel[-1] = 2.*vel[10][-1] - vel[10][-2]

ax = axarr[0,0]
ax.step(plt_vel,1000.*plt_spec,color='k',where='mid')
ax.set_ylabel('Flux Density [mJy]')
ax.set_xlim(vel_min,vel_max)
ax.set_ylim(0.,65.)
ax.annotate('SE Tail',xy=[0.05,0.9],xycoords='axes fraction')

plt_vel = numpy.zeros(len(vel[11])+2)
plt_spec = numpy.zeros(len(vel[11])+2)
plt_vel[1:-1] = vel[11]
plt_spec[1:-1] = spec[11]
plt_vel[0] = 2.*vel[11][0] - vel[11][1]
plt_vel[-1] = 2.*vel[11][-1] - vel[11][-2]

ax = axarr[0,1]
ax.step(plt_vel,1000.*plt_spec,color='k',where='mid')
ax.set_ylabel('Flux Density [mJy]')
ax.set_xlim(vel_min,vel_max)
ax.set_ylim(0.,65.)
ax.annotate('cd Bridge',xy=[0.05,0.9],xycoords='axes fraction')


plt_vel = numpy.zeros(len(vel[9])+2)
plt_spec = numpy.zeros(len(vel[9])+2)
plt_vel[1:-1] = vel[9]
plt_spec[1:-1] = spec[9]
plt_vel[0] = 2.*vel[9][0] - vel[9][1]
plt_vel[-1] = 2.*vel[9][-1] - vel[9][-2]

ax = axarr[1,0]
ax.step(plt_vel,1000.*plt_spec,color='k',where='mid')
ax.set_ylabel('Flux Density [mJy]')
ax.set_xlim(vel_min,vel_max)
ax.set_ylim(0.,35.)
ax.annotate('S Clump',xy=[0.05,0.9],xycoords='axes fraction')

plt_vel = numpy.zeros(len(vel[6])+2)
plt_spec = numpy.zeros(len(vel[6])+2)
plt_vel[1:-1] = vel[6]
plt_spec[1:-1] = spec[6]
plt_vel[0] = 2.*vel[6][0] - vel[6][1]
plt_vel[-1] = 2.*vel[6][-1] - vel[6][-2]

ax = axarr[1,1]
ax.step(plt_vel,1000.*plt_spec,color='k',where='mid')
ax.set_ylabel('Flux Density [mJy]')
ax.set_xlim(vel_min,vel_max)
ax.set_ylim(0.,35.)
ax.annotate('NW Tail',xy=[0.05,0.9],xycoords='axes fraction')


plt_vel = numpy.zeros(len(vel[8])+2)
plt_spec = numpy.zeros(len(vel[8])+2)
plt_vel[1:-1] = vel[8]
plt_spec[1:-1] = spec[8]
plt_vel[0] = 2.*vel[8][0] - vel[8][1]
plt_vel[-1] = 2.*vel[8][-1] - vel[8][-2]

ax = axarr[2,0]
ax.step(plt_vel,1000.*plt_spec,color='k',where='mid')
ax.set_ylabel('Flux Density [mJy]')
ax.set_xlim(vel_min,vel_max)
ax.set_ylim(0.,25.)
ax.annotate('E Clump',xy=[0.05,0.9],xycoords='axes fraction')

plt_vel = numpy.zeros(len(vel[7])+2)
plt_spec = numpy.zeros(len(vel[7])+2)
plt_vel[1:-1] = vel[7]
plt_spec[1:-1] = spec[7]
plt_vel[0] = 2.*vel[7][0] - vel[7][1]
plt_vel[-1] = 2.*vel[7][-1] - vel[7][-2]

ax = axarr[2,1]
ax.step(plt_vel,1000.*plt_spec,color='k',where='mid')
ax.set_ylabel('Flux Density [mJy]')
ax.set_xlim(vel_min,vel_max)
ax.set_ylim(0.,25.)
ax.annotate('NE Tail',xy=[0.05,0.9],xycoords='axes fraction')


plt_vel = numpy.zeros(len(vel[12])+2)
plt_spec = numpy.zeros(len(vel[12])+2)
plt_vel[1:-1] = vel[12]
plt_spec[1:-1] = spec[12]
plt_vel[0] = 2.*vel[12][0] - vel[12][1]
plt_vel[-1] = 2.*vel[12][-1] - vel[12][-2]

ax = axarr[3,0]
ax.step(plt_vel,1000.*plt_spec,color='k',where='mid')
ax.set_ylabel('Flux Density [mJy]')
ax.set_xlabel('$v_{\mathrm{opt}}$ [km/s]')
ax.set_xlim(3600.,4300.)
ax.set_ylim(0.,40.)
ax.annotate('NGC 848S Tail',xy=[0.05,0.9],xycoords='axes fraction')

plt_vel = numpy.zeros(len(vel[13])+2)
plt_spec = numpy.zeros(len(vel[13])+2)
plt_vel[1:-1] = vel[13]
plt_spec[1:-1] = spec[13]
plt_vel[0] = 2.*vel[13][0] - vel[13][1]
plt_vel[-1] = 2.*vel[13][-1] - vel[13][-2]

ax = axarr[3,1]
ax.step(plt_vel,1000.*plt_spec,color='k',where='mid')
ax.set_ylabel('Flux Density [mJy]')
ax.set_xlabel('$v_{\mathrm{opt}}$ [km/s]')
ax.set_xlim(vel_min,vel_max)
ax.set_ylim(0.,40.)
ax.annotate('NGC 848S loop',xy=[0.05,0.9],xycoords='axes fraction')

if save_figs:
    plt.savefig('Fig6-HCG16_tidal_spectra_indv.pdf',bbox_inches='tight')

