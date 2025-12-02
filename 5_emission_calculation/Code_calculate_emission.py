# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 10:12:31 2024

@author: Czhao_Team
"""


from math import sin, cos,radians,tan,acos,atan
def get_distance(lon_a, lat_a, lon_b, lat_b):
   if abs(lon_a - lon_b) < 0.000001 and abs(lat_a - lat_b) < 0.000001:
       return 0
   re = 6378140  
   rp = 6356755  
   oblateness = (re - rp) / re 
   rad_lat_a = radians(lat_a)
   rad_lon_a = radians(lon_a)
   rad_lat_b = radians(lat_b)
   rad_lon_b = radians(lon_b)
   atan_a = atan(rp / re * tan(rad_lat_a))
   atan_b = atan(rp / re * tan(rad_lat_b))
   tmp = acos(sin(atan_a) * sin(atan_b) + cos(atan_a) * cos(atan_b) * cos(rad_lon_a - rad_lon_b))
   if tmp == 0:
       return 0
   c1 = (sin(tmp) - tmp) * (sin(atan_a) + sin(atan_b)) ** 2 / cos(tmp / 2) ** 2
   c2 = (sin(tmp) + tmp) * (sin(atan_a) - sin(atan_b)) ** 2 / sin(tmp / 2) ** 2
   dr = oblateness / 8 * (c1 - c2)
   distance = re * (tmp + dr)
   return distance         
##Capacity of road sections at various times
def every_time_actual_route_capacity():      
    dic_actual_route_num={}
    filePath='D:/main_code/5_emission_calculation/sample_every_time_rode_compacity.txt'  # origin destination time capacity
    with open(filePath,'r')as f:
        for row in f.readlines():
            row=row.strip().split() 
            if (row[0],row[1],row[2]) not in dic_actual_route_num:
                dic_actual_route_num[(row[0],row[1],row[2])]=int(row[3])
    return dic_actual_route_num

def every_time_change_route_capacity():
    dic_change_route_num={}
    filePath='D:/main_code/5_emission_calculation/sample_every_time_rode_compacity.txt'  # 
    with open(filePath,'r')as f:
        for row in f.readlines():
            row=row.strip().split()    
            if (row[0],row[1],row[2]) not in dic_change_route_num:
                dic_change_route_num[(row[0],row[1],row[2])]=int(row[3])  
    return dic_change_route_num

def route():
    dic_route={}
    file1='D:/main_code/4_congestion_calculation/sample_commute_route.txt'
    with open(file1,'r')as f:
        for row in f.readlines():
            row=row.strip().split() 
            pid=row[0]
            for i in range(1,len(row)):
                if pid not in dic_route:
                    dic_route[pid]=[row[i]]
                else:
                    dic_route[pid]=dic_route[pid]+[row[i]]     #Commuting routes for each id
    return dic_route
#Emissions per individual empirically verified
def actual_indival_emission(dic_actual_route_num,dic_route):
    emission=0
    emission1=0
    file_w=open('D:/main_code/5_emission_calculation/actual_indival_road_emission.txt','w') #Emissions per individual by road segment
    file_w1=open('D:/main_code/5_emission_calculation/actual_indival_emission.txt','w') #Emissions per individual empirically verified 
    file='D:/main_code/4_congestion_calculation/sample_every_route_time_2500.txt'
    with open(file,'r')as f:
        for row in f.readlines():
            row=row.strip().split() 
            pid=row[0]
            if pid in dic_route:
                for j in range(1,len(dic_route[pid])-1):
                    start_lat=float(dic_route[pid][j].split(',')[0] )
                    start_lon=float(dic_route[pid][j].split(',')[1] )
                    next_lat=float(dic_route[pid][j+1].split(',')[0] )
                    next_lon=float(dic_route[pid][j+1].split(',')[1] )
                    start_time=str(int(int(row[j])/60)*4) 
                    distance_actual=(get_distance(start_lon,start_lat,next_lon,next_lat))*0.001      #road Section Distance
                    emission+=dic_actual_route_num[(dic_route[pid][j],dic_route[pid][j+1],start_time)]*0.209*distance_actual 
                    emission1=dic_actual_route_num[(dic_route[pid][j],dic_route[pid][j+1],start_time)]*0.209*distance_actual  
                    line=str(pid)+' '+str(start_lat)+','+str(start_lon)+' '+str(next_lat)+','+str(next_lon)+' '+str(distance_actual)+' '+str(dic_actual_route_num[(dic_route[pid][j],dic_route[pid][j+1],start_time)])+' '+str(emission1)+'\n'
                    file_w.write(line)
            line1=str(pid)+' '+str(emission)+'\n'
            file_w1.write(line1)
            emission=0                  
    file_w.close()
    file_w1.close()
#Emissions per individual  after swapping homes
def change_indival_emission(dic_change_route_num,dic_route):
    emission=0
    emission1=0
    file_w=open('D:/main_code/5_emission_calculation/GHS_indival_road_emission.txt','w') 
    file_w1=open('D:/main_code/5_emission_calculation/GHS_indival_emission.txt','w')  
    file='D:/main_code/4_congestion_calculation/sample_every_route_time_2500.txt'
    with open(file,'r')as f:
        for row in f.readlines():
            row=row.strip().split() 
            pid=row[0]
            if pid in dic_route:
                for j in range(1,len(dic_route[pid])-1):
                    start_lat=float(dic_route[pid][j].split(',')[0] )
                    start_lon=float(dic_route[pid][j].split(',')[1] )
                    next_lat=float(dic_route[pid][j+1].split(',')[0] )
                    next_lon=float(dic_route[pid][j+1].split(',')[1] )
                    start_time=str(int(int(row[j])/60)*4) 
                    distance_change=(get_distance(start_lon,start_lat,next_lon,next_lat))*0.001     
                    emission+=dic_change_route_num[(dic_route[pid][j],dic_route[pid][j+1],start_time)]*0.209*distance_change
                    emission1=dic_change_route_num[(dic_route[pid][j],dic_route[pid][j+1],start_time)]*0.209*distance_change  
                    line=str(pid)+' '+str(start_lat)+','+str(start_lon)+' '+str(next_lat)+','+str(next_lon)+' '+str(distance_change)+' '+str(dic_change_route_num[(dic_route[pid][j],dic_route[pid][j+1],start_time)])+' '+str(emission1)+'\n'
                    file_w.write(line)
            line1=str(pid)+' '+str(emission)+'\n'
            file_w1.write(line1)
            emission=0             
    file_w.close()
    file_w1.close()

def emission_reduction_rate():
    file='D:/main_code/5_emission_calculation/actual_indival_emission.txt'
    file1='D:/main_code/5_emission_calculation/GHS_indival_emission.txt' 
    s_actual=0
    s_change=0
    with open(file,'r')as f:
        for row in f.readlines():
            row=row.strip().split() 
            s_actual+=float(row[1])
            
    with open(file1,'r')as f:
        for row in f.readlines():
            row=row.strip().split()  
            s_change+=float(row[1])
    print(1-(s_change/s_actual))
    
if __name__ == '__main__':
    dic_actual_route_num=every_time_actual_route_capacity()
    dic_change_route_num=every_time_change_route_capacity()
    dic_route=route()
    # actual_indival_emission(dic_actual_route_num,dic_route)
    change_indival_emission(dic_change_route_num,dic_route)
    emission_reduction_rate()
        
