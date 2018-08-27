#coding=utf-8 
import pandas as pd
import numpy as np
import itertools

def CrossCorrelation(sp1,sp2,delay=0,thresh=0.0005):
    score=0
    for i in range(len(sp1)):
        for j in range(len(sp2)):
            if (abs(sp1.iloc[i]['m/z']-sp2.iloc[j]['m/z']-delay)<sp1.iloc[i]['m/z']*thresh):
                if ((sp1.iloc[i]['intensity']>3) & (sp2.iloc[j]['intensity']>3)):
                    score=score+sp1.iloc[i]['intensity']*sp2.iloc[j]['intensity']/10000
                break
    return score,0    

def CrossCorrelation_raw(sp1,sp2,delay=0):
    a=np.array(sp1['intensity'])
    b=np.array(sp2['intensity'])
    a=np.where(a<5,0,a)
    b=np.where(b<5,0,b)
    c=a[0:50000]*b[0:50000]/10000
    return c.sum(),0
    #for i in range(50000):
        #if ((sp1.iloc[i]['intensity']>5)&(sp2.iloc[i]['intensity']>5)):
            #score=score+sp1.iloc[i]['intensity']*sp2.iloc[i]['intensity']                
    #return score   
    
def CrossCorrelation_delay(sp1,sp2,move_range=30):
    score_max=0
    delay_max=0
    a=np.array(sp1['intensity'])
    b=np.array(sp2['intensity'])
    a=np.where(a<5,0,a)
    b=np.where(b<5,0,b)
    for i in np.arange(-1*move_range,move_range,1):
        ac=a[move_range+i:-1*move_range+i]
        bc=b[move_range:-1*move_range]
        
        c=ac[0:48000]*bc[0:48000]/10000  
        sc=c.sum()        
        if (sc>score_max):
            score_max=sc
            delay_max=i
        #print(i,c.sum())  
    return score_max,delay_max

def index_cbn(rst,ia,ib,index_col,rst_col):
    for data in rst:
        condition1=(data[index_col][0]==ia) and (data[index_col][1]==ib)
        condition2=(data[index_col][0]==ib) and (data[index_col][1]==ia)
        if (condition1 and condition2):
            rtn=data[rst_col]
            break
    return rtn


        
class cci_list:
    def __init__(self,data,index_col=0,data_col=1):
        self.data=data
        self.index_col=index_col
        self.data_col=data_col
        
        
    def index(self,ia,ib):
        for d in self.data:
            condition1=(d[self.index_col][0]==ia) and (d[self.index_col][1]==ib)
            condition2=(d[self.index_col][0]==ib) and (d[self.index_col][1]==ia)
            if (condition1 and condition2):
                rtn=d[self.data_col]
                break
        return rtn
        
    def averange(self,idx):
        rst=[]
        for d in self.data:
            if (d[self.index_col][0]==idx) or (d[self.index_col][1]==idx):
                rst.append(d[self.data_col])
        buff=[]
        for i in rst:
            buff.append(i[0])
        rtn=np.array(buff)  
        
        if(len(rtn)>0):
            return rtn.sum()/len(rtn)
        else:
            return 0
            
    
            
    