#using heuristic transhipment station genration algorithm (Algorithm 2) COBAC (Algotihm 5) is implemented
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
    t_stations=len(center)
    n_stations_prev=n_stations
    result_stations=n_stations
    max_iter=n_iter
    store_data=np.zeros((t_stations,t_stations))
    assign_cluster=[float('nan')]*t_stations
    result_cluster=assign_cluster.copy()
    min_loss=float('inf')
    dist=np.zeros((t_stations,t_stations))
  

    for i in range(t_stations):
      for j in range(t_stations):
        temp=distance(center_info[i][0],center_info[i][1],
                      center_info[j][0],center_info[j][1])
        dist[i][j]=temp;
        store_data[i][j]=temp;
      dist[i]=np.array(sorted(dist[i]))

    flow=np.zeros((t_stations,2))
    flow_index=0
    for i in range(t_stations):
          temp1=(dist[i][2]-dist[i][1])*center_info[i][3]
          flow[flow_index][0]=temp1
          flow[flow_index][1]=i
          flow_index+=1
    flow=np.array(sorted(flow,key=key0))    

    while(n_iter!=0):
        flow_index=0
        reference=[0]*t_stations
        count=t_stations

        while(count!=n_stations):
          if(reference[int(flow[flow_index][1])]==0):
            reference[int(flow[flow_index][1])]=1
            count-=1
          flow_index+=1 

        target=[]
        for i in range(t_stations):
          if(reference[i]==0):
            target.append(i)                     

        for i in target:
         assign_cluster[i]=i
    
        distance1=0.0
        for i in range(t_stations):
            min1=float('inf')
            for j in target:
                if(store_data[i][j]<min1):
                  min1=store_data[i][j]      
            distance1+=min1*center_info[i][3]
        
        cost=oil_rate*fuel_cons_rate*distance1 + n_stations*station_cost
        loss=cost
        
        
        if(loss<min_loss):
            result_cluster=assign_cluster.copy()
            min_loss=loss
            result_stations=n_stations
          
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
        elif(growth_rate>0 and n_stations==len(center)):
            growth_rate=-10
        else:    
          growth_rate=growth_rate - np.sign(deriv)*param
        n_stations=min(max(transform(growth_rate)+n_stations,10),len(center))
        n_iter-=1
    return result_cluster,center_info,min_loss,result_stations,target 