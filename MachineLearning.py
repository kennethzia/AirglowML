# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 14:20:32 2022

@author: Ken
"""

#https://www.kaggle.com/code/prashant111/lightgbm-classifier-in-python/notebook
#https://www.analyticsvidhya.com/blog/2021/08/complete-guide-on-how-to-use-lightgbm-in-python/
#https://lightgbm.readthedocs.io/en/latest/Python-Intro.html#training

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


#Input image data parameters
Station = 'Rothera'
Year = '2017'
#Path to folders with "MonthYear" with no space in between!
Drive=r'H:/ircam/2017/data'


#path directs to code to the classifications folder
path = r'C:\Users\Ken\Desktop\MachineLearning\LabeledImages'

# the ASI_data.cvs file is read in and saved as a data frame
df = pd.read_csv(os.path.join(path ,Station+'_ASI_Data.csv'))

#df is split into a trainging and test data frame
train,test = train_test_split(df, test_size=0.30, random_state=0)
df_train = pd.DataFrame(train)
df_test = pd.DataFrame(test)

#the new training and testing data frames are saved within the classifications folder
# df_train.to_csv(os.path.join(path ,Station+'ASI_train.csv'), index=False)
# df_test.to_csv(os.path.join(path ,Station+'ASI_test.csv'), index=False)

#Training Set Image Location
imgnumTr=df_train['Frame'].to_numpy() #puts each images frame into to_numpy
imgdateTr=df_train['Date'].to_numpy() #puts each images date into to_numpy
imgfilesTr=['']*(np.size(imgnumTr))
filesqTr=['']*(np.size(imgnumTr))
#abbreviationg the name of the months to correspond with file names 
month = ['January', 'February','March','April','May','June','July','August','September', 'October','November','December']
mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

for i in range(np.size(imgnumTr)):
    a=imgdateTr[i]
    ax = a[0]+a[1]+a[2]
    index=mon.index(ax)
    imgfilesTr[i]=os.path.join(Drive,month[int(index)]+Year,imgdateTr[i])
    filesqTr[i]=os.path.join(imgfilesTr[i],'OH_'+str(imgnumTr[i]).zfill(4)+'.tif')
    filesqTr[i] = os.path.normpath(filesqTr[i])

#rotating the images in the training set to remove bias    
rotateTr=np.random.rand(np.size(imgnumTr))*360.0

y_train=df_train['Class2'].to_numpy()

#Testing Set Image Location 
imgnumTe=df_test['Frame'].to_numpy()
imgdateTe=df_test['Date'].to_numpy()
imgfilesTe=['']*(np.size(imgnumTe))
filesqTe=['']*(np.size(imgnumTe))



for i in range(np.size(imgnumTe)):
    a=imgdateTe[i]
    ax = a[0]+a[1]+a[2]
    index=mon.index(ax)
    imgfilesTe[i]=os.path.join(Drive,month[int(index)]+Year,imgdateTe[i])
    imgfilesTe[i] = os.path.normpath(imgfilesTe[i])
    
    filesqTe[i]=os.path.join(imgfilesTe[i],'OH_'+str(imgnumTe[i]).zfill(4)+'.tif')
    filesqTe[i] = os.path.normpath(filesqTe[i])
    
rotateTe=np.random.rand(np.size(imgnumTe))*360.0
y_test=df_test['Class2'].to_numpy()

print(filesqTr[0])
testFrame=cv2.imread(filesqTr[0],2)
testFrame=testFrame    ### Dont want to normalize until after cropping  /np.max(testFrame)
c=np.shape(testFrame)
testFrame=testFrame[48:-48,80:-80]    #crops image
testFrame = testFrame/np.max(testFrame)
plt.imshow(testFrame)
plt.colorbar()
c=np.shape(testFrame)
a=testFrame.reshape(-1)
np.size(a)



  


Frame=np.zeros((c[0],c[1]))
readFrame=np.zeros((c[0],c[0]))
X_train = np.zeros((np.size(imgnumTr),np.size(a)))
print(np.size(a))
for k in range(np.size(imgnumTr)):
    butsFrame=cv2.imread(filesqTr[k],0) #reading
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
    #cv2.imwrite(r'C:\Users\Ken\Desktop\OATHdata\oath_v1.1\images\ASI_scaled_rotated\train'+str(imgnumTr[k])+'.png',readFrame) #write image back in to file
    readFrame = readFrame.reshape(-1) #2d array to 1d array
    X_train[k,:]= readFrame #combines all images into 2d traing set array
    
    print(str(k)+'....'+str(np.size(imgnumTr))+'training')

X_test = np.zeros((np.size(imgnumTe),np.size(a)))
for k in range(np.size(imgnumTe)):
    testFrame=cv2.imread(filesqTe[k],0) #reading
    Frame=np.double(testFrame) #makes numpy array
    readFrame=Frame[48:-48,80:-80] #crops
    readFrame=readFrame/np.max(readFrame) #normalizes
    if (rotateTe[k] <= 90): #rotates
        readFrame=readFrame
    if (rotateTe[k] > 90 and rotateTe[k] < 180):
        readFrame=cv2.rotate(readFrame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    if (rotateTe[k] > 180 and rotateTe[k] < 270):
        readFrame=cv2.rotate(readFrame, cv2.ROTATE_180)
    else:
        readFrame=cv2.rotate(readFrame, cv2.cv2.ROTATE_90_CLOCKWISE)
    #cv2.imwrite(r'C:\Users\Ken\Desktop\OATHdata\oath_v1.1\images\ASI_scaled_rotated\test'+str(imgnumTe[k])+'.png',readFrame) #writes image back into file
    X_test[k,:]=readFrame.reshape(-1)   #2d array to 1d array
    print(str(k)+'....'+str(np.size(imgnumTe))+'testing') 



# Reports accuracy and precision of ml code
model = lgb.LGBMClassifier(learning_rate=0.09,max_depth=-5)
model.fit(X_train,y_train,eval_set=[(X_test,y_test),(X_train,y_train)],
          verbose=20,eval_metric='logloss')

print('Training accuracy {:.4f}'.format(model.score(X_train,y_train)))
print('Testing accuracy {:.4f}'.format(model.score(X_test,y_test)))

lgb.plot_metric(model)

metrics.plot_confusion_matrix(model,X_test,y_test,cmap='Blues')

print(metrics.classification_report(y_test,model.predict(X_test)))



model.booster_.save_model(os.path.join(r'C:\Users\Ken\Desktop\MachineLearning\LightGBMmodels',Station+"_Model.txt"))
#reading new images



# the file we want is read in and saved as a data frame
#new_df = pd.read_csv(path + r'\ASI_data.csv')


#cropping them
#prediction 

# a=model.feature_importances_
# b=np.reshape(a,(200,200))
# plt.figure(figsize=(10,8))
# plt.pcolormesh(np.log10(b),cmap='Greys' )
# plt.colorbar(label='log10(Pixel Weights)')





### for loading 
## new predictions:
# clf_fs = lgb.Booster(model_file='model1.txt')
# y_pred2 = clf_fs.predict(X_data2, num_iteration=clf_fs.best_iteration_)[:, 1]

