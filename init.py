import pymongo
import csv

def import_lists(filename,year):
    con = pymongo.MongoClient('localhost', 27017)
    db = con["meanspend"]
    col = db[year]
    file_d = open(filename, "r", encoding='UTF-8')
    table = csv.DictReader(file_d)
    
    
import_lists("files_list_with_codes_2014.csv", '2014')
import_lists("files_list_with_codes_2015.csv", '2015')
    