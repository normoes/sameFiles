import os
import datetime
import shutil

def backup_file(srcfile, directory_structure, dstdir, debug = False):   
    #print '1', srcfile
    #print '2', directory_structure
    folder_time = datetime.datetime.utcnow().strftime("%Y_%m_%d__%H-%M")
    #print '3',dstdir
    dstdir = os.path.join(dstdir,folder_time,directory_structure)
    #if debug:
    #    print 'backup path:', dstdir
    try:
        try:
            os.makedirs(dstdir) ## create all directories, raises an error if it already exists
        except Exception as e:
            #import sys
            #print e
            #e = sys.exc_info()[0]
            #print ("Error: %s" % e )  
            print dstdir, 'already exists'
    finally:
        try:
            shutil.copy(srcfile, dstdir)
            if debug:
                print 'file backed up in', dstdir
            return True
        # eg. src and dest are the same file
        except shutil.Error as e:
            print('Error: %s' % e)
        # eg. source or destination doesn't exist
        except IOError as e:
            print('Error: %s' % e.strerror)    
        except Exception as e:
            print('Error: %s' % e.strerror)
             
    return False
