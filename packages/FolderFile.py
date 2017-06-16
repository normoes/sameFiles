import os
import csv
import errno

def isValidFile(filePath):
    if os.path.exists(filePath) and os.path.isfile(filePath):
        return True
    return False
def isValidFolder(filePath):
    if os.path.exists(filePath) and os.path.isdir(filePath):
        return True
    return False   

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

## open folder or file
def openFolder(path):
    import platform
    import subprocess
    path = os.path.normpath(path)
    if isValidFolder(path):
        print 'exists'
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
            
def generateLinesOfFiles(filePath):        
    if isValidFile(filePath):
        with open(filePath, 'r') as fh: # also closes file
            for line in fh.readlines():
                line = line.rstrip()
                if line:
                    yield line
                else:
                    yield '----'
    yield '' 
 
## don't forget to close the file, when done 
def getCsvReader(filePath, debug=False):   
    if os.path.exists(filePath) and os.path.isfile(filePath):
        fh = open(filePath, 'rb')
        fieldnames = list()
        header = fh.readline()  
        try:          
            if header.rstrip():
                fieldnames.extend(header.rstrip().split(';'))
        except Exception as e:
            print e
        if debug:
            print fieldnames
        return csv.DictReader(fh, fieldnames, delimiter=";"), fh
    return None, None
        
## don't forget to close the file, when done 
def createCsv(filename, fieldnames, mode='ab'):   
    fh = None
    print 'creating csv'
    print filename
    try:
        #filecheck = filechecker.fileChecker()        
        fh = open(filename, mode) # 'ab'
        
        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter=";")
        print writer
        print fieldnames
        print 'returning csv'
        return writer, fh
    except:
        return None, None        
    

def humansize(nbytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    if nbytes == 0: return '0 B'
    i = 0
    while nbytes >= 1024 and i < len(self.suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, self.suffixes[i])     
    
def isEmpty(name):
    try:
        size = os.path.getsize(name)
    except OSError as e:
        print e
        size = 0
    return not(size > 0 )
