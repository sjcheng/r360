# -*- coding: utf-8 -*-
"""
Created on Sat April 6 08:07:02 2015

@author: sjcheng
"""

#from featureforge.feature import input_schema, output_schema
#import math,numpy
#from numpy import linalg as la #用到别名
from sklearn import tree
from sklearn.feature_extraction import DictVectorizer
from sklearn.externals.six import StringIO  
#import pydot 
import time

ISOTIMEFORMAT='%Y-%m-%d %X'
FILENAMEFORMAT='%Y%m%d%H%M'

class Feature: 
    @staticmethod
    def get_features(data_list, index):
        tmp_array = []        
        for data in data_list:
          tmp_array.append(float(data[index]))
        return tmp_array

def read_csv_train_data(filename):
    f = open(filename, 'r')
    csv_schema_line = f.readline()
    csv_schema = csv_schema_line.replace('\n','').split('\t')
    data_list = []
    for line in f:
        data = []
        tmp = line.replace('\n','').split('\t')
        for i in range(len(csv_schema)):
            if(tmp[i] == '') :
                #data.append(numpy.nan)
                #if uses numpy.nan will has exception when ValueError: Input contains NaN, infinity or a value too large for dtype('float32').
                data.append("-1")            
            else: 
                data.append(tmp[i])
        data_list.append(data)
    f.close()
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
                #data[csv_schema[i]] = numpy.nan
                data[csv_schema[i]] = "-1"
            else: 
                data[csv_schema[i]] = tmp[i]
        final_data=[]
        for i in range(len(schema)):
            final_data.append(data[schema[i]])
        data_list.append(final_data)
    f.close
    return schema, data_list
    
def output_csv_data(filename, data_list, schema):
    f = open(filename, "w")
    title = ""
    for field in schema:
        if title == "":
            title = field
        else:
            title = title + "\t" + field
    f.write( title )
    f.newlines()
    for data in data_list:
        f.write( data )
        f.newlines()
    

def generate_feature_vector(data_schema, data_list, schema):
    features = []
    for data in data_list:
        newData = {}
        for field in schema:
            newData[field] = ( data[data_schema.index(field) ] )
        features.append( newData )
    return features
    
# data1 as the main data, and mostly the key is "user_id"
def merge_feature_vector(data1_schema, data1, data2_schema, data2, keys):
    result = []
    join_flag = []
    data2Itor = {}

    schema = []
    schema = data1_schema + data2_schema
    
    for data in data2:
        data2Itor[generate_partition_key(data2_schema, data, keys)] = data
        
    for data in data1:
        key = generate_partition_key(data1_schema, data, keys)
        if ( key not in data2Itor ) :
            #print "cannot find ", key," in data2 "
            join_flag.append(0)
            continue
        result.append( data + data2Itor[key] )
        join_flag.append(1)
    return schema, result, join_flag
    
def generate_feature_vector_by_schema(data_dict_list, keep_schema):
    result = []
    for data_dict in data_dict_list:
        data = []
        for field in keep_schema:
            data.append(data_dict[field])
        result.append(data)
    return result
    
def partiton_csv_train_data(filename, partition_fields):
    f = open(filename, 'r')
    csv_schema_line = f.readline()
    csv_schema = csv_schema_line.replace('\n','').split('\t')
    filePointer = {}
    filenames = set()
    for line in f:
        data = {}
        tmp = line.replace('\n','').split('\t')
        for i in range(len(csv_schema)):
            if(tmp[i] == '') :
                data[csv_schema[i]] = numpy.nan
            else: 
                data[csv_schema[i]] = tmp[i]
        key = generate_partition_key(data, partition_fields)
        if key not in filePointer:
            partition_filename = "quality_" + key
            filenames.add( partition_filename )
            if len(filePointer) >= 20:
                closeFiles( filePointer )
                filePointer.clear()
            filePointer[key] = open( partition_filename , "a" )
        filePointer[key].write(line)
    f.close
    for k,v in filePointer.items():
        v.close
    return filePointer.keys()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
def closeFiles( filePointer ):
    for k,v in filePointer.items():
        v.close()

def generate_partition_key(data_schema, data, partition_fields):
    key = ""
    i = 0
    for field in partition_fields:
        if i == 0:
            if field not in data_schema:
                print "ERROR: data doesn't contain ", field, ", Data: ", data
                continue
            key = field+"-"+str(data[data_schema.index(field)])
            i = i+1
        else:
            key = key + "_" + field + "-" + str(data[data_schema.index(field)])
    return key
    
def count_pass_rate(data_list, indexOfResult):
    total_num = len(data_list)
    count = 0
    for data in data_list:
        if data[indexOfResult] == '1' :
            count = count + 1
    return count/(total_num+1.0)
    
def get_current_time():
    return time.strftime( ISOTIMEFORMAT, time.localtime() )
    
if __name__ == '__main__':

    # for patition quality data 
    # quality_train_file = 'quality_train.txt'    
    # partition_result = partiton_csv_train_data(quality_train_file, ["product_type","city_id","bank_id"])
    print get_current_time(), " start ..."
    # for partition 
    order_train_file = 'order_train.txt'
    order_schema, orders = read_csv_train_data(order_train_file)
    print get_current_time(), "Finish load ", order_train_file
    print get_current_time(), "Total order number: ", len(orders), " Order pass rate: ", count_pass_rate(orders, order_schema.index("result"))
    
    product_train_file = 'product_train.txt'
    product_schema, products = read_csv_train_data(product_train_file)
    print get_current_time(), "Finish load ", product_train_file
    
    #first merge product with order, expend product_id to with product 
    after_merge_schema, merged_order_with_product, join_tmp =  merge_feature_vector(order_schema, orders, product_schema, products, ["product_id"])
    print get_current_time(), "Finish merge order with product information."
    print get_current_time(), "Total order merged with product number: ", len(merged_order_with_product), " Order pass rate: ", count_pass_rate(merged_order_with_product, after_merge_schema.index("result"))    
    #print "Sample order with product: ", merged_order_with_product[0]
    
    #merge order with quality, need know which quality information is related with the order
    # city_id, product_type, bank_id, guarantee_type
    # first step: product_type-2_city_id-a87ff679a2f3e71d9181a67b7542122c_bank_id-cfcd208495d565ef66e7dff9f98764da
    quality_partition_filename = "quality_train.txt"
    #quality_partition_filename = "quality_partition_by_bct/quality_product_type-2_city_id-a87ff679a2f3e71d9181a67b7542122c_bank_id-cfcd208495d565ef66e7dff9f98764da"    
    quality_schema, qualitys = read_csv_train_data_by_schema(quality_partition_filename, ["user_id","city_id","bank_id","guarantee_type", "apply_from", "reapply_count"])
    print get_current_time(), "Finish load quality file ", quality_partition_filename, " total number: ", len(qualitys)
    #print "Sample quality : ", qualitys[0]

    after_merge_schema3, merged_order_with_product_with_quality, join_tmp = merge_feature_vector(after_merge_schema, merged_order_with_product, quality_schema, qualitys, ["user_id","city_id","bank_id"]) #,"city_id", "product_type", , "guarantee_type"
    print get_current_time(), "merged_order_with_product_with_quality count: ", len(merged_order_with_product_with_quality)
    print get_current_time(), "the rate of result = 1: ", count_pass_rate(merged_order_with_product_with_quality, after_merge_schema3.index("result"))

    #Load test data   
    order_test_file = "order_test_no_label.txt"
    order_test_schema, orders_test = read_csv_train_data(order_test_file)
    print get_current_time(), "Total order test number: ", len(orders_test)
    after_merge_schema, orders_test, join_tmp =  merge_feature_vector(order_test_schema, orders_test, product_schema, products, ["product_id"])
    print get_current_time(), "After merge with product, Total order test number: ", len(orders_test)    
   
    order_test_after_merge_schema, orders_test, join_flag = merge_feature_vector(after_merge_schema, orders_test, quality_schema, qualitys, ["user_id","city_id","bank_id"]) #,"city_id", "product_type", , "guarantee_type"
    print get_current_time(), "After merge with product and quality, Total order test number: ", len(orders_test), ", join flag length: ", len(join_flag)
  
    Y = Feature.get_features(merged_order_with_product_with_quality, after_merge_schema3.index('result'))
  
    #remove user_id, if the user id doesn't exist in train set, seems will have problem
    tree_train_feature_schema = [ "date", "term", "limit", "city_id", "bank_id", "product_type", "guarantee_type", "apply_from", "reapply_count" ]
    X_train = generate_feature_vector( after_merge_schema3, merged_order_with_product_with_quality, tree_train_feature_schema )  
    X_test = generate_feature_vector( order_test_after_merge_schema, orders_test, tree_train_feature_schema )  
  
    #clean unused memory
    orders = []
    products = []
    qualitys = []
    orders_test = []
    merged_order_with_product_with_quality = []
    merged_order_with_product = []
  
    '''
    X_train = X_train[:1000]
    Y = Y[:1000]
    X_test = X_test[:1000]
    join_flag=join_flag[:1000]
    '''
    
    X_combine = X_train + X_test
    #print "X: ", X
    #print "Y: ", Y
    
    vec = DictVectorizer()
    
    X_combine = vec.fit_transform([item for item in X_combine]).toarray()
    print get_current_time(), "finish transform X combine"
    #print "train feature names: ", vec.get_feature_names()
    X_train = X_combine[:len(X_train)]
    X_test = X_combine[len(X_train):]
        
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X_train, Y)
    print get_current_time(), "finish fit"
    
    Y_predict = clf.predict(X_test)
    print get_current_time(), "predict finish"

    print get_current_time(), "join_flag number: ", len(join_flag)
    print get_current_time(), "predict test: ", len(Y_predict)
    
    predict_result_file = "predict_"+ str(time.strftime( FILENAMEFORMAT, time.localtime() ) )
    f = open(predict_result_file+".txt", 'w')
    index = 0
    for i in join_flag:
        if i == 0:
            print >> f, '0'
        else:
            print >> f, str(int(Y_predict[index]))
            index = index + 1
            if index % 2000 == 0:
                f.flush()
    f.flush()
    f.close()
    
    print "importance:", clf.feature_importances_

    dot_data = StringIO.StringIO() 
    tree.export_graphviz(clf, out_file=dot_data) 
#    graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
#    graph.write_pdf( predict_result_file + ".pdf" )
        
'''    
    quality_train_file = 'partition_data/quality_application_type-9_product_type-2_city_id-a87ff679a2f3e71d9181a67b7542122c_bank_id-cfcd208495d565ef66e7dff9f98764da'
    quality_useful_schema = ["user_id","reapply_count","qid145","apply_from","spam_score","mobile_verify","quality"]
    quality_schema, qualitys = read_csv_train_data_by_schema(quality_train_file, quality_useful_schema)    
 
    merged_quality = merge_feature_vector(orders, qualitys, ["user_id","product_type","bank_id"])
'''
   
    
