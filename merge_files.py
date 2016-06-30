# encoding: utf-8
import os
import csvkit as csv
from modules.tables import DictList

def iterate_and_parse_files(sub_directory):
    """ Merge all csv files in folder to list of dicts
    """
    data = DictList()
    folder = os.getcwd() + "/" + sub_directory
    for file_name in os.listdir(folder):
        reader = csv.DictReader(open(folder + file_name))
        data += list(reader)
    return data



data = iterate_and_parse_files("data/overview/")
data.save_as("data/overview.csv")