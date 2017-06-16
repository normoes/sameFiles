def which(program, debug = False):
    import os
    def is_exe(fpath):        
        # return os.path.isfile(fpath) and os.access(fpath, os.X_OK) # --> swcurity hole https://docs.python.org/3/library/os.html#os-file-dir
        ## more secure approach:
        hasPermission = True
        try:
            fp = open(fpath)
        except PermissionError:
            hasPermission = False 
        else:
            fp.close()
        return os.path.isfile(fpath) and hasPermission 
        
    def adapt_extension(fname):
        if os.name == 'nt':
            if os.path.splitext(fname)[1] != '.exe':
                return ''.join([fname, '.exe'])
        return fname
            
    fpath = os.path.split(program)[0]
    fname = adapt_extension(program)    
    if fpath:
        if is_exe(fname):
            return fname
    else:
        for path in os.environ["PATH"].split(os.pathsep):             
            path = path.strip('"')
            exe_file = os.path.join(path, fname)      
            if is_exe(exe_file):
                return exe_file

    return None

if __name__ == "__main__":
    import sys
    #print sys.argv
    try:
        assert(len(sys.argv) > 1), 'no argument provided'
        print which(sys.argv[1], True)
    except AssertionError as e:
        print e