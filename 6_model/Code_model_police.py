# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 23:58:29 2025
@author: Czhao_Team
"""
from math import radians, tan, atan, acos, sin, cos
import random
import copy


def get_keys(d, value):
    return [k for k, v in d.items() if v == value]


def get_ou_distance(lon_a, lat_a, lon_b, lat_b):
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


def get_distance(lon_a, lat_a, lon_b, lat_b):
    home = str(lat_a) + ',' + str(lon_a)
    work = str(lat_b) + ',' + str(lon_b)
    if point_center_linkid[home][2] == point_center_linkid[work][2]:
        home_center = point_center_linkid[home][0]
        work_center = point_center_linkid[work][0]
    else:
        home_center = point_center_linkid[home][1]
        work_center = point_center_linkid[work][1]
    if home_center == work_center:
        distance = 0
    else:
        distance = center_distance[(home_center, work_center)]
    return distance


def id_change_home():
    dic_id_change_home = {}
    filePath3 = open('D:/main_code/2_home_swapping/sample_change_home_in_center_commuter.txt', 'r')
    for row in filePath3:
        row = row.strip().split()
        dic_id_change_home[int(row[0])] = row[1]  # id:households'residence after GHS
    return dic_id_change_home


def home_capacity():  #
    dic_id_workplace = {}  # id:workplace
    dic_id_home = {}  # id:home
    dic_home = {}  # home:number of individual
    dic_home_one_two = {}  # home : number of single-commuter hopuseholds and dual-commuter households
    dic_home_three_four = {}  # home : number of three-commuter hopuseholds and four-commuter households
    filePath = open('D:/main_code/2_home_swapping/sample_commuter_home_workplace.txt', 'r')
    for row in filePath:
        row = row.strip().split()
        dic_id_workplace[int(row[0])] = row[2]
        dic_id_home[int(row[0])] = row[1]

    filePath2 = open('D:/main_code/2_home_swapping/sample_all_commuter_households.txt', 'r')
    for row in filePath2:
        row = row.strip().split()
        home = dic_id_home[int(row[0])]
        if len(row) == 1 or len(row) == 2:  # home:number of single-commuter households and dual-commuter households
            if home not in dic_home_one_two:
                dic_home_one_two[home] = 1
            else:
                dic_home_one_two[home] = dic_home_one_two[home] + 1
            if home not in dic_home:
                dic_home[home] = 2
            else:
                dic_home[home] = dic_home[home] + 2
        if len(row) == 3 or len(row) == 4:  # home : number of three-commuter households and four-commuter households
            if home not in dic_home_three_four:
                dic_home_three_four[home] = 1
            else:
                dic_home_three_four[home] = dic_home_three_four[home] + 1
            if home not in dic_home:
                dic_home[home] = 4
            else:
                dic_home[home] = dic_home[home] + 4
    return dic_home_one_two, dic_home_three_four, dic_home


def household_id_member():  # household_id:household_member_id
    dic_work = {}
    filePath1 = open('D:/main_code/2_home_swapping/sample_all_commuter_households.txt', 'r')
    j = 0
    for row in filePath1:
        row = row.strip().split()
        if len(row) == 1:
            dic_work[j] = [int(row[0])]  # household_id:household_member_id
        if len(row) == 2:
            dic_work[j] = [int(row[0]), int(row[1])]
        if len(row) == 3:
            dic_work[j] = [int(row[0]), int(row[1]), int(row[2])]
        if len(row) == 4:
            dic_work[j] = [int(row[0]), int(row[1]), int(row[2]), int(row[3])]
        j += 1
    return dic_work

def family_house_price():
    # housing price
    dic_home_price = {}
    file_house_price = 'D:/main_code/3_constrained_home_swapping/p-GHS/sample_home_price.txt'
    with open(file_house_price, 'r') as f:
        for row in f.readlines():
            row = row.strip().split()
            dic_home_price[(row[0])] = float(row[1])
    return dic_home_price


def model(dic_home_one_two, dic_home_three_four, dic_home, dic_home_price, dic_work, dic_id_change_home):
    dic_home_capacity=copy.deepcopy(dic_home)
    for h in dic_home_capacity:
        dic_home_capacity[h] = 0
    file = open('D:/main_code/model/result_model_police.txt', 'w')
    D = 0.5  # decent
    L = 272  # average street length
    list_worker_family = list(dic_work.keys())
    ll = list_worker_family
    dic_home_select = {};
    dic_home_id_select = {};
    dic_home_id_select_one_two = {};
    dic_home_id_select_three_four = {}
    for j in ll:
        origin_home = dic_id_home[dic_work[j][0]]
        change_home = dic_id_change_home[dic_work[j][0]]  # household'residence after GHS
        lon_op_h = float(change_home.split(',')[1]);
        lat_op_h = float(change_home.split(',')[0])
        dic_home_select_P = {}
        for h in dic_home:
            capacity = dic_home[h]
            capacity_select = dic_home_capacity[h]
            lon_h = float(h.split(',')[1]);
            lat_h = float(h.split(',')[0])
            origin_price = float(dic_home_price[origin_home]);
            change_price = float(dic_home_price[h])
            before_after_home_distance = get_ou_distance(lon_h, lat_h, lon_op_h, lat_op_h)
            police = 1 / (((1 - (D / ((1 + (before_after_home_distance / 272)) ** 2))) ** 4) + 0.0001)
            if len(dic_work[j]) == 1:  
                lon_w = float(dic_id_workplace[dic_work[j][0]].split(',')[1]);
                lat_w = float(dic_id_workplace[dic_work[j][0]].split(',')[0])
                dis_worker = round(get_distance(lon_w, lat_w, lon_h, lat_h), 4)
                A = capacity * (1 + capacity_select) / (dis_worker + 1)
                E = 1 - abs(origin_price - change_price) / origin_price
                if h in dic_home_one_two:
                    if E > 0 and dic_home_one_two[h] > 0:
                        P = A * E * police
                        dic_home_select_P[h] = P
            if len(dic_work[j]) == 2:  #
                lon_w1 = float(dic_id_workplace[dic_work[j][0]].split(',')[1]);
                lat_w1 = float(dic_id_workplace[dic_work[j][0]].split(',')[0])
                dis_worker1 = round(get_distance(lon_w1, lat_w1, lon_h, lat_h), 4)
                lon_w2 = float(dic_id_workplace[dic_work[j][1]].split(',')[1]);
                lat_w2 = float(dic_id_workplace[dic_work[j][1]].split(',')[0])
                dis_worker2 = round(get_distance(lon_w2, lat_w2, lon_h, lat_h), 4)
                A = capacity * (1 + capacity_select) / pow(((dis_worker1 + 1) * (dis_worker2 + 1)), 1 / 2)
                E = 1 - abs(origin_price - change_price) / origin_price
                if h in dic_home_one_two:
                    if E > 0 and dic_home_one_two[h] > 0:
                        P = A * E * police
                        dic_home_select_P[h] = P
            if len(dic_work[j]) == 3:
                lon_w1 = float(dic_id_workplace[dic_work[j][0]].split(',')[1]);
                lat_w1 = float(dic_id_workplace[dic_work[j][0]].split(',')[0])
                dis_worker1 = round(get_distance(lon_w1, lat_w1, lon_h, lat_h), 4)
                lon_w2 = float(dic_id_workplace[dic_work[j][1]].split(',')[1]);
                lat_w2 = float(dic_id_workplace[dic_work[j][1]].split(',')[0])
                dis_worker2 = round(get_distance(lon_w2, lat_w2, lon_h, lat_h), 4)
                lon_w3 = float(dic_id_workplace[dic_work[j][2]].split(',')[1]);
                lat_w3 = float(dic_id_workplace[dic_work[j][2]].split(',')[0])
                dis_worker3 = round(get_distance(lon_w3, lat_w3, lon_h, lat_h), 4)
                A = capacity * (1 + capacity_select) / pow(((dis_worker1 + 1) * (dis_worker2 + 1) * (dis_worker3 + 1)),
                                                           1 / 3)
                E = 1 - abs(origin_price - change_price) / origin_price
                if h in dic_home_three_four:
                    if E > 0 and dic_home_three_four[h] > 0:
                        P = A * E * police
                        dic_home_select_P[h] = P
            if len(dic_work[j]) == 4:
                lon_w1 = float(dic_id_workplace[dic_work[j][0]].split(',')[1]);
                lat_w1 = float(dic_id_workplace[dic_work[j][0]].split(',')[0])
                dis_worker1 = round(get_distance(lon_w1, lat_w1, lon_h, lat_h), 4)
                lon_w2 = float(dic_id_workplace[dic_work[j][1]].split(',')[1]);
                lat_w2 = float(dic_id_workplace[dic_work[j][1]].split(',')[0])
                dis_worker2 = round(get_distance(lon_w2, lat_w2, lon_h, lat_h), 4)
                lon_w3 = float(dic_id_workplace[dic_work[j][2]].split(',')[1]);
                lat_w3 = float(dic_id_workplace[dic_work[j][2]].split(',')[0])
                dis_worker3 = round(get_distance(lon_w3, lat_w3, lon_h, lat_h), 4)
                lon_w4 = float(dic_id_workplace[dic_work[j][3]].split(',')[1]);
                lat_w4 = float(dic_id_workplace[dic_work[j][3]].split(',')[0])
                dis_worker4 = round(get_distance(lon_w4, lat_w4, lon_h, lat_h), 4)
                A = capacity * (1 + capacity_select) / pow((dis_worker1 * dis_worker2 * dis_worker3 * dis_worker4) + 1,
                                                           1 / 4)
                E = 1 - abs(origin_price - change_price) / origin_price
                if h in dic_home_three_four:
                    if E > 0 and dic_home_three_four[h] > 0:
                        P = A * E * police
                        dic_home_select_P[h] = P

        dic_select_home_P_range = {}
        u = sum(dic_home_select_P.values())
        s = 0
        for l in dic_home_select_P:
            dic_select_home_P_range[l] = [s / u, (s + dic_home_select_P[l]) / u]
            s = s + dic_home_select_P[l]
        m = random.random()
        select_home = []
        for n in dic_select_home_P_range:
            if dic_select_home_P_range[n][0] <= m < dic_select_home_P_range[n][1]:
                select_home.append(n)
        o = random.choice(select_home)
        if o == dic_id_change_home[dic_work[j][0]]:
            dic_home_select[j] = o

            if len(dic_work[j]) == 1 or len(dic_work[j]) == 2:
                if o not in dic_home_id_select_one_two.keys():
                    dic_home_id_select_one_two[o] = [j]
                else:
                    dic_home_id_select_one_two[o] = dic_home_id_select_one_two[o] + [j]

            if len(dic_work[j]) == 3 or len(dic_work[j]) == 4:
                if o not in dic_home_id_select_three_four.keys():
                    dic_home_id_select_three_four[o] = [j]
                else:
                    dic_home_id_select_three_four[o] = dic_home_id_select_three_four[o] + [j]

            if o not in dic_home_id_select.keys():
                dic_home_id_select[o] = [j]
            else:
                dic_home_id_select[o] = dic_home_id_select[o] + [j]
    for id_select_home in dic_home_id_select:
        if id_select_home in dic_home_id_select_one_two:
            fid_number_one = len(dic_home_id_select_one_two[id_select_home])
            if fid_number_one > dic_home_one_two[id_select_home]:
                kk = random.sample(dic_home_id_select_one_two[id_select_home],
                                   len(dic_home_id_select_one_two[id_select_home]) - int(
                                       dic_home_one_two[id_select_home]))
                for q in kk:
                    dic_home_id_select_one_two[id_select_home].remove(q)
                    dic_home_id_select[id_select_home].remove(q)
                    del dic_home_select[q]
                    ll.remove(q)

        if id_select_home in dic_home_id_select_three_four:
            fid_number_three = len(dic_home_id_select_three_four[id_select_home])
            if fid_number_three > dic_home_three_four[id_select_home]:
                kk = random.sample(dic_home_id_select_three_four[id_select_home],
                                   len(dic_home_id_select_three_four[id_select_home]) - int(
                                       dic_home_three_four[id_select_home]))
                for q in kk:
                    dic_home_id_select_three_four[id_select_home].remove(q)
                    dic_home_id_select[id_select_home].remove(q)
                    del dic_home_select[q]
                    ll.remove(q)

    for r in dic_home_select:
        if len(dic_work[r]) == 1:
            line = str(dic_home_select[r]) + ' ' + str(dic_id_workplace[dic_work[r][0]]) + '\n'
            file.write(line)
        if len(dic_work[r]) == 2:
            line = str(dic_home_select[r]) + ' ' + str(dic_id_workplace[dic_work[r][0]]) + ' ' + str(
                dic_id_workplace[dic_work[r][1]]) + '\n'
            file.write(line)
        if len(dic_work[r]) == 3:
            line = str(dic_home_select[r]) + ' ' + str(dic_id_workplace[dic_work[r][0]]) + ' ' + str(
                dic_id_workplace[dic_work[r][1]]) + ' ' + str(dic_id_workplace[dic_work[r][2]]) + '\n'
            file.write(line)
        if len(dic_work[r]) == 4:
            line = str(dic_home_select[r]) + ' ' + str(dic_id_workplace[dic_work[r][0]]) + ' ' + str(
                dic_id_workplace[dic_work[r][1]]) + ' ' + str(dic_id_workplace[dic_work[r][2]]) + ' ' + str(
                dic_id_workplace[dic_work[r][3]]) + '\n'
            file.write(line)

    for t in dic_home_id_select_one_two:
        fid_number = len(dic_home_id_select_one_two[t])
        dic_home_one_two[t] = dic_home_one_two[t] - fid_number

    for t in dic_home_id_select_three_four:
        fid_number = len(dic_home_id_select_three_four[t])
        dic_home_three_four[t] = dic_home_three_four[t] - fid_number

    for t in dic_home_id_select:
        id_select_home_number = 0
        for fid in dic_home_id_select[t]:
            id_select_home_number += len(dic_work[fid])
        dic_home[t] = dic_home[t] - id_select_home_number
        dic_home_capacity[t] = dic_home_capacity[t] + id_select_home_number
        for v in dic_home_id_select[t]:
            del dic_work[v]

    while len(dic_work) > 0:   # # the process only ceased once all households had been allocated their places of residence
        list_worker_family = list(dic_work.keys())
        if len(list_worker_family) > 1000:
            ll = random.sample(list_worker_family, 1000)
        else:
            ll = list_worker_family
        dic_home_select = {};
        dic_home_id_select = {};
        dic_home_id_select_one_two = {};
        dic_home_id_select_three_four = {}
        for j in ll:
            origin_home = dic_id_home[dic_work[j][0]]
            change_home = dic_id_change_home[dic_work[j][0]]
            lon_op_h = float(change_home.split(',')[1]);
            lat_op_h = float(change_home.split(',')[0])
            dic_home_select_P = {}
            for h in dic_home:
                capacity = dic_home[h]
                capacity_select = dic_home_capacity[h]
                lon_h = float(h.split(',')[1]);
                lat_h = float(h.split(',')[0])
                origin_price = float(dic_home_price[origin_home]);
                change_price = float(dic_home_price[h])
                before_after_home_distance = get_ou_distance(lon_h, lat_h, lon_op_h, lat_op_h)  # the distance between optimal locatiuon and the current residence
                police = 1 / (((1 - (D / ((1 + (before_after_home_distance / 272)) ** 2))) ** 4) + 0.0001)  #
                if len(dic_work[j]) == 1:
                    lon_w = float(dic_id_workplace[dic_work[j][0]].split(',')[1]);
                    lat_w = float(dic_id_workplace[dic_work[j][0]].split(',')[0])
                    dis_worker = round(get_distance(lon_w, lat_w, lon_h, lat_h), 4)
                    A = capacity * (1 + capacity_select) / (dis_worker + 1)
                    E = 1 - abs(origin_price - change_price) / origin_price
                    if h in dic_home_one_two:
                        if E > 0 and dic_home_one_two[h] > 0:
                            P = A * E * police
                            dic_home_select_P[h] = P
                if len(dic_work[j]) == 2:  #
                    lon_w1 = float(dic_id_workplace[dic_work[j][0]].split(',')[1]);
                    lat_w1 = float(dic_id_workplace[dic_work[j][0]].split(',')[0])
                    dis_worker1 = round(get_distance(lon_w1, lat_w1, lon_h, lat_h), 4)
                    lon_w2 = float(dic_id_workplace[dic_work[j][1]].split(',')[1]);
                    lat_w2 = float(dic_id_workplace[dic_work[j][1]].split(',')[0])
                    dis_worker2 = round(get_distance(lon_w2, lat_w2, lon_h, lat_h), 4)
                    A = capacity * (1 + capacity_select) / pow(((dis_worker1 + 1) * (dis_worker2 + 1)), 1 / 2)
                    E = 1 - abs(origin_price - change_price) / origin_price
                    if h in dic_home_one_two:
                        if E > 0 and dic_home_one_two[h] > 0:
                            P = A * E * police
                            dic_home_select_P[h] = P
                if len(dic_work[j]) == 3:
                    lon_w1 = float(dic_id_workplace[dic_work[j][0]].split(',')[1]);
                    lat_w1 = float(dic_id_workplace[dic_work[j][0]].split(',')[0])
                    dis_worker1 = round(get_distance(lon_w1, lat_w1, lon_h, lat_h), 4)
                    lon_w2 = float(dic_id_workplace[dic_work[j][1]].split(',')[1]);
                    lat_w2 = float(dic_id_workplace[dic_work[j][1]].split(',')[0])
                    dis_worker2 = round(get_distance(lon_w2, lat_w2, lon_h, lat_h), 4)
                    lon_w3 = float(dic_id_workplace[dic_work[j][2]].split(',')[1]);
                    lat_w3 = float(dic_id_workplace[dic_work[j][2]].split(',')[0])
                    dis_worker3 = round(get_distance(lon_w3, lat_w3, lon_h, lat_h), 4)
                    A = capacity * (1 + capacity_select) / pow(
                        ((dis_worker1 + 1) * (dis_worker2 + 1) * (dis_worker3 + 1)), 1 / 3)
                    E =1 - abs(origin_price - change_price) / origin_price
                    if h in dic_home_three_four:
                        if E > 0 and dic_home_three_four[h] > 0:
                            P = A * E * police
                            dic_home_select_P[h] = P
                if len(dic_work[j]) == 4:
                    lon_w1 = float(dic_id_workplace[dic_work[j][0]].split(',')[1]);
                    lat_w1 = float(dic_id_workplace[dic_work[j][0]].split(',')[0])
                    dis_worker1 = round(get_distance(lon_w1, lat_w1, lon_h, lat_h), 4)
                    lon_w2 = float(dic_id_workplace[dic_work[j][1]].split(',')[1]);
                    lat_w2 = float(dic_id_workplace[dic_work[j][1]].split(',')[0])
                    dis_worker2 = round(get_distance(lon_w2, lat_w2, lon_h, lat_h), 4)
                    lon_w3 = float(dic_id_workplace[dic_work[j][2]].split(',')[1]);
                    lat_w3 = float(dic_id_workplace[dic_work[j][2]].split(',')[0])
                    dis_worker3 = round(get_distance(lon_w3, lat_w3, lon_h, lat_h), 4)
                    lon_w4 = float(dic_id_workplace[dic_work[j][3]].split(',')[1]);
                    lat_w4 = float(dic_id_workplace[dic_work[j][3]].split(',')[0])
                    dis_worker4 = round(get_distance(lon_w4, lat_w4, lon_h, lat_h), 4)
                    A = capacity * (1 + capacity_select) / pow(
                            ((dis_worker1+1) * (dis_worker2+1) * (dis_worker3+1) * (dis_worker4+1)), 1 / 4)
                    E = 1 - abs(origin_price - change_price) / origin_price
                    if h in dic_home_three_four:
                        if E > 0 and dic_home_three_four[h] > 0:
                            P = A * E * police
                            dic_home_select_P[h] = P
            if len(dic_home_select_P) == 0:
                for h in dic_home:
                    capacity = dic_home[h]
                    capacity_select = dic_home_capacity[h]
                    lon_h = float(h.split(',')[1]);
                    lat_h = float(h.split(',')[0])
                    origin_price = float(dic_home_price[origin_home]);
                    change_price = float(dic_home_price[h])
                    before_after_home_distance = get_ou_distance(lon_h, lat_h, lon_op_h, lat_op_h)
                    police = 1 / (((1 - (D / ((1 + (before_after_home_distance / 272)) ** 2))) ** 4) + 0.0001)
                    if len(dic_work[j]) == 1:
                        lon_w = float(dic_id_workplace[dic_work[j][0]].split(',')[1]);
                        lat_w = float(dic_id_workplace[dic_work[j][0]].split(',')[0])
                        dis_worker = round(get_distance(lon_w, lat_w, lon_h, lat_h), 4)
                        A = capacity * (1 + capacity_select) / (dis_worker + 1)
                        E = 1 - abs(origin_price - change_price) / origin_price
                        if h in dic_home_one_two:
                            if dic_home_one_two[h] > 0:
                                P = A * E * police
                                dic_home_select_P[h] = P
                    if len(dic_work[j]) == 2:  #
                        lon_w1 = float(dic_id_workplace[dic_work[j][0]].split(',')[1]);
                        lat_w1 = float(dic_id_workplace[dic_work[j][0]].split(',')[0])
                        dis_worker1 = round(get_distance(lon_w1, lat_w1, lon_h, lat_h), 4)
                        lon_w2 = float(dic_id_workplace[dic_work[j][1]].split(',')[1]);
                        lat_w2 = float(dic_id_workplace[dic_work[j][1]].split(',')[0])
                        dis_worker2 = round(get_distance(lon_w2, lat_w2, lon_h, lat_h), 4)
                        A = capacity * (1 + capacity_select) / pow(((dis_worker1 + 1) * (dis_worker2 + 1)), 1 / 2)
                        E = 1 - abs(origin_price - change_price) / origin_price
                        if h in dic_home_one_two:
                            if dic_home_one_two[h] > 0:
                                P = A * E * police
                                dic_home_select_P[h] = P
                    if len(dic_work[j]) == 3:
                        lon_w1 = float(dic_id_workplace[dic_work[j][0]].split(',')[1]);
                        lat_w1 = float(dic_id_workplace[dic_work[j][0]].split(',')[0])
                        dis_worker1 = round(get_distance(lon_w1, lat_w1, lon_h, lat_h), 4)
                        lon_w2 = float(dic_id_workplace[dic_work[j][1]].split(',')[1]);
                        lat_w2 = float(dic_id_workplace[dic_work[j][1]].split(',')[0])
                        dis_worker2 = round(get_distance(lon_w2, lat_w2, lon_h, lat_h), 4)
                        lon_w3 = float(dic_id_workplace[dic_work[j][2]].split(',')[1]);
                        lat_w3 = float(dic_id_workplace[dic_work[j][2]].split(',')[0])
                        dis_worker3 = round(get_distance(lon_w3, lat_w3, lon_h, lat_h), 4)
                        A = capacity * (1 + capacity_select) / pow(
                            ((dis_worker1 + 1) * (dis_worker2 + 1) * (dis_worker3 + 1)), 1 / 3)
                        E = 1 - abs(origin_price - change_price) / origin_price
                        if h in dic_home_three_four:
                            if dic_home_three_four[h] > 0:
                                P = A * E * police  
                                dic_home_select_P[h] = P
                    if len(dic_work[j]) == 4:
                        lon_w1 = float(dic_id_workplace[dic_work[j][0]].split(',')[1]);
                        lat_w1 = float(dic_id_workplace[dic_work[j][0]].split(',')[0])
                        dis_worker1 = round(get_distance(lon_w1, lat_w1, lon_h, lat_h), 4)
                        lon_w2 = float(dic_id_workplace[dic_work[j][1]].split(',')[1]);
                        lat_w2 = float(dic_id_workplace[dic_work[j][1]].split(',')[0])
                        dis_worker2 = round(get_distance(lon_w2, lat_w2, lon_h, lat_h), 4)
                        lon_w3 = float(dic_id_workplace[dic_work[j][2]].split(',')[1]);
                        lat_w3 = float(dic_id_workplace[dic_work[j][2]].split(',')[0])
                        dis_worker3 = round(get_distance(lon_w3, lat_w3, lon_h, lat_h), 4)
                        lon_w4 = float(dic_id_workplace[dic_work[j][3]].split(',')[1]);
                        lat_w4 = float(dic_id_workplace[dic_work[j][3]].split(',')[0])
                        dis_worker4 = round(get_distance(lon_w4, lat_w4, lon_h, lat_h), 4)
                        A = capacity * (1 + capacity_select) / pow(
                            ((dis_worker1+1) * (dis_worker2+1) * (dis_worker3+1) * (dis_worker4+1)), 1 / 4)
                        E = 1 - abs(origin_price - change_price) / origin_price
                        if h in dic_home_three_four:
                            if dic_home_three_four[h] > 0:
                                P = A * E * police
                                dic_home_select_P[h] = P

            dic_select_home_P_range = {}
            u = sum(dic_home_select_P.values())
            s = 0
            for l in dic_home_select_P:
                dic_select_home_P_range[l] = [s / u, (s + dic_home_select_P[l]) / u]
                s = s + dic_home_select_P[l]
            m = random.random()
            select_home = []
            for n in dic_select_home_P_range:
                if dic_select_home_P_range[n][0] <= m < dic_select_home_P_range[n][1]:
                    select_home.append(n)
            o = random.choice(select_home)
            sum_select_same_home_opt = 0
            dic_home_select[j] = o
            sum_select_same_home_opt = sum_select_same_home_opt + 1
            if len(dic_work[j]) == 1 or len(dic_work[j]) == 2:
                if o not in dic_home_id_select_one_two.keys():
                    dic_home_id_select_one_two[o] = [j]
                else:
                    dic_home_id_select_one_two[o] = dic_home_id_select_one_two[o] + [j]

            if len(dic_work[j]) == 3 or len(dic_work[j]) == 4:
                if o not in dic_home_id_select_three_four.keys():
                    dic_home_id_select_three_four[o] = [j]
                else:
                    dic_home_id_select_three_four[o] = dic_home_id_select_three_four[o] + [j]


            if o not in dic_home_id_select.keys():
                dic_home_id_select[o] = [j]
            else:
                dic_home_id_select[o] = dic_home_id_select[o] + [j]
        #####
        for id_select_home in dic_home_id_select:
            if id_select_home in dic_home_id_select_one_two:
                fid_number_one = len(dic_home_id_select_one_two[id_select_home])
                if fid_number_one > dic_home_one_two[id_select_home]:
                    kk = random.sample(dic_home_id_select_one_two[id_select_home],
                                       len(dic_home_id_select_one_two[id_select_home]) - int(
                                           dic_home_one_two[id_select_home]))
                    for q in kk:
                        dic_home_id_select_one_two[id_select_home].remove(q)
                        dic_home_id_select[id_select_home].remove(q)
                        del dic_home_select[q]
                        ll.remove(q)


            if id_select_home in dic_home_id_select_three_four:
                fid_number_three = len(dic_home_id_select_three_four[id_select_home])

                if fid_number_three > dic_home_three_four[id_select_home]:
                    kk = random.sample(dic_home_id_select_three_four[id_select_home],
                                       len(dic_home_id_select_three_four[id_select_home]) - int(
                                           dic_home_three_four[id_select_home]))
                    for q in kk:
                        dic_home_id_select_three_four[id_select_home].remove(q)
                        dic_home_id_select[id_select_home].remove(q)
                        del dic_home_select[q]
                        ll.remove(q)

        for r in dic_home_select:
            if len(dic_work[r]) == 1:
                line = str(dic_home_select[r]) + ' ' + str(dic_id_workplace[dic_work[r][0]]) + '\n'
                file.write(line)
            if len(dic_work[r]) == 2:
                line = str(dic_home_select[r]) + ' ' + str(dic_id_workplace[dic_work[r][0]]) + ' ' + str(
                    dic_id_workplace[dic_work[r][1]]) + '\n'
                file.write(line)
            if len(dic_work[r]) == 3:
                line = str(dic_home_select[r]) + ' ' + str(dic_id_workplace[dic_work[r][0]]) + ' ' + str(
                    dic_id_workplace[dic_work[r][1]]) + ' ' + str(dic_id_workplace[dic_work[r][2]]) + '\n'
                file.write(line)
            if len(dic_work[r]) == 4:
                line = str(dic_home_select[r]) + ' ' + str(dic_id_workplace[dic_work[r][0]]) + ' ' + str(
                    dic_id_workplace[dic_work[r][1]]) + ' ' + str(dic_id_workplace[dic_work[r][2]]) + ' ' + str(
                    dic_id_workplace[dic_work[r][3]]) + '\n'
                file.write(line)

        for t in dic_home_id_select_one_two:
            fid_number = len(dic_home_id_select_one_two[t])
            dic_home_one_two[t] = dic_home_one_two[t] - fid_number

        for t in dic_home_id_select_three_four:
            fid_number = len(dic_home_id_select_three_four[t])
            dic_home_three_four[t] = dic_home_three_four[t] - fid_number

        for t in dic_home_id_select:
            id_select_home_number = 0
            for fid in dic_home_id_select[t]:
                id_select_home_number += len(dic_work[fid])
            dic_home[t] = dic_home[t] - id_select_home_number
            dic_home_capacity[t] = dic_home_capacity[t] + id_select_home_number
            for v in dic_home_id_select[t]:
                del dic_work[v]
    file.close()


if __name__ == '__main__':
    # calculate commuting distance
    point_center_linkid = {}
    center_distance = {}
    f_center_distance = open('D:/main_code/1_navigation_routin_crawer/sample_result_start_end_length_time.txt', 'r',
                             encoding='utf-8-sig')
    f_point_center = open(
        'D:/main_code/1_navigation_routin_crawer/sample_origin-point_same-street-point_street-center-point_street-id.txt',
        'r', encoding='utf-8-sig')
    for line in f_center_distance:
        line = line.strip().split()
        center_distance[(line[0], line[1])] = int(line[2])
    for line in f_point_center:
        line = line.strip().split()
        lon1 = line[0].split(',')[0]
        lat1 = line[0].split(',')[1]
        origin = str(lat1) + ',' + str(lon1)
        lon2 = line[1].split(',')[0]
        lat2 = line[1].split(',')[1]
        origin_center = str(lat2) + ',' + str(lon2)
        lon3 = line[2].split(',')[0]
        lat3 = line[2].split(',')[1]
        center = str(lat3) + ',' + str(lon3)
        point_center_linkid[origin] = (origin_center, center, line[3])
    dic_id_change_home = id_change_home()
    dic_home_one_two, dic_home_three_four, dic_home = home_capacity()
    dic_work = household_id_member()
    dic_home_price = family_house_price()
    model(dic_home_one_two, dic_home_three_four, dic_home, dic_home_price, dic_work)
