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
            if(tmp[i] == '') :
                data[csv_schema[i]] = numpy.nan
            else: 
                data[csv_schema[i]] = tmp[i]
        data_list.append(data)
    f.close
    return csv_schema, data_list

def read_csv_train_data_by_schema(filename, schema):
    f = open(filename, 'r')
    csv_schema_line = f.readline()
    csv_schema = csv_schema_line.replace('\n','').split('\t')
    data_list = []
    for line in f:
        data = {}
        tmp = line.replace('\n','').split('\t')
        for i in range(len(csv_schema)):
            if(tmp[i] == '') :
                data[csv_schema[i]] = numpy.nan
            else: 
                data[csv_schema[i]] = tmp[i]
        final_data={}
        for i in range(len(schema)):
            final_data[schema[i]] = data[schema[i]]
        data_list.append(final_data)
    f.close
    return schema, data_list
    
# data1 as the main data, and mostly the key is "user_id"
def merge_feature_vector(data1, data2, key):
    result = []
    data2Itor = {}
    for data in data2:
        data2Itor[data[key]] = data
    for data in data1:
        if ( data[key] not in data2Itor ) :
            # print "cannot find user id ", data[key]," in quality data"
            continue
        result.append( dict(data.items() + data2Itor[data[key]].items()) )
    return result
    
def cosine_distance(u, v):
    return numpy.dot(u, v) / (math.sqrt(numpy.dot(u, u)) * math.sqrt(numpy.dot(v, v)))

def pearcorr(list1, list2):
  return numpy.corrcoef(list1, list2)[0, 1]

def ecludSim(inA,inB):
    ##计算向量的第二范式,相当于直接计算了欧式距离
    ## TODO TypeError: unsupported operand type(s) for -: 'list' and 'list'
    return 1.0/(1.0 + la.norm(inA-inB)) 
    
if __name__ == '__main__':
    order_train_file = 'order_train.txt'
    order_scheama, orders = read_csv_train_data(order_train_file)
    
    Y = Feature.get_features(orders, 'result')

    for key in order_scheama:
        if "id" not in key :
            feature = Feature.get_features(orders, key)
            print key, cosine_distance(Y, feature), pearcorr(Y, feature)
    
    
    quality_useful_schema = ["user_id","reapply_count","qid145","apply_from","spam_score","mobile_verify","quality"]
    quality_train_file = 'quality_train.txt'  
    quality_schema, qualitys = read_csv_train_data_by_schema(quality_train_file, quality_useful_schema)
    
    merged_quality = merge_feature_vector(orders, qualitys, "user_id")
    feature_date = Feature.get_features(merged_quality, 'date')
    Y = Feature.get_features(merged_quality, 'result')

    #print "merged: ", merged_quality
    for key in quality_schema:
        if "id" not in key and "type" not in key:
            feature = Feature.get_features(merged_quality, key)
            print key, cosine_distance(Y, feature), pearcorr(Y, feature)
