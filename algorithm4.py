#using random transhipment station genration algorithm (Algorithm 4) COBAC is implemented
#Algorithm 4 is not implemented as a separate function but rather is included in the code of COBAC implicitly

def transform(a): 
    if(a<1 and a>=0):
        return 1
    elif(a>-1 and a<0):
        return -1
    else:
       try: 
        return floor(a)
       except:
        print(a)
        input()

def distance(lat1,lon1,lat2,lon2):
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


def adaptive_search_clustering(budget,oil_rate,fuel_cons_rate,station_cost,n_stations=200,growth_rate=10,n_iter=500):
    center_info=sorted(center,key=key2,reverse=True)
    n_stations_prev=n_stations
    max_iter=n_iter
    store_data=np.zeros((len(center_info),len(center_info)))
    assign_cluster=[float('nan')]*len(center_info)
    result_cluster=assign_cluster.copy()
    min_loss=float('inf')
    

    while(n_iter!=0):
        distance1=0
        
        main_station=set()
        while(len(main_station)!=n_stations):
            main_station.add(random.randint(0,2359))
        
        assign_cluster=[float('nan')]*len(center_info)
        for i in main_station:
            assign_cluster[i]=i
    
        side_station=[]
        for i in range(len(center_info)):
            if(assign_cluster[i]!=assign_cluster[i]):
                side_station.append(i)
        
        for i in side_station:
            min1=float('inf')
            for j in main_station:
                if(store_data[i][j]==0):
                    store_data[i][j]=distance(center_info[i][0],center_info[i][1],
                                              center_info[j][0],center_info[j][1])
                    store_data[j][i]=store_data[i][j]
                if(store_data[i][j]<min1):
                        min1=store_data[i][j]
                        assign_cluster[i]=j
            distance1+=min1*center_info[i][3]
            

        cost=oil_rate*fuel_cons_rate*distance1 + n_stations*station_cost
        loss=cost
        
        
        if(loss<min_loss):
            result_cluster=assign_cluster.copy()
            min_loss=loss
          
        if(max_iter!=n_iter):
          try:
           change=((n_stations-n_stations_prev)/(n_stations_prev))
           deriv=((loss-prev_loss)/(prev_loss))/change
           if(deriv!=deriv):
               print(n_stations," ",n_stations_prev)
               print(loss," ",prev_loss)
          except:
           deriv=(loss-prev_loss)/prev_loss
           if(deriv!=deriv):
               print(loss," ",prev_loss)
               
           
        else:
          deriv=-1*(random.randint(0,5)/100)
          sign=np.sign(deriv)
          prev_sign=sign
          param=2
               
        n_stations_prev=n_stations
        prev_loss=loss
        
        if(prev_sign==sign):
            param=param*(0.5+abs(deriv))
        else:
            param=2
            param=param*(0.5+abs(deriv))
            
        prev_sign=sign
        sign=np.sign(deriv)
        
        
        if(growth_rate<0 and n_stations==10):
            growth_rate=10
        elif(growth_rate>0 and n_stations==2360):
            growth_rate=-10
        else:    
          growth_rate=growth_rate - np.sign(deriv)*param
        n_stations=min(max(transform(growth_rate)+n_stations,10),2360)

        n_iter-=1
    return result_cluster,center_info,min_loss 
