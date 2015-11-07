import io
import csv
import pymongo
import statistics
import tqdm
import os

#import numpy as np
#import pandas as pd


def main(datapath='data'):
    con = pymongo.MongoClient('localhost', 27017)
    db = con["meanspend"]
    col = db['data']
    for root, dirs, files in os.walk(datapath, topdown=False):
        for filename in tqdm(files):
            process_file(filename)
               
                
def process_file(filename):
    #data = np.recfromcsv(filename, delimiter=',', filling_values=numpy.nan, case_sensitive=True, deletechars='', replace_space=' ')
    with io.open(filename,"r", encoding='UTF-8') as source_file:
        data_iter = csv.DictReader(source_file)
        #data = [data for data in data_iter]
        pricelist = []
        unitlist = []
        for line in data_iter:
            pricelist.append(line['product_price'])
            unitlist.append(line['OKEI_name'])
        price_med = statistics.median(pricelist)
        unit_mode = statistics.mode(unitlist)
        #df = pd.DataFrame(data)
        
    return price_med, unit_mode

def get_median(data):
        
    return 

