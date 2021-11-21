
def key2(a):
    return a[3]

def key0(a):
    return a[0]

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

def brute_force_clustering(oil_rate, fuel_cons_rate,station_cost,grids)
  grids=sorted(grids,key=key2,reverse=True)
  t_stations=len(center)
  store_data=np.zeros((t_stations,t_stations))
  min_loss=float('inf')
  dist=np.zeros((t_stations,t_stations))
  assign_cluster=[float('nan')]*t_stations
  result_cluster=assign_cluster.copy()
    
  for i in range(t_stations):
    for j in range(t_stations):
      temp=distance(grids[i][0],grids[i][1],
                    grids[j][0],grids[j][1])
      dist[i][j]=temp;
      store_data[i][j]=temp;
    dist[i]=np.array(sorted(dist[i]))

  flow=np.zeros((t_stations*(t_stations-1),2))
  flow_index=0
  for i in range(t_stations):
    for j in range(1,t_stations):
        temp1=(dist[i][j]-dist[i][j-1])*grids[i][3]
        flow[flow_index][0]=temp1
        flow[flow_index][1]=i
        flow_index+=1
  flow=np.array(sorted(flow,key=key0))    

  for n_stations in range(1,t_stations+1):
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
          distance1+=min1*grids[i][3]
      
      cost=oil_rate*fuel_cons_rate*distance1 + n_stations*station_cost
      loss=cost

      if(loss<min_loss):
          min_loss=loss
          result_stations=n_stations
          result_cluster=assign_cluster.copy()
  return result_stations, result_cluster ,min_loss
