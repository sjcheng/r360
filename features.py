# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 08:07:02 2015

@author: Administrator
"""

from featureforge.feature import input_schema, output_schema
import math,numpy
from numpy import linalg as la #用到别名

class Feature: 
    @staticmethod
    def get_features(data_list, featurename):
        tmp_array = []        
        for data in data_list:
          tmp_array.append(float(data[featurename]))
        return tmp_array
    
def read_csv_train_data(filename):
    f = open(filename, 'r')
    csv_schema_line = f.readline()
    csv_schema = csv_schema_line.replace('\n','').split('\t')
    data_list = []
    for line in f:
        data = {}
        tmp = line.replace('\n','').split('\t')
        for i in range(len(csv_schema)):
            data[csv_schema[i]] = tmp[i]
        data_list.append(data)
    f.close
    return data_list
    
# data1 as the main data, and mostly the key is "user_id"
def merge_feature_vector(data1, data2, key):
    print "no finish"
    
def cosine_distance(u, v):
    return numpy.dot(u, v) / (math.sqrt(numpy.dot(u, u)) * math.sqrt(numpy.dot(v, v)))

def pearcorr(list1, list2):
  return numpy.corrcoef(list1, list2)[0, 1]

def ecludSim(inA,inB):
    ##计算向量的第二范式,相当于直接计算了欧式距离
    return 1.0/(1.0 + la.norm(inA-inB)) 
    
if __name__ == '__main__':
    order_train_file = 'order_train.txt'
    orders = read_csv_train_data(order_train_file)

    quality_train_file = 'quality_train_tmp.txt'  
    qualitys = read_csv_train_data(quality_train_file)
    
    Y = Feature.get_features(orders, 'result')
    feature_date = Feature.get_features(orders, 'date')
    feature_term = Feature.get_features(orders, 'term')
    feature_limit = Feature.get_features(orders, 'limit')
    print "date: ", cosine_distance(Y, feature_date), pearcorr(Y, feature_date), ecludSim(Y, feature_date)
    print "term: ", cosine_distance(Y, feature_term), pearcorr(Y, feature_term), ecludSim(Y, feature_term)
    print "limit: ", cosine_distance(Y, feature_limit), pearcorr(Y, feature_limit), ecludSim(Y, feature_term)