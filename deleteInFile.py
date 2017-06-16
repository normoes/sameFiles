import os
import packages.fileSearch as fileSearch
import packages.FileOperations as fileOps
import time # for backup folders


"""
    multiline properties impemented
    object dependency implemented
"""

temp_dir = r'C:\Temp\Python_Backup'

def delete_lines_with(root_dir, file_extension, identifier, dependency, search_Func):
    print 'Start:'
    print 'Delete lines containing:', identifier
    file_list = list()
    new_lines = list()
    multiLine = False

    
    if (dependency and len(identifier) > 1) or not dependency:  
        for root, subFolders, files in os.walk(root_dir):
            ## get file extension
            ##filename, fileExtension = os.path.splitext(os.path.join(subFolders, files))
            filenames = [os.path.join(root, name) for name in files if os.path.splitext(os.path.join(root, name))[1] == file_extension ]        
            for name in filenames:
                line_no = 0
                try:
                    somethingNewFound = False
                    idFound = False
                    # empty the list again
                    del new_lines[:]
                    with open(name, 'r') as file1:
                        for line in file1:
                            line_no += 1
                            new_lines.append(line)
                            if line.strip():
                                line = line.strip()
                                if multiLine:
                                    if line.startswith("'"):
                                        new_lines.pop()
                                        print ' line no.', line_no, ' --> ', line
                                        continue
                                    else:
                                        multiLine = False
                                        if idFound:
                                            idFound = False
                                ## search with regular expression support
                                ## --> object or inherited starts a new component: reset idFound
                                if fileSearch.match_inString_regExpr(line, '^object') or fileSearch.match_inString_regExpr(line, '^inherited'):
                                    idFound = False
                                if dependency and not idFound:
                                    ## search first identifier without regular expression support
                                    if fileSearch.match_inString(line, identifier[0]):
                                        idFound = True
                                        continue # next line, further checking
                                else:                                
                                    for ID in identifier:
                                        ## at the moment, do not use match_in_strin_regExpr here
                                        ## --> 'self.List' would not be found, because of the interpretaion of '.'
                                        if search_Func(line, ID):      
                                            if (dependency and idFound and not search_Func(line, identifier[0])) or not dependency:
                                                new_lines.pop()
                                                if line.startswith('//') == False:
                                                    if len(line.split('=')) > 1:
                                                        multiLine = line.split('=')[1] == ''
                                                    somethingNewFound = True
                                                    if name in file_list: 
                                                        pass
                                                    else:
                                                        print 'FILE: ', name
                                                        file_list.append(name)                                                        
                                                    print ' line no.', line_no, ' --> ', line
                                            if dependency:
                                                idFound = False                             
                    if somethingNewFound:                        
                        if not dry_run:
                            if fileOps.backup_file(name, os.path.dirname(name)[len(root_dir)+1:], temp_dir, True):
                            # replace contents only with successful backup
                                with open(name, 'w') as fh:
                                    print 'writing new lines'
                                    fh.writelines(new_lines)
                        else:
                            print 'DRY_RUN:', name
                        print 'identifier:', identifier, ' deleted in file:', name
                    
                except Exception as e:
                    import sys
                    print e
                    print 'exception:', name
                    e = sys.exc_info()[0]
                    print ("Error: %s" % e )      
    
    else:
        print 'when using dependency, make sure there are at least 2 identifiers in parameter identifier'
    print 'Done.'
    return file_list



if __name__ == '__main__':
    root_dir = r'C:\Users\nom\Documents\SVN\CodeBeamer\src'
    ## this is a two step identifier
    identifier = ('TFestoLabel', '^Text =[.]*');  #TFestoRadioButton
    #identifier = ('TFestoCheckListBox', '^Checked =[.]*');  #TFestoRadioButton
    ## only when [0] (TFestoLabel) is found accept [1]
    ## see identifier_dependency        
    #identifier = ('Offset_Image_Left', )
    #identifier = ('ImageButtonBox', )
    #identifier = ('self.List', )
    #identifier = ('TFestoRichedit', 'Zoom ');
    
    #identifier = ('Zoom[ ]*=', );
    ## files to be found
    #file_extension = '.pas'
    file_extension = '.dfm'   
    file_list = list()

    ## identifier_dependency:
    ## first identifier allows finding following identifiers in list of identifiers    
    ## e.g.: when searching for a property in .dfm files, which only should be deleted for TButton
    ##    --> start matching ONLY AFTER TButton was found previously
    identifier_dependency = False 
    dry_run = True
    #search_Func_forIDs = fileSearch.match_inString
    search_Func_forIDs = fileSearch.match_inString_regExpr 
    file_list = delete_lines_with(root_dir, file_extension, identifier, identifier_dependency, search_Func_forIDs)
    
    #for value in file_list:
    #    print value  
