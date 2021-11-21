#script for final clustering 
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import pickle
from shapely.geometry import Polygon,Point

#start=time.time()

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


crunch=pd.read_csv("FishTank_dataset.csv")  

country=load_obj('country_index')
rfmo_dic3=load_obj('rfmo_country_map')
area=load_obj('rfmo_area')

def key(a):
    return a[1]

def cluster_center(data):
    lat=0.0
    lon=0.0
    for i in range(len(data)):
        lat+=data[i][0]
        lon+=data[i][1]
    lat=lat/len(data)
    lon=lon/len(data)
    return [lat,lon]

def check_rfmo(interupt,center,data):
    for a in rfmo_dic3.keys():
        flag=1
        for i in interupt:
          if(rfmo_dic3[a][country[i]]==0):
              flag=0
              break
        if(flag==1):
#            inner=Polygon(area[a][0])
            outer=Polygon(area[a][1])
            p=Point(center[1],center[0])
            if(p.within(outer)):
                  return a,data
            else:
                flag=0
    if(flag==0):
        dt=pd.DataFrame(data,columns=['1','2','3','4'])
        l1=list(dt.groupby('3'))
        per=0.0
        ans1=None
        ans2=data
        for a in rfmo_dic3.keys():
            count=0.0
            ret=[]
            for i in range(len(l1)):
                temp=l1[i][1].values
                if(rfmo_dic3[a][country[temp[0][3]]]==1):
                    ret.extend(temp)
                    count+=1
            if(count/float(len(l1))>=0.70 and count/float(len(l1))>per):
                per=count/float(len(l1))
                ans1=a
                ans2=ret
        return ans1,ans2
        
        
def grid_generation(data,dist):
    data=data.sort_values(['lat_bin','lon_bin'],ascending=[1,1])
    data=data.values
    dic={}
    serial=0
    flag=data[0][1]
    dic[serial]=[]
    dic[serial].append([data[0][1],data[0][2],data[0][5],data[0][3]])
    for i in range(1,len(data)):
        if(flag+dist>data[i][1]):
            dic[serial].append([data[i][1],data[i][2],data[i][5],data[i][3]])
        else:
            serial+=1
            dic[serial]=[]
            dic[serial].append([data[i][1],data[i][2],data[i][5],data[i][3]])
            flag=data[i][1]
    
    serial2=0
    dic2={}
    center=[]
    
    for i in dic.values():
        i=sorted(i,key=key)
        interupt=set([])
        mmsi=set([])
        dic2[serial2]=[]
        dic2[serial2].append([i[0][0],i[0][1],i[0][3],i[0][2]])
        interupt.add(i[0][2])
        mmsi.add(i[0][3])
        flag=i[0][1]
        for j in range(1,len(i)):
            if(flag+dist>i[j][1]):
                dic2[serial2].append([i[j][0],i[j][1],i[j][3],i[j][2]])
                interupt.add(i[j][2])
                mmsi.add(i[j][3])
            else:
                cluster_center_data=cluster_center(dic2[serial2])
                crfmo,dic2[serial2]=check_rfmo(interupt,cluster_center_data,dic2[serial2])
                center.append(cluster_center_data+[crfmo]+[len(mmsi)])
                interupt=set([])
                mmsi=set([])
                serial2+=1
                dic2[serial2]=[]
                dic2[serial2].append([i[j][0],i[j][1],i[j][3],i[j][2]])
                interupt.add(i[j][2])
                mmsi.add(i[j][3])
                flag=i[j][1]
    cluster_center_data=cluster_center(dic2[serial2])
    crfmo=check_rfmo(interupt,cluster_center_data,dic2[serial2])
    center.append(cluster_center_data+[crfmo]+[len(mmsi)])            
    return dic2,np.array(center)            

cluster,center=grid_generation(crunch,2)


