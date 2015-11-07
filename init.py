import pymongo
import csv
import json

def import_lists(filename):
    con = pymongo.MongoClient('localhost', 27017)
    db = con["meanspend"]
    col = db["data"]
    file_d = open(filename, "r", encoding='UTF-8')
    table = csv.DictReader(file_d)
    for line in table:
        line.pop('size')
        if bool(col.find_one({'code': line['code']})):
            resp = col.update_one({'code': line['code']}, {'$set': {'files_2015': line['files_2015']} })
        else:
            resp = col.insert(line)
            
            
            
import_lists("files_list_with_codes_2014.csv")
import_lists("files_list_with_codes_2015.csv")
    