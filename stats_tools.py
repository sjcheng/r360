# -*- coding: utf-8 -*-
"""
Created on Sun Apr 05 22:27:18 2015

@author: Administrator
"""

import features
import random

def stats_feature(item_name):
    f = open('stats_'+item_name+'_id.txt', 'w')
    item_id_dict_pos={}
    item_id_dict_tot={}
    item_id_dict_passpro = {}
    for order in orders:
        item_id = order[item_name]
        if item_id in item_id_dict_tot:
            item_id_dict_tot[item_id] = item_id_dict_tot[item_id]+1                        
        elif item_id not in item_id_dict_tot:
            item_id_dict_tot[item_id] = 1
            item_id_dict_pos[item_id] = 0
        if order['result']=='1':
            item_id_dict_pos[item_id] = item_id_dict_pos[item_id]+1
    for item_id in item_id_dict_tot:
       print >> f, item_id, item_id_dict_tot[item_id],item_id_dict_pos[item_id],float(item_id_dict_pos[item_id])/float(item_id_dict_tot[item_id])
       item_id_dict_passpro[item_id] =  float(item_id_dict_pos[item_id])/float(item_id_dict_tot[item_id])   
    f.close()
    return item_id_dict_passpro

def stats_combine_feature(feature_list):
    f = open('stats_'+str(feature_list)+'_id.txt', 'w')
    item_id_dict_pos={}
    item_id_dict_tot={}
    item_id_dict_passpro = {}
    for order in orders:
        item_name_list = []
        for feature in feature_list:
            item_name_list.append(order[feature])
        item_id = ','.join(item_name_list)
        if item_id in item_id_dict_tot:
            item_id_dict_tot[item_id] = item_id_dict_tot[item_id]+1                        
        elif item_id not in item_id_dict_tot:
            item_id_dict_tot[item_id] = 1
            item_id_dict_pos[item_id] = 0
        if order['result']=='1':
            item_id_dict_pos[item_id] = item_id_dict_pos[item_id]+1
    for item_id in item_id_dict_tot:
       print >> f, item_id, item_id_dict_tot[item_id],item_id_dict_pos[item_id],float(item_id_dict_pos[item_id])/float(item_id_dict_tot[item_id])
       item_id_dict_passpro[item_id] =  float(item_id_dict_pos[item_id])/float(item_id_dict_tot[item_id])   
    f.close()
    return item_id_dict_passpro

if __name__ == '__main__':
    order_train_file = 'order_train.txt'
    orders = features.read_csv_train_data(order_train_file)
    feature_list = ['product_id','term','limit','date']
    stats_combine_feature(feature_list)
    #stats for products
  
    
#    order_test_file = 'order_test_no_label.txt'
#    test_orders = features.read_csv_train_data(order_test_file) 
#    f = open('tmp_result20150405_3.txt', 'w')
#    for test_order in test_orders:
#        if test_order['product_id'] in product_id_dict_passpro:
#            passpro = product_id_dict_passpro[test_order['product_id']]
#            if (random.random()<=passpro):
#                print >> f, 1
#                print "random >> 1"
#            else:
#                print >> f, 0
#                print "random >> 0"
#        else:
#            print >> f, 0
#    f.close()
    #stats for users
#    user_id_dict_pos={}
#    user_id_dict_tot={}
#    f = open('stats_user_id.txt', 'w')
#    for order in orders:
#        user_id = order['user_id']
#        if user_id in user_id_dict_tot:
#            user_id_dict_tot[user_id] = user_id_dict_tot[user_id]+1                        
#        elif user_id not in user_id_dict_tot:
#            user_id_dict_tot[user_id] = 1
#            user_id_dict_pos[user_id] = 0
#        if order['result']=='1':
#            user_id_dict_pos[user_id] = user_id_dict_pos[user_id]+1
#    for user_id in user_id_dict_tot:
#       print >> f, user_id, user_id_dict_tot[user_id],user_id_dict_pos[user_id],float(user_id_dict_pos[user_id])/float(user_id_dict_tot[user_id])
#    f.close()
    