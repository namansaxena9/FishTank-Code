def station_generation(heuristic,n_stations,n_grids):
        index=0
        reference=[0]*n_grids
        count=n_grids

        while(count!=n_stations):
          if(reference[int(heuristic[index][1])]==0):
            reference[int(heuristic[index][1])]=1
            count-=1
          index+=1 

        station=[]
        for i in range(n_grids):
          if(reference[i]==0):
            station.append(i)                     

        return station
