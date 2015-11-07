import io
import csv
import pymongo
import statistics
from tqdm import tqdm
import os

#import numpy as np
#import pandas as pd


def maintest(datapath='data'):
    con = pymongo.MongoClient('localhost', 27017)
    db = con["meanspend"]
    col = db['data']
    for root, dirs, files in os.walk(datapath, topdown=False):
        for filename in tqdm(files):
            if bool(col.find_one({'$or': [{'files_2015': filename}, {'files_2014':filename}]})):
                (price_med, unit_mod, med_outliers, mod_outliers) = process_file(os.path.join(datapath,filename))
                resp = col.update_one({'files_2015': filename }, {'$set': {'price_med15': price_med, 'unit_mod15': unit_mod, 
                                        'mod_outliers': mod_outliers, 'med_outliers': med_outliers}})
            print(" -----------------/n %s" % str(col.find_one({'$or': [{'files_2015': filename}, {'files_2014':filename}]})))
              


def mongomain(datapath = 'data2'):
    con = pymongo.MongoClient('localhost', 27017)
    db = con["meanspend"]
    col = db['data']
    for item in col.find():
        filepath14 = item['files_2014']
        filepath15 = item['files_2015']
        (price_med14, unit_mod14) = process_file(os.path.join(datapath, filepath14))
        (price_med15, unit_mod15) = process_file(os.path.join(datapath, filepath15))
        resp = col.update_one({'code': item['code'] }, 
                        {'$set': {'price_med14': price_med14, 'price_med15': price_med15,'unit_mod14': unit_mod14, 'unit_mod15': unit_mod15} })
        if resp:
            print(resp)
        
    return True    
        
def mongolist():    
    con = pymongo.MongoClient('localhost', 27017)
    db = con["meanspend"]
    col = db['data']
    for item in col.find():
        print(item)

def process_file(filename):
    #data = np.recfromcsv(filename, delimiter=',', filling_values=numpy.nan, case_sensitive=True, deletechars='', replace_space=' ')
    with io.open(filename,"r", encoding='UTF-8') as source_file:
        data_iter = csv.DictReader(source_file)
        #data = [data for data in data_iter]
        pricelist = []
        unitlist = []
        for line in data_iter:
            pricelist.append(float(line['product_price']))
            unitlist.append(line['OKEI_name'])
        price_med = statistics.median(pricelist)
        unit_mode = statistics.mode(unitlist)
        #df = pd.DataFrame(data)
    
    med_outliers = []
    mod_outliers = []
    
    with io.open(filename,"r", encoding='UTF-8') as source_file:
         data_iter = csv.DictReader(source_file)
         for line in data_iter:
            if line['OKEI_name'] != unit_mode:
                mod_outliers.append(line)
            if (float(line['product_price'])/price_med) > 3:
                med_outliers.append(line)
        
    return price_med, unit_mode, med_outliers, mod_outliers

def get_median_outliers(data):
        
    return True

def get_mod_outliers(data):
    
    return True