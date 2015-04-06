# -*- coding: utf-8 -*-
"""
Created on Sun Apr 05 22:27:18 2015

@author: Administrator
"""

import features
import random

def stats_feature(item_name, orders):
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

def stats_combine_feature(feature_list, orders):
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
    
def stats_frequency(schema, datas):
    for item in schema:
        print item
        dict_item = {}
        for data in datas:
            value = data[item]
            if value in dict_item:
                dict_item[value] = dict_item[value]+1
            else:
                dict_item[value] = 1
        print dict_item

def sim(product_id1, product_id2):
   sim = 0
   sim_base = 0
   key_list = ['city_id', 'bank_id', 'product_type', 'guarantee_type', 'loan_term_min', 'loan_term_max', 'loan_term_type', 'repayment_type', 'loan_quota_min', 'loan_quota_max', 'is_p2p', 'business_license', 'income', 'house', 'socialsecurity', 'penalty']
   for key in key_list:
       sim_base = sim_base+1
       if product_id1[key] == product_id2[key]:
           sim = sim+1
   return float(sim)/float(sim_base)

def getMostSimilarProductid(nonexist_product_id, exist_product_id_list, product_info_dict):
   max_sim = -1
   max_sim_product_id = -1
   
   for exist_product_id in exist_product_id_list:
       tmp_sim=sim(product_info_dict[nonexist_product_id], product_info_dict[exist_product_id])
       if tmp_sim > max_sim:
           max_sim = tmp_sim
           max_sim_product_id = exist_product_id
   return max_sim_product_id, max_sim
                    
def list_to_dict(item_list, key):
    item_dict = {}
    for item in item_list:
        item_dict[item[key]] = item
    return item_dict

def list_key_set(item_list, key):
    item_key_list = []
    for item in item_list:
        item_key_list.append(item[key])
    item_key_set = set(item_key_list)
    return item_key_set
        
def getResult(test_order, product_id_dict_passpro, product_id_term_passpro, product_id_limit_passpro, product_id_term_limit_passpro, replace_product_id=None):
    product_id = test_order['product_id']
    if replace_product_id is not None:
        product_id = replace_product_id
    term = test_order['term']
    limit = test_order['limit']
    test_product_id_term_limit = ','.join([product_id, term, limit])
    if test_product_id_term_limit in product_id_term_limit_passpro:
        return product_id_term_limit_passpro[test_product_id_term_limit]
    test_product_id_term =  ','.join([product_id, term])   
    if test_product_id_term in product_id_term_passpro:
        return product_id_term_passpro[test_product_id_term]
    test_product_id_limit = ','.join([product_id, limit]) 
    if test_product_id_limit in product_id_limit_passpro:
        return product_id_limit_passpro[test_product_id_limit]
    return product_id_dict_passpro[product_id]

def tmp_predictor():
    order_train_file = 'order_train.txt'
    schema_order, orders = features.read_csv_train_data(order_train_file)
    order_test_file = 'order_test_no_label.txt'
    schema_test_order, test_orders = features.read_csv_train_data(order_test_file)
    product_info_file = 'product.final.txt'
    schema_product_info, product_info_list = features.read_csv_train_data(product_info_file)
    product_info_dict = list_to_dict(product_info_list, 'product_id')
    exist_product_id_list = list_key_set(orders, 'product_id')

    product_id_dict_passpro = stats_feature('product_id', orders)
    product_id_term_passpro = stats_combine_feature(['product_id','term'], orders)
    product_id_limit_passpro = stats_combine_feature(['product_id','limit'], orders)
    product_id_term_limit_passpro = stats_combine_feature(['product_id','term', 'limit'], orders)
    
    result_f = open('result0406_v2.txt', 'w')    
    count = 0
    tmp_sim_product_id = {}
    n = len(test_orders)
    for test_order in test_orders:
        count = count+1
        print count, float(count)/n
        test_product_id = test_order['product_id']
        #product_id exist
        if test_product_id in product_id_dict_passpro:
            result = getResult(test_order, product_id_dict_passpro, product_id_term_passpro, product_id_limit_passpro, product_id_term_limit_passpro)
        else:
            if test_product_id in tmp_sim_product_id:
                max_sim_product_id = tmp_sim_product_id[test_product_id]
            else:
               max_sim_product_id, max_sim = getMostSimilarProductid(test_product_id, exist_product_id_list, product_info_dict)
               tmp_sim_product_id[test_product_id] = max_sim_product_id           
            result = getResult(test_order, product_id_dict_passpro, product_id_term_passpro, product_id_limit_passpro, product_id_term_limit_passpro, max_sim_product_id)#print test_product_id, max_sim_product_id, max_sim
        if random.random()<result:
          print >> result_f, 1
        else:
          print >> result_f, 0
    result_f.close()
    
if __name__ == '__main__':
    tmp_predictor()
#    order_train_file = 'order_train.txt'
#    schema_order, orders = features.read_csv_train_data(order_train_file)
#    order_test_file = 'order_test_no_label.txt'
#    schema_test_order, test_orders = features.read_csv_train_data(order_test_file)
#    count = 0 
#    
#    quality_useful_schema = ["user_id"]
#    quality_train_file = 'quality.final.txt'  
#    quality_schema, qualitys = features.read_csv_train_data_by_schema(quality_train_file, quality_useful_schema)
#    exist_user_list = list_key_set(qualitys, 'user_id')
#    
#    for order_test in orders:
#      if order_test['user_id'] in exist_user_list:
#            count =count+1
#    print count, float(count)/len(test_orders)
    #quality_useful_schema = ["user_id"]
    #quality_train_file = 'quality.final.txt'  
    #quality_schema, qualitys = features.read_csv_train_data_by_schema(quality_train_file, quality_useful_schema)
    

    
    
    #feature_list = ['product_id','term','limit','date']
    #stats_combine_feature(feature_list)
    #stats for products
    #filename =  "quality.final.txt"
    #schema = ['application_type', 'product_type', 'standard_type']
    #schema, datas = features.read_csv_train_data_by_schema(filename, schema)
    #stats_frequency(schema, datas)
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
    