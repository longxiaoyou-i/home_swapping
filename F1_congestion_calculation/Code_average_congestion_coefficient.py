# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 15:33:50 2023

@author: Czhao_Team
"""
def road_speed():
    dic_route_speed={} #Speed limits on different roads
    file_route_type='D:/main_code/4_congestion_calculation/sample_rode_types.txt'
    with open(file_route_type,'r')as f:
        for row in f.readlines():
            row=row.strip().split()
            if row[2]=='0' or '1':
                dic_route_speed[(row[0],row[1])]=100
            if row[2]=='2' or '3' or '4':
                dic_route_speed[(row[0],row[1])]=60
            if row[2]=='5':
                dic_route_speed[(row[0],row[1])]=30
            if row[2]=='6':
                dic_route_speed[(row[0],row[1])]=40
            if row[2]=='7':
                dic_route_speed[(row[0],row[1])]=50
    return dic_route_speed

def real_road_congestion_coffcient(dic_route_speed):
    dic_road={}     
    file_route='D:/main_code/4_congestion_calculation/sample_actual_7-8.txt'
    with open(file_route,'r')as f:
        for row in f.readlines():
            row=row.strip().split()
            number_vechile=int(row[2])
            if (row[0],row[1]) in dic_route_speed:
                speed=dic_route_speed[(row[0],row[1])]
                n_max=(1000*speed)/(4+speed)
                if number_vechile/n_max>=0.4:  #Evidence of congested and slowed road sections
                    dic_road[row[0],row[1]]=number_vechile/n_max   
    return dic_road
                    
def calculate_congestion_coffcient(dic_road):                
    s_index=0 
    file_route='D:/main_code/4_congestion_calculation/sample_actual_7-8.txt'
    with open(file_route,'r')as f:
        for row in f.readlines():
            row=row.strip().split()
            number_vechile=int(row[2])
            if (row[0],row[1]) in dic_route_speed:
                if (row[0],row[1]) in dic_road:
                    speed=dic_route_speed[(row[0],row[1])]
                    n_max=(1000*speed)/(4+speed)
                    s_index=s_index+(number_vechile/n_max)
    aver_index=s_index/len(dic_road)
    print(aver_index)   #Evidence-based average congestion cofficient
    
    s_index=0 
    file_route='D:/main_code/4_congestion_calculation/sample_GHS_7-8.txt'
    with open(file_route,'r')as f:
        for row in f.readlines():
            row=row.strip().split()
            number_vechile=int(row[2])
            if (row[0],row[1]) in dic_route_speed:
                if (row[0],row[1]) in dic_road:
                    speed=dic_route_speed[(row[0],row[1])]
                    n_max=(1000*speed)/(4+speed)
                    s_index=s_index+(number_vechile/n_max)
    aver_index=s_index/len(dic_road)
    print(aver_index) #after swapping home  average congestion cofficient
    
    
if __name__ == '__main__' :
    dic_route_speed=road_speed()
    dic_road= real_road_congestion_coffcient(dic_route_speed)
    calculate_congestion_coffcient(dic_road)
                

