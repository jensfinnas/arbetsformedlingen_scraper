# encoding: utf-8
from time import sleep
import os
import csvkit as csv
import tables

def partition(alist, indices):
    """ Split a list into parts based on a set of indexes
        http://stackoverflow.com/questions/1198512/split-a-list-into-parts-based-on-a-set-of-indexes-in-python
    """
    return [alist[i:j] for i, j in zip([0]+indices, indices+[None])]

def file_exists(filename):
    """ Check if a file exists
    """
    return os.path.isfile(filename) 


def patiently(function, exception_to_catch, exception_to_raise=None, msg="", seconds=6):
    """ Execute a function repetedly with a short sleep until it does not 
        raise the error specified in the function.
        Used to handle async events on site.
    """
    if not exception_to_raise:
        exception_to_raise = exception_to_catch
    attempts = 10
    i = 0
    print "Execute function %s patiently" % function.__name__
    while i < attempts: 
        try:
            return function()
        except exception_to_catch:
            print i
            sleep( float(seconds) / float(attempts))
            i += 1
    raise exception_to_raise(msg)


def merge_csv_files(filelist):
    """ Pass a list of csv files and merge to DictList
    """
    data = tables.DictList()
    for file_name in filelist:
        reader = csv.DictReader(open(file_name))
        data += list(reader)

    return data

    