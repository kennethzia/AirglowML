# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 11:03:43 2019

@author: Kenneth
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import glob as glob
from natsort import natsorted
from scipy import interpolate
import os


plt.rcParams.update({'font.size': 15})

#Set the Station and Year as would be found on the Desktop for save-location/location of FFT analysis files
phase=r''
station = 'Davis'
year = '2020'
month1 = ['April','May','June','July','August','September']
month2 = ['Apr','May','Jun','Jul','Aug','Sep']

#Loops through months of interest
totz=0
for r in range(np.size(month1)):
    
    #Path of csv files but also need to mkdir Figures to save all these figure to.
    month=month1[r]
    months=month2[r] #Short
    monthz=month+year
    Filez=os.path.join(r"C:\Users\Ken\Desktop",year+station,month+year,months)
    MonFilez=os.path.join(r"C:\Users\Ken\Desktop",year+station,month+year)
    days=glob.glob(Filez+'*')
    number=np.size(days)
    totz = number+totz

tot=np.zeros(totz)
doy=np.zeros(totz)
o=0
for r in range(np.size(month1)):
    
    #Path of csv files but also need to mkdir Figures to save all these figure to.
    month=month1[r]
    months=month2[r] #Short
    monthz=month+year
    Filez=os.path.join(r"C:\Users\Ken\Desktop",year+station,month+year,months)
    MonFilez=os.path.join(r"C:\Users\Ken\Desktop",year+station,month+year)
    days=glob.glob(Filez+'*')
    number=np.size(days)
    
    totdata=np.zeros((300,301,number))
    
    #Loops through days that were analyzed
    for z in range(number):
        d=days[z]
        a=os.path.split(d)
        b=str(a[1])
        a=b.split('_')
        
        perpath=d
        date=months+d[0]
        
       # os.mkdir(perpath+r'\Figures')
        
        patha=perpath+'\OH_TOTAL.csv'
    
        filesa=patha    

        data=np.zeros((300,301))
        Avgdata=np.zeros((300,301))
        data3=np.zeros((300,301))
        data1=np.zeros((300,301))
        
        
        data2 = pd.read_csv(filesa)
        data1[:,:]=(data2.values)
        #To keep range from 5-150 m/s 
        data1[149-3:149+3,150-3:150+3]=np.full((6,6),-22.0)
        
        tot[o]=np.sum(10**data1[:,:])
        
        x=np.arange(-len(data)/2,len(data)/2,1)
        y=np.arange(-len(data)/2,len(data)/2,1)
        x0=np.zeros(len(data))
        y0=np.zeros(len(data))    
        
        #To keep range from 5-150 m/s      
        
        
                        
                  
        
        
        #Produces figure of Phase Speed PSD for that clean window
                    
        plt.figure(figsize=(10,8))
        data[:,:]=np.log10(10**data1[:,:])
        t=np.sum((data[:,:]))
        #t2[k]=t
        #x2[k]=k*2
        ind = np.unravel_index(np.argmax(data, axis=None), data.shape)
        xmax=float(int(ind[1])-150)
        ymax=float(int(ind[0])-150)
        psmax=np.sqrt(xmax**2+ymax**2)
        theta=np.arctan2(ymax,xmax)*180.0/(np.pi)
        
        circle1 = plt.Circle((0, 0), 50, color='k', fill=False)
        circle2 = plt.Circle((0, 0), 100, color='k', fill=False)
        circle3 = plt.Circle((0, 0), 150, color='k', fill=False)
        
        circle1 = plt.Circle((0, 0), 50, color='k', fill=False)
        circle2 = plt.Circle((0, 0), 100, color='k', fill=False)
        circle3 = plt.Circle((0, 0), 150, color='k', fill=False)
        
        circle11 = plt.Circle((0, 0), 10,linestyle=':', color='k', fill=False)
        circle21 = plt.Circle((0, 0), 20,linestyle=':', color='k', fill=False)
        circle31 = plt.Circle((0, 0), 30,linestyle=':', color='k', fill=False)
        circle41 = plt.Circle((0, 0), 40,linestyle=':', color='k', fill=False)
        
        circle12 = plt.Circle((0, 0), 110,linestyle=':', color='k', fill=False)
        circle22 = plt.Circle((0, 0), 120,linestyle=':', color='k', fill=False)
        circle32 = plt.Circle((0, 0), 130,linestyle=':', color='k', fill=False)
        circle42 = plt.Circle((0, 0), 140,linestyle=':', color='k', fill=False)
        
        circle13 = plt.Circle((0, 0), 60,linestyle=':', color='k', fill=False)
        circle23 = plt.Circle((0, 0), 70,linestyle=':', color='k', fill=False)
        circle33 = plt.Circle((0, 0), 80,linestyle=':', color='k', fill=False)
        circle43 = plt.Circle((0, 0), 90,linestyle=':', color='k', fill=False)
        
        
        ####################Actual Mesh Plot
        plt.pcolormesh(x,y,(data[:,:-1]),cmap='jet',vmin=-10,vmax=np.max(data))#-4)#,vmax=np.max(data))#100)
        plt.colorbar(label='log$_{10}$(PSD)')
        
        totdata[:,:,z]=data[:,:]
        plt.plot()
        plt.title('Average')

        
        plt.plot(x0,y,color='k',lw='0.5')
        plt.plot(x,y0,color='k',lw='0.5')
        plt.gcf().gca().add_artist(circle1)
        plt.gcf().gca().add_artist(circle2)
        plt.gcf().gca().add_artist(circle3)
        plt.gcf().gca().add_artist(circle11)
        plt.gcf().gca().add_artist(circle21)
        plt.gcf().gca().add_artist(circle31)
        plt.gcf().gca().add_artist(circle41)
        plt.gcf().gca().add_artist(circle12)
        plt.gcf().gca().add_artist(circle22)
        plt.gcf().gca().add_artist(circle32)
        plt.gcf().gca().add_artist(circle42)
        plt.gcf().gca().add_artist(circle13)
        plt.gcf().gca().add_artist(circle23)
        plt.gcf().gca().add_artist(circle33)
        plt.gcf().gca().add_artist(circle43)

        
        plt.xticks(np.arange(-150,150,50))
        plt.yticks(np.arange(-150,150,50))
        
        plt.xlim(-100,100)
        plt.ylim(-100,100)
        plt.xlabel('W-E [m/s]')
        plt.ylabel('N-S [m/s]')
        
        
        plt.show()
        # Save Name and Location
        plt.savefig(os.path.join(MonFilez,a[0]+"OH_"+str(z)+".jpg"))
        
        o=o+1
            
    #Produces Monthly Average Plot
            
    plt.figure(figsize=(10,8))
    data[:,:]=np.log10(np.mean(10**totdata[:,:,:],2))
    t=np.sum((data[:,:]))
    
    circle1 = plt.Circle((0, 0), 50, color='k', fill=False)
    circle2 = plt.Circle((0, 0), 100, color='k', fill=False)
    circle3 = plt.Circle((0, 0), 150, color='k', fill=False)
    
    circle1 = plt.Circle((0, 0), 50, color='k', fill=False)
    circle2 = plt.Circle((0, 0), 100, color='k', fill=False)
    circle3 = plt.Circle((0, 0), 150, color='k', fill=False)
    
    circle11 = plt.Circle((0, 0), 10,linestyle=':', color='k', fill=False)
    circle21 = plt.Circle((0, 0), 20,linestyle=':', color='k', fill=False)
    circle31 = plt.Circle((0, 0), 30,linestyle=':', color='k', fill=False)
    circle41 = plt.Circle((0, 0), 40,linestyle=':', color='k', fill=False)
    
    circle12 = plt.Circle((0, 0), 110,linestyle=':', color='k', fill=False)
    circle22 = plt.Circle((0, 0), 120,linestyle=':', color='k', fill=False)
    circle32 = plt.Circle((0, 0), 130,linestyle=':', color='k', fill=False)
    circle42 = plt.Circle((0, 0), 140,linestyle=':', color='k', fill=False)
    
    circle13 = plt.Circle((0, 0), 60,linestyle=':', color='k', fill=False)
    circle23 = plt.Circle((0, 0), 70,linestyle=':', color='k', fill=False)
    circle33 = plt.Circle((0, 0), 80,linestyle=':', color='k', fill=False)
    circle43 = plt.Circle((0, 0), 90,linestyle=':', color='k', fill=False)
    
    
    
    plt.pcolormesh(x,y,data[:,:-1],cmap='jet',vmin=-10,vmax=np.max(data))#100)
    plt.colorbar(label='log$_{10}$(PSD)')
    
    plt.plot()
    plt.title(month1[r]+'Average')
    
    plt.plot(x0,y,color='k',lw='0.5')
    plt.plot(x,y0,color='k',lw='0.5')
    plt.gcf().gca().add_artist(circle1)
    plt.gcf().gca().add_artist(circle2)
    plt.gcf().gca().add_artist(circle3)
    plt.gcf().gca().add_artist(circle11)
    plt.gcf().gca().add_artist(circle21)
    plt.gcf().gca().add_artist(circle31)
    plt.gcf().gca().add_artist(circle41)
    plt.gcf().gca().add_artist(circle12)
    plt.gcf().gca().add_artist(circle22)
    plt.gcf().gca().add_artist(circle32)
    plt.gcf().gca().add_artist(circle42)
    plt.gcf().gca().add_artist(circle13)
    plt.gcf().gca().add_artist(circle23)
    plt.gcf().gca().add_artist(circle33)
    plt.gcf().gca().add_artist(circle43)

    
    plt.xticks(np.arange(-150,150,50))
    plt.yticks(np.arange(-150,150,50))
    
    plt.xlim(-100,100)
    plt.ylim(-100,100)
    plt.xlabel('W-E [m/s]')
    plt.ylabel('N-S [m/s]')
    
    
    plt.show()
    plt.savefig(os.path.join(MonFilez,month2[r]+"AVG.jpg"))

plt.figure()
plt.plot(tot)
plt.yscale('log')
plt.savefig(os.path.join(MonFilez,'totalPow.jpg'))
    
    
