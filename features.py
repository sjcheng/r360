# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 08:07:02 2015

@author: Administrator
"""

from featureforge.feature import input_schema, output_schema
import math,numpy

'''
user_id：用户id
product_id：产品id
date：不同日期，值越大代表离当前越近
term：申请期限
limit：申请金额
result：0代表贷款申请没有被批准，1代表贷款申请获得批准
'''

class Order:    
    oneorder = {}
    def __init__(self, user_id, product_id, date, term, limit, result=None):
        self.oneorder['user_id']=user_id
        self.oneorder['product_id']=product_id
        self.oneorder['date']=date
        self.oneorder['term']=term
        self.oneorder['limit']=limit
        self.oneorder['result']=result
    def getorder(self):
        return self.oneorder


class OrderFeature: 
    @staticmethod
    def get_features(orders, featurename):
        tmp_array = []        
        for order in orders:
          tmp_array.append(float(order[featurename]))
        return tmp_array
        
    @staticmethod
    def order_feature(order, feature_name):
      return order[feature_name]

def read_order_train_data(filename):
    f = open(filename, 'r')
    orders = []
    for line in f:
      tmp = line.split('\t')
      user_id = tmp[0]
      product_id = tmp[1]
      date = tmp[2]
      term = tmp[3]
      limit = tmp[4]
      result = tmp[5]
      oneorder = Order(user_id, product_id, date, term, limit, result).getorder()
      orders.append(oneorder)
    f.close()    
    return orders
        
def cosine_distance(u, v):
    return numpy.dot(u, v) / (math.sqrt(numpy.dot(u, u)) * math.sqrt(numpy.dot(v, v)))
    
if __name__ == '__main__':
    train_file = 'order_train.txt'
    orders = read_order_train_data(train_file)
    Y = OrderFeature.get_features(orders, 'result')
    print Y
    feature_date = OrderFeature.get_features(orders, 'date')
    print feature_date
    feature_term = OrderFeature.get_features(orders, 'term')
    feature_limit = OrderFeature.get_features(orders, 'limit')
    print cosine_distance(Y, feature_date)
    print cosine_distance(Y, feature_term)
    print cosine_distance(Y, feature_limit)