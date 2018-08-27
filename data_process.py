# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 13:48:48 2018

@author: Shi lei
"""
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
import pandas as pd
import numpy as np
import os
import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import os
import matplotlib.pylab as plt
import copy

from scipy.signal import convolve
import numpy as np
from matplotlib import pyplot as plt
from multiprocessing import Process, Queue,Pool
import itertools
from cci import CrossCorrelation,CrossCorrelation_raw,CrossCorrelation_delay,cci_list

def find_peak(y):
    Y=-1*y
    kernel = [1,-1]
    dY = convolve(Y, kernel, 'valid') 

    #Checking for sign-flipping
    S = np.sign(dY)
    ddS = convolve(S, kernel, 'valid')
    #These candidates are basically all negative slope positions
    #Add one since using 'valid' shrinks the arrays
    candidates = np.where(dY < 0)[0] + (len(kernel)+1)

    #Here they are filtered on actually being the final such position in a run of
    #negative slopes
    peaks = sorted(set(candidates).intersection(np.where(ddS == 2)[0]+1 ))
    
    #If you need a simple filter on peak size you could use:
    #alpha =-5
    #peaks = np.array(peaks)[Y[peaks] < alpha]
    #select=np.array(peaks)[Y[peaks] < alpha]
    #print(select.size)
    
    py=pd.Series(Y[peaks],index=peaks)
    py=py.sort_values()
    
    #if(select.size>100):
        #return py.index[0:200]
    #else:
        #py=pd.Series(Y[peaks],index=peaks)
        #py=py.sort_values()

        #return peaks
       # return py.index[0:90]

    return py.index[0:100]

#----------------------------------------------------------------------------
class cluster():
    thresh=0.0005
    idx=0
    count=0
    def __init__(self,idx,thresh):
        #print('process idx: ',idx)
        self.thresh=thresh
        self.count=0
        self.idx=idx
        self.peak_stat = pd.DataFrame({'index':[],'m/z':[],'count':[],'intensity':[],'intensity_min':[],'intensity_max':[]})
        self.peak_stat=self.peak_stat[['index','m/z','count','intensity','intensity_min','intensity_max']]
    def match(self,x,y):
        if (len(self.peak_stat)==0):
            self.peak_stat.loc[0]=[self.idx,x,1,y,y,y]
        else:
            match=False
            for i in range(len(self.peak_stat)):            
                if (abs(self.peak_stat.iloc[i]['m/z']-x)<x*self.thresh):
                    #print('point matched',x,self.peak_stat.iloc[i]['m/z'])
                    
                    mz=self.peak_stat.iloc[i]['m/z']
                    intensity=self.peak_stat.iloc[i]['intensity']
                    count=self.peak_stat.iloc[i]['count']
                    
                    self.peak_stat.iloc[i]['m/z']=(mz*count+x)/(count+1)         
                    self.peak_stat.iloc[i]['intensity']=(intensity*count+y)/(count+1)
                    self.peak_stat.iloc[i]['count']=self.peak_stat.iloc[i]['count']+1
                    if (self.peak_stat.iloc[i]['intensity_min']>y):
                        self.peak_stat.iloc[i]['intensity_min']=y
                    if (self.peak_stat.iloc[i]['intensity_max']<y):
                        self.peak_stat.iloc[i]['intensity_max']=y
                    match=True
                    break
                    #print(self.peak_stat.iloc[i]) 
            if(match==False):
                self.peak_stat.loc[len(self.peak_stat)]=[self.idx,x,1,y,y,y]
                #print('new point added',x)
    def match_peaks(self,px,py):
        self.count=self.count+1
        for x,y in zip(px,py):
            self.match(x,y)      
                    
    def result(self):
        #print (self.peak_stat.size)
        self.peak_stat['count']=self.peak_stat['count']/self.count
        return self.peak_stat

#--------------------------------------------------------------------------------------------

class sp_data:
    def __init__(self,data_path,thresh,ui):
        self.ui=ui
        ui.textBrowser.append('开始分析数据')
        self.df = pd.DataFrame({'ID':[],'file':[]})
        self.df =self.df[['ID','file']]
        self.raws=pd.DataFrame({'ID':[],'tof':[],'m/z':[],'intensity':[]})
        self.raws=self.raws[['ID','tof','m/z','intensity']]
        os.chdir(data_path)
        IDX=0
        frames=list()
        
        for root, dirs, files in os.walk(data_path):  
            #print(root) #当前目录路径 
            #print(dirs) #当前路径下所有子目录  
            if(len(files)>0):  
                #tags=root.split('/')
                #print(tags)
                #tag1=tags[-3]
                #tag2=tags[-1]
                #tag3=tags[-3]
                #tag4=tags[-4]
                #tag3=tag3.replace(tag4,'')
                #print(tag1,',',tag2,',',tag3,',',tag4)
                #print(len(files),' files')
                for file in files:
                    if('.csv' in file):
                        if (('大肠埃希菌' in file) & ('大肠埃希菌'  not in root)):
                            ui.textBrowser.append('侦测到“大肠埃希菌”质控数据')
                            pass
                        else:
                           # print(root+'\\'+file)
                            f=open(root+'\\'+file)
                            data=pd.read_csv(f,skiprows=1,header=None,names=['tof','m/z','intensity'])
                            col_name = data.columns.tolist()
                            col_name.insert(0,'ID')
                            self.df.reindex(columns=col_name)
                            data['ID']=IDX
                            if (data['intensity'].max()>thresh):
                                frames.append(data)
                            #container=[raws, data]
                            #raws=pd.concat(container)
                                self.df.loc[IDX]=[IDX,file]
                                IDX=IDX+1  
                                ui.textBrowser.append('添加数据文件：%s' % file)
                            else:
                                ui.textBrowser.append('低信噪比数据：%s' % file)
                                ui.textBrowser_2.append('低信噪比数据：%s' % file)
                    QApplication.processEvents()
                
        self.raws=pd.concat(frames)    
        self.raws.set_index(['ID'],inplace = True)
        self.df.set_index(['ID'],inplace = True)
        
    def normallize(self):
        for i in self.df.index:
            #print(raws_n.size[0],raws_n.size[1])
            self.raws.loc[i]['intensity']=100*self.raws.loc[i]['intensity']/self.raws.loc[i]['intensity'].max()
            #self.ui.textBrowser.append('%s 归一化完成' % self.df.loc[i]['file'])
    def peak_search(self):
        self.peak_df = pd.DataFrame({'ID':[],'m/z':[],'intensity':[]})
        self.peak_df=self.peak_df[['ID','m/z','intensity']]
        for i in self.df.index:
            x=np.array(self.raws.loc[i]['m/z'])
            y=np.array(self.raws.loc[i]['intensity'])
            peaks=find_peak(y)
            #print(x[peaks])
            #print('\b\b\b\b\b\b',i)
            for px,py in zip(x[peaks],y[peaks]):
                #print([in_out_data.iloc[i]['btype'],in_out_data.iloc[i]['extrace'],px,py])
                self.peak_df.loc[len(self.peak_df)]=[i,px,py]
        #plot.scatter(temp.loc[i,'m/z'][peak],temp.loc[i,'intensity'][peak])
        #plt.show()  
        self.peak_df.set_index(['ID'],inplace = True)
        for i in set(self.peak_df.index):    ####按照m/z排序
            self.peak_df.loc[i]=self.peak_df.loc[i].sort_values('m/z')
        #print(self.peak_df)
        #self.ui.textBrowser.append('寻峰完成')
    
    def state_peaks(self,thresh):
        clust=cluster(0,thresh)
        for i in set(self.peak_df.index):
        #print(tp,',',origin,',',gen,',',proc,',',idx)
            clust.match_peaks(self.peak_df.loc[i]['m/z'],self.peak_df.loc[i]['intensity'])  
        self.ssp=clust.result()
        #print(self.ssp)
       # print('ssp over')
       
    def get_cci(self,method):
        self.rst=[]
        for i in itertools.combinations(self.df.index, 2):
            cci=CrossCorrelation_raw(self.raws.loc[i[0]],self.raws.loc[i[1]])
            self.rst.append((i,cci))
            print(i,cci)
        self.cc_list=cci_list(self.rst,0,1)
        
            

            
        
            

        

#data=sp_data('E:/质谱建库数据20180719/2.香味类香味菌（Myroides odoratus）')
    