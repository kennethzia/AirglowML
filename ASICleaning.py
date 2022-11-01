# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 13:28:50 2022

@author: Ken
"""
########For Cleaning ASI images from DAVIS 

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import cv2
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import lightgbm as lgb
from sklearn import metrics
import glob as glob

month = ['March','April','May','June','July','August','September', 'October']#
mon = [ "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct"]# 
for i in range(0,np.size(month)):
    
    path = os.path.join(r'G:\McMurdo2012',month[i]+'2012') 
    folders=glob.glob(os.path.join(path,mon[i]+'*****'))
    
    for z in range(np.size(folders)):
        #path directs to code to the classifications folder
        
        # imgfiles=os.path.join(path,date)
        
        filesq=glob.glob(folders[z]+r'\OH_****.tif')
        v=folders[z]
        q=v.split('\\')
        # #abbreviationg the name of the months to correspond with file names 
        # month = ['January', 'February','March','April','May','June','July','August','September', 'October','November','December']
        # mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        # Year = '2020'
        # Drive='F:\\'
        
        
        
        #rotating the images in the training set to remove bias    
        rotateTr=np.random.rand(np.size(filesq))*360.0
        
        
        print(filesq[0])
        testFrame=cv2.imread(filesq[0],2)
        testFrame=testFrame    ### Dont want to normalize until after cropping  /np.max(testFrame)
        c=np.shape(testFrame)
        testFrame=testFrame[48:-48,80:-80]    #crops image
        testFrame = testFrame/np.max(testFrame)
 #       plt.imshow(testFrame)
#        plt.colorbar()
        c=np.shape(testFrame)
        a=testFrame.reshape(-1)
        np.size(a)
        
        
        
          
        
        
        Frame=np.zeros((c[0],c[1]))
        readFrame=np.zeros((c[0],c[0]))
        X_data = np.zeros((np.size(filesq),np.size(a)))
        print(np.size(a))
        for k in range(np.size(filesq)):
            butsFrame=cv2.imread(filesq[k],0) #reading
            Frame=np.double(butsFrame) #makes numpy array
            #Frame[:,:]=Frame/np.max(Frame[:,:])
            readFrame=Frame[48:-48,80:-80]     #crops 
            readFrame=readFrame/np.max(readFrame) #normalizes
            if (rotateTr[k] <= 90):  #all the if statements do the rotation
                readFrame=readFrame
            if (rotateTr[k] > 90 and rotateTr[k] < 180):
                readFrame=cv2.rotate(readFrame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            if (rotateTr[k] > 180 and rotateTr[k] < 270):
                readFrame=cv2.rotate(readFrame, cv2.ROTATE_180)
            else:
                readFrame=cv2.rotate(readFrame, cv2.cv2.ROTATE_90_CLOCKWISE)
            #cv2.imwrite(r'C:\Users\Ken\Desktop\OATHdata\oath_v1.1\images\ASI_scaled_rotated\train'+str(filesq[k])+'.png',readFrame) #write image back in to file
            readFrame = readFrame.reshape(-1) #2d array to 1d array
            X_data[k,:]= readFrame #combines all images into 2d traing set array
            
            print(str(k)+'....'+str(np.size(filesq))+'    cleaning')
        
        
        #loading Model for Davis##########################
        clf_fs = lgb.Booster(model_file=r"C:\Users\Ken\Desktop\MachineLearning\LightGBMmodels\McMurdo_Model.txt")
        
        # Running Images Thru Model
        y_pred = clf_fs.predict(X_data, num_iteration=99)
        
        #Saving Model Prediction in Date folder
        # location=os.path.join(path,date)
        
        
        #q[monthDay]
        np.savetxt(folders[z] + r'\Clean'+q[3]+'.csv',y_pred, delimiter=",")
 
##Clean 0 Dirty 1



# print('Training accuracy {:.4f}'.format(model.score(X_train,y_train)))
# print('Testing accuracy {:.4f}'.format(model.score(X_test,y_test)))

# lgb.plot_metric(model)

# metrics.plot_confusion_matrix(model,X_test,y_test,cmap='Blues')

# print(metrics.classification_report(y_test,model.predict(X_test)))

# # a=model.feature_importances_
# # b=np.reshape(a,(200,200))
# # plt.figure(figsize=(10,8))
# # plt.pcolormesh(np.log10(b),cmap='Greys' )
# # plt.colorbar(label='log10(Pixel Weights)')

# model.booster_.save_model("Zmodel.txt")
# #reading new images

# #new_path directs to code to a folder of our choice
# new_path = r'C:\Users\Ken\Davis_2012'

# the file we want is read in and saved as a data frame
#new_df = pd.read_csv(path + r'\ASI_data.csv')


#cropping them
#prediction 







### for loading 
## new predictions:
# clf_fs = lgb.Booster(model_file='model1.txt')
# y_pred2 = clf_fs.predict(X_data2, num_iteration=clf_fs.best_iteration_)[:, 1]