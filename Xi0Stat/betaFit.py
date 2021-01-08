#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 12:31:27 2020

@author: Michi
"""

from beta import Beta
from globals import *
from scipy.integrate import quad

d0O2=123 # d_0 of eq. 2.125 for O2, in Mpc
d0O3=123


def BB(dL, gamma=gammaGlob, massFunction='O3', strainSensitivity='O2'):
    #print('gamma BB: %s' %gamma)
    #print('d0 BB: %s' %d0)
    if strainSensitivity=='O2':
        d0=d0O2
    elif strainSensitivity=='O3':
        d0=d0O3
        
    a0, a1 = get_as(gamma, massFunction=massFunction)
    Bfit = np.exp(-a0*(dL-d0)/d0-a1*((dL-d0)/d0)**2)
        
    return np.where(dL<=d0, 1, Bfit)


def get_as(gamma, massFunction='O3'):
    if massFunction=='O2':
        a0= (5.21+9.55*gamma+3.47*gamma**2)*1e-02
        a1=(7.37-0.72*gamma)*1e-02
    elif massFunction=='O3':
        a0= (3.21+9.61*gamma+2.80*gamma**2)*1e-02
        a1=(8.45-0.54*gamma)*1e-02
    return a0, a1


class BetaFit(Beta):
    
    
    def __init__(self,  zR, **kwargs):
        Beta.__init__(self, **kwargs)
        self.zR=zR
        
    def get_beta(self, H0s, Xi0s, n=nGlob, **kwargs):
        '''
        Computes beta 
        from eq. 2.134
        '''
        
        H0s = np.atleast_1d(H0s)
        Xi0s = np.atleast_1d(Xi0s)
        
        
        beta = np.ones((H0s.size, Xi0s.size))
        
        for i in np.arange(H0s.size):
            
            for j in np.arange(Xi0s.size):
                             
                beta[i,j] = self._get_beta( H0=H0s[i], Xi0=Xi0s[j], n=n, **kwargs)
                                
        return np.squeeze(beta) 
       
        
    
    
    def _get_beta(self, H0, Xi0, n=1.91, **kwargs):
        #print('zR get beta: %s' %zR)
        
        #cosmo=FlatLambdaCDM(H0=H0GLOB, Om0=Om0GLOB)
        #norm = quad(lambda x: cosmo.differential_comoving_volume(x).value, 0, self.zR )[0]
        norm=quad(lambda x: j(x), 0, self.zR )[0]
        
        num = quad(lambda x: BB(dLGW(x, H0=H0, Xi0=Xi0, n=n), **kwargs)*j(x), 0, self.zR )[0]
        
        
        return num/norm
      
    
