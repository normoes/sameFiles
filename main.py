#!/usr/bin/python

import os
import hashlib
import time


def getHash(contents):
    return hashlib.sha1(contents).hexdigest()

def walkPaths(path):
    for path, dirs, files in os.walk(path):
        for fileName in files:
            yield os.path.join(path,fileName)


if __name__ == '__main__':
    path = r'pathToCheckForDuplicates'
    files = {}
    for fileName in walkPaths(path):
        #start= time.time()
        fh =open(fileName, 'rb')
        h= getHash(fh.read())
        if not h in files.keys():
            ls = []
        else:
            ls = files.get(h)
        ls.append(fileName)
        files[h] = ls
        ##print fileName, getHash(fh.read())
        fh.close()
        #print time.time() - start

    for h,f in files.items():
        if len(f) > 1:
            print '\n'.join(f)
            print '--------'
