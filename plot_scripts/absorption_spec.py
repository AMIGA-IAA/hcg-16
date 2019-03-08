import numpy, matplotlib, os
import astropy.io.fits
from astropy import units as u
import matplotlib.pyplot as plt

font = {'size'   : 14, 'family' : 'serif', 'serif' : 'cm'}
plt.rc('font', **font)
plt.rcParams['text.usetex'] = True
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] ='gray_r'
plt.rcParams['lines.linewidth'] = 1
plt.rcParams['axes.linewidth'] = 1



c = 299792.458 #km/s

def v_opt(v_rad):
    '''Conversion from radio to optical velocity.'''
    
    return c*((1./(1.-(v_rad/c))) - 1.)

def v_rad(v_opt):
    '''Conversion from radio to optical velocity.'''
    
    return c*(1. - (1./(1.+(v_opt/c))))




#Define directories where files are stored
script_dir = os.getcwd()
casa_dir = os.path.join(script_dir,"../casa/")
sofia_dir = os.path.join(script_dir,"../sofia/")



v_hcg16d = 3874. #km/s
ra_hcg16d = 32.428870 #deg
dec_hcg16d = -10.184086 #deg



#Read in the cube and check that casa produced the correct header
filename = 'HCG16_CD_rob0_MS.pbcor.fits'
tmp = astropy.io.fits.open(casa_dir+filename)
if tmp[0].header['EQUINOX'] != 1950 or mom0[0].header['EQUINOX'] != 2000:
    tmp[0].header['EQUINOX'] = 2000
    tmp.writeto(casa_dir+filename,overwrite=True)
tmp.close()



#Reda in robust=0 cube
cube_fits = astropy.io.fits.open(casa_dir+filename)[0]

cube = cube_fits.data
cube_head = cube_fits.header

cube_dx = cube_head['CDELT1']
cube_dy = cube_head['CDELT2']
cube_dv = cube_head['CDELT3']

cube_ra = cube_head['CRVAL1'] + cube_dx * numpy.arange(1,1+cube_head['NAXIS1']) - cube_dx * cube_head['CRPIX1'] # RA
cube_dec = cube_head['CRVAL2'] + cube_dy * numpy.arange(1,1+cube_head['NAXIS2']) - cube_dy * cube_head['CRPIX2'] # Dec
cube_ch = numpy.arange(0,63)
cube_vel = cube_head['CRVAL3'] + cube_dv * numpy.arange(1,1+cube_head['NAXIS3']) - cube_dv * cube_head['CRPIX3']

bmaj,bmin,pa = cube_head['BMAJ']*3600., cube_head['BMIN']*3600., cube_head['BPA']
pixel = cube_head['CDELT1']*3600.

beam_factor = (numpy.pi*bmaj*bmin/(pixel**2.))/(4.*numpy.log(2.))



#Convert cube velocity to optical velocity
cube_vel = v_opt(cube_vel/1000.)
cube_dv = cube_dv/1000.


#Create weighting for a beam centred on HCG16d
pix_wts = numpy.zeros(numpy.shape(cube[0]))

leni,lenj = numpy.shape(pix_wts)

def gaussian2d(x, y, mux, muy, sigx, sigy):
    return numpy.exp(-numpy.power((x - mux)/sigx, 2.)/2.)*numpy.exp(-numpy.power((y - muy)/sigy, 2.)/2.)

for i in range(leni):
    for j in range(lenj):
        dec_sep = cube_dec[i]-dec_hcg16d
        
        ra_sep = (cube_ra[j]-ra_hcg16d)*numpy.cos((cube_dec[j]+dec_hcg16d)*numpy.pi/360.)
    
        pix_wts[i][j] = gaussian2d(ra_sep,dec_sep,0.,0.,bmin/(2.3548*3600.),bmaj/(2.3548*3600.))

#Apply weighting
for i in range(len(cube_vel)):
    cube[i] = cube[i]*pix_wts


absorp_spec = 1000.*numpy.nansum(numpy.nansum(cube,axis=1),axis=1)/beam_factor


#Make plot
fig = plt.subplots(figsize=(8.27,4.))

plt.step(cube_vel,absorp_spec,where='mid',c='k')
plt.axvline(v_hcg16d,c='k',ls='dashed')
plt.axhline(0.,c='k')

plt.xlabel(r'$v_\mathrm{opt}$ [km/s]')
plt.ylabel('Flux Density [mJy]')

plt.xlim(3625.,4325.)
plt.ylim(-1.6,1.6)

plt.savefig('HCG16d_absorption_spectrum.pdf',bbox_inches='tight')
