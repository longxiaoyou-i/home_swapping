# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 16:47:46 2023

@author: Czhao_Team
"""
import random
import copy

#commuting distance
def get_distance(lon_a, lat_a, lon_b, lat_b):
    home = str(lat_a) + ',' + str(lon_a)
    work = str(lat_b) + ',' + str(lon_b)
    if point_center_linkid[home][2]==point_center_linkid[work][2]:
        home_center=point_center_linkid[home][0]
        work_center=point_center_linkid[work][0]
    else:
        home_center=point_center_linkid[home][1]
        work_center=point_center_linkid[work][1]
    if home_center==work_center:
        distance=0
    else:
        distance=center_distance[(home_center,work_center)]
    return distance

#original total commuting distance
def actual_total_commuting_distance():
    dic_id_home_workplace={}  
    dic_dis={}  
    pid=[]  
    filePath='D:/main_code/2_home_swapping/sample_commuter_home_workplace.txt'  
    with open(filePath,'r')as f:
        for row in f.readlines():
            row=row.strip().split()    
            row_1=row[1].split(',')            
            row_2=row[2].split(',')            
            LatA = float(row_1[0])
            LonA = float(row_1[1])
            LatB = float(row_2[0])
            LonB = float(row_2[1])
            dic_id_home_workplace[row[0]] = [(LatA, LonA), (LatB, LonB)]  
    family=0
    filePath1='D:/main_code/2_home_swapping/sample_one_two_commuter_households.txt' 
    with open(filePath1,'r')as f:
        for row in f.readlines():
            row=row.strip().split()  
            if len(row)==1:
                pid.append([family,row[0]])  
                family+=1
            if len(row)==2:
                pid.append([family,row[0],row[1]])
                family+=1
            # if len(row)==3:
            #     pid.append([family,row[0],row[1],row[2]])
            #     family+=1
            # if len(row)==4:
            #     pid.append([family,row[0],row[1],row[2],row[3]])
            #     family+=1
    s_dis=0   
    for i in pid:
        lon_h1=float(dic_id_home_workplace[i[1]][0][1]); lat_h1=float(dic_id_home_workplace[i[1]][0][0])  
        family_distance=0
        for j in range(1,len(i)):
            lon_w=float(dic_id_home_workplace[i[j]][1][1]); lat_w=float(dic_id_home_workplace[i[j]][1][0])
            distance=round(get_distance(lon_h1,lat_h1,lon_w,lat_w),4)
            family_distance+=distance
        dic_dis[i[0]]=family_distance    #family_id:family_distance
        s_dis=dic_dis[i[0]]+s_dis
    return dic_id_home_workplace,pid,dic_dis

#only allow home-swapping between 1-commuter and 2-commuter households, as well as swapping between 3-commuter and 4-commuter households.   
def swap_home(dic_id_home_workplace,pid,dic_dis):
    m=0  
    n=0
    sc_dis=0  
    dic_id_home_workplace1=copy.deepcopy(dic_id_home_workplace)
    while m < 1000000:   #We terminate the swapping attempts if no households can be swapped to reduce commuting distance for a consecutive 1×106 attempts.
        rid = random.sample(pid, 2)  
        home1 = dic_id_home_workplace1[rid[0][1]][0];home2=dic_id_home_workplace1[rid[1][1]][0]
        s1=0;s2=0  # Total distance per household before swap home
        s1_change=0;s2_change=0  # Total distance per household after swap home
        lon_h1=float(dic_id_home_workplace1[rid[0][1]][0][1]); lat_h1=float(dic_id_home_workplace1[rid[0][1]][0][0])  
        lon_h2=float(dic_id_home_workplace1[rid[1][1]][0][1]); lat_h2=float(dic_id_home_workplace1[rid[1][1]][0][0])  
        for i in range(1,len(rid[0])): 
            lon_w1=float(dic_id_home_workplace1[rid[0][i]][1][1]); lat_w1=float(dic_id_home_workplace1[rid[0][i]][1][0])
            distance=round(get_distance(lon_h1,lat_h1,lon_w1,lat_w1),4)
            s1=s1+distance  
        for i in range(1,len(rid[1])):  
            lon_w2=float(dic_id_home_workplace1[rid[1][i]][1][1]); lat_w2=float(dic_id_home_workplace1[rid[1][i]][1][0])
            distance=round(get_distance(lon_h2,lat_h2,lon_w2,lat_w2),4)
            s2=s2+distance  
        s=s1+s2  
        for i in range(1,len(rid[0])): 
            lon_w1=float(dic_id_home_workplace1[rid[0][i]][1][1]); lat_w1=float(dic_id_home_workplace1[rid[0][i]][1][0])
            distance=round(get_distance(lon_h2,lat_h2,lon_w1,lat_w1),4)
            s1_change=s1_change+distance  
        for i in range(1,len(rid[1])):
            lon_w2=float(dic_id_home_workplace1[rid[1][i]][1][1]); lat_w2=float(dic_id_home_workplace1[rid[1][i]][1][0])
            distance=round(get_distance(lon_h1,lat_h1,lon_w2,lat_w2),4)
            s2_change=s2_change+distance  
        s_change=s1_change+s2_change
        if s > s_change:  
            for i in range(1,len(rid[0])):
                dic_id_home_workplace1[rid[0][i]][0],home2 = home2,dic_id_home_workplace1[rid[0][i]][0]
            for i in range(1,len(rid[1])):
                dic_id_home_workplace1[rid[1][i]][0],home1 = home1,dic_id_home_workplace1[rid[1][i]][0]
            dic_dis[rid[0][0]]=s1_change    
            dic_dis[rid[1][0]]=s2_change   
            n+=1
            if n % 1000 == 0:
                for i in dic_dis:
                    sc_dis += dic_dis[i]
                print(sc_dis)
                sc_dis = 0
            m=0
        else:
            m+=1
    return dic_id_home_workplace1

if __name__ == '__main__':
    point_center_linkid={}
    center_distance={}
    f_center_distance = open('D:/main_code/1_navigation_routin_crawer/sample_result_start_end_length_time.txt', 'r', encoding='utf-8-sig')
    f_point_center = open('D:/main_code/1_navigation_routin_crawer/sample_origin-point_same-street-point_street-center-point_street-id.txt', 'r', encoding='utf-8-sig')
    for line in f_center_distance:
        line = line.strip().split()
        center_distance[(line[0],line[1])] = int(line[2])
    for line in f_point_center:
        line = line.strip().split()  
        lon1=line[0].split(',')[0]
        lat1=line[0].split(',')[1]
        origin=str(lat1) + ',' + str(lon1)
        lon2=line[1].split(',')[0]
        lat2=line[1].split(',')[1]
        origin_center=str(lat2) + ',' + str(lon2)
        lon3=line[2].split(',')[0]
        lat3=line[2].split(',')[1]
        center=str(lat3) + ',' + str(lon3)
        point_center_linkid[origin]=(origin_center,center,line[3]) #original location：original location,Road center location,Road number
        
    dic_id_home_workplace,pid,dic_dis = actual_total_commuting_distance()
    dic_id_home_workplace1 = swap_home(dic_id_home_workplace,pid,dic_dis)  
    file = open('D:/main_code/2_home_swapping/GHS_12.txt', 'w')
    for i in dic_id_home_workplace1:  
        line = str(i)+'\t'+str(dic_id_home_workplace1[i][0][0]) + '\t' + str(dic_id_home_workplace1[i][0][1]) + '\t' + str(dic_id_home_workplace1[i][1][0])+ '\t' + str(dic_id_home_workplace1[i][1][1])+'\n'
        file.write(line)
    file.close()
