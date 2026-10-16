# -*- coding: utf-8 -*-
import json
from urllib.request import urlopen


"""# 
"http://api.map.baidu.com/routematrix/v2/driving?"  # drive
'http://api.map.baidu.com/routematrix/v2/riding?'  # bicycle
'http://api.map.baidu.com/routematrix/v2/walking?'  # walk
'http://api.map.baidu.com/direction/v2/transit?'  # bus
"""
def craw_route():
    
    # cod = r"&coord_type=bd09ll"
    key = ' '
    list_pair = []
    f = open('D:/main_code/1_navigation_routin_crawer/sample_residence_workplace.txt', 'r', encoding='utf-8-sig')
    for line in f:
        line = line.strip().split()
        list_pair.append((line[0], line[1]))
    f.close()
    
    f_drive = open('result/result_drive_' + '.txt', 'w', encoding='utf-8-sig')
    #f_ride = open('result_ride.txt', 'w', encoding='utf-8-sig')
    #f_walk = open('result_walk.txt', 'w', encoding='utf-8-sig')
    #f_bus = open('result_bus.txt', 'w', encoding='utf-8-sig')
    f_error = open('result/error.txt', 'a+', encoding='utf-8-sig')
    for i in range(len(list_pair)):
        out = list_pair[i][0]
        des = list_pair[i][1]
        #print(i, out, des)
        try:
            url_drive = r"http://api.map.baidu.com/directionlite/v1/driving?origin={0}&destination={1}&ak={2}".format(out, des, key)
            # url_drive = r"https://api.map.baidu.com/directionlite/v1/driving?origin=40.01116,116.339303&destination=39.936404,116.452562&ak=bdAGy3KfvUf3v7H3bPcbcDNCr5Dg3fgg"
            result_drive = json.loads(urlopen(url_drive).read())  
            status_drive = result_drive['status']
            if status_drive == 0:  
                distance_drive = result_drive['result']['routes'][0]['distance']  
                timesec_drive = result_drive['result']['routes'][0]['duration']   
                step = result_drive['result']['routes'][0]['steps']
                f_drive.write(out + '\t' + des + '\t' + str(distance_drive) + '\t' + str(timesec_drive) + '\t' + str(step) + '\n')
            else:
                print(out, des, 'drive error')
                f_error.write(str(out) + '\t' + str(des) + '\t' + 'drive error\n')
            # time.sleep(1)
        except:
            print(out, des, 'drive error')
            f_error.write(str(out) + '\t' + str(des) + '\t' + 'drive error\n')
            
    
    f_drive.close()
    f_error.close()

if __name__ == '__main__' :
    craw_route()
