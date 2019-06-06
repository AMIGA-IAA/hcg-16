#This file stores a collection of basic function used in a number of the accompanying notebooks.
#Some constants used throughout are also set here.

import numpy, astropy.io.fits


#Constants:
#Distance to HCG 16
dist = 55.2 #Mpc
#Error in distance to HCG 16
err_dist = 3.3 #Mpc
#Speed of light
c = 299792.458 #km/s
#HI line rest frequency
f0 = 1420.405751/1000. #GHz
#Hubble constant
H0 = 70. #km/s/Mpc
h = H0/100.
#Redshift of HCG 16 member galaxies (from optical lines)
v_grp = 3957. #km/s
v_hcg16a = 4073. #km/s
v_hcg16b = 3864. #km/s
v_hcg16c = 3849. #km/s
v_hcg16d = 3874. #km/s
v_hcg16n = 4045. #km/s #NGC 848
v_hcg16p = 3972. #km/s #PGC 8210

#Positions of HCG 16 members
ra_hcg16a = 32.352519 
ra_hcg16b = 32.336845
ra_hcg16c = 32.4105329
ra_hcg16d = 32.428870
ra_hcg16n = 32.573518 #NGC 848
ra_hcg16p = 32.275081 #PGC 8210

dec_hcg16a = -10.135923
dec_hcg16b = -10.133093
dec_hcg16c = -10.1466869
dec_hcg16d = -10.184086
dec_hcg16n = -10.321447 #NGC 848
dec_hcg16p = -10.320226 #PGC 8210

#Functions
def gaussian(x, mu, sig):
    '''
    Gaussian with mean mu and standard deviation sig.
    
    Inputs:
        x: Independent variable.
        mu: Mean of Gaussian distribution.
        sig: Standard deviation of Gaussian.
        
    Outputs:
        y: Value of Gaussian distribution at x.
    '''
    
    return numpy.exp(-numpy.power((x - mu)/sig, 2.)/2.)

def v_rad(v_opt):
    '''
    Conversion from optical to radio velocity.
    
    Inputs:
        v_opt: Optical velocity [km/s].
        
    Outputs:
        v_rad: Radio velocity [km/s].
    '''
    
    return c*(1. - (1./(1.+(v_opt/c))))

def v_opt(v_rad):
    '''
    Conversion from radio to optical velocity.
    
    Inputs:
        v_rad: Radio velocity [km/s].
        
    Outputs:
        v_opt: Optical velocity [km/s].
    '''
    
    return c*((1./(1.-(v_rad/c))) - 1.)

def logMHI_pred(B_c,D,B_c_err,D_err):
    '''
    Predicts HI mass of a galaxy given its B-band luminosity following Jones et al. 2018, A&A 609A, 17J.
    
    Inputs:
        B_c = Extinction and k-corrected B-band apparent magnitude.
        D = Source luminoisty distance [Mpc].
        B_c_err = Error in B_c.
        D_err = Error in D [Mpc].
        
    Outputs:
        logMHI = Logarithm of the predicted HI mass [Msol].
        logMHI_err = Error in logMHI.
    '''
    
    logD = numpy.log10(D)
    logD_err = D_err/(D*numpy.log(10.))
    
    logLB = 10. + 2.*numpy.log10(D) + 0.4*(4.88-B_c)
    
    logMHI = 0.94*logLB + 0.18
    
    logMHI_err = numpy.sqrt(0.2**2. + (0.94**2.)*((0.4*B_c_err)**2. + (2.*logD_err)**2.))
    
    return logMHI,logMHI_err

def read_fitscube(filename,need_beam=False,widths=False,verbose=False):
    '''
    Reads a fits cube that is RA, Dec, Vel and builds the axes.
    
    Inputs:
        filename = String indicating the full location of the fits file.
        need_beam = Boolean indicating whether to return beam dimensions.
        widths = Boolean indicating whether to return axes step sizes.
        verbose = Boolean indicating whether to print all output.
        
    Outputs:
        cube = The data values from the fits file.
        cube_ra = Right ascension axis values [deg].
        cube_dec = Declination axis values [deg].
        cube_vel = Velocity axis values [km/s].
        bmaj = (if need_beam) Beam major axis diameter [arcsec].
        bmin = (if need_beam) Beam major axis diameter [arcsec].
        pa = (if need_beam) Beam position angle [deg].
        beam_factor = (if need_beam) Ratio of beam area to pixel area.
        cube_dx = (if widths) RA axis step size [deg].
        cube_dy = (if widths) Dec axis step size [deg].
        cube_dv = (if widths) Velocity axis step size [km/s].
    '''
    
    cube_fits = astropy.io.fits.open(filename)

    cube = cube_fits[0].data
    cube_head = cube_fits[0].header

    cube_dx = cube_head['CDELT1']
    cube_dy = cube_head['CDELT2']
    cube_dv = cube_head['CDELT3']

    cube_ra = cube_head['CRVAL1'] + cube_dx * numpy.arange(1,1+cube_head['NAXIS1']) - cube_dx * cube_head['CRPIX1'] # RA
    cube_dec = cube_head['CRVAL2'] + cube_dy * numpy.arange(1,1+cube_head['NAXIS2']) - cube_dy * cube_head['CRPIX2'] # Dec
    cube_vel = cube_head['CRVAL3'] + cube_dv * numpy.arange(1,1+cube_head['NAXIS3']) - cube_dv * cube_head['CRPIX3']

    if 'm/s' == str.strip(cube_head['CUNIT3']):
        if verbose:
            print("Velocity units are m/s. Converting to km/s.")
        cube_vel = cube_vel/1000. #km/s
        cube_dv = cube_dv/1000. #km/s
    elif 'km/s' == str.strip(cube_head['CUNIT3']):
        if verbose:
            print("Velocity units are km/s.")
        pass
    else:
        print("Warning: Velocity units not recognised.")
        print("Warning: Units listed as: "+cube_head['CUNIT3'])
    
    if 'OPT' in str(cube_head['CTYPE3']) or 'opt' in str(cube_head['CTYPE3']):
        if verbose:
            print("Velocity convention is optical.")
        pass
    elif 'RAD' in str(cube_head['CTYPE3']) or 'rad' in str(cube_head['CTYPE3']):
        if verbose:
            print("Velocity convention is radio. Converting to optical.")
        cube_vel = v_opt(cube_vel)
    else:
        print("Warning: Could not identify radio or optical velocity convention.")
        print("Warning: Convention listed as: "+cube_head['CTYPE3'])

    bmaj,bmin,pa = cube_head['BMAJ']*3600.,cube_head['BMIN']*3600., cube_head['BPA']
    pixel = cube_head['CDELT2']*3600.

    beam_factor = (numpy.pi*bmaj*bmin/(pixel**2.))/(4.*numpy.log(2.))
    
    
    if need_beam and widths:
        return cube,cube_ra,cube_dec,cube_vel,bmaj,bmin,pa,beam_factor,cube_dx,cube_dy,cube_dv
    elif need_beam:
        return cube,cube_ra,cube_dec,cube_vel,bmaj,bmin,pa,beam_factor
    elif widths:
        return cube,cube_ra,cube_dec,cube_vel,cube_dx,cube_dy,cube_dv
    else:
        return cube,cube_ra,cube_dec,cube_vel