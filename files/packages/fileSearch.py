import re


def case_sensitivity(case):
    def new_func(func):
        def func_wrapper(*args, **kwargs): #line, pattern, substitute
            return func(case, *args, **kwargs) # line, pattern, substitute, case
        return func_wrapper
    return new_func
    
"""   
def tags(tag_name):
    def tags_decorator(func):
        def func_wrapper(name):
            return "<{0}>{1}</{0}>".format(tag_name, func(name))
#       def func_wrapper(*args, **kwargs):
#           return "<p>{0}</p>".format(func(*args, **kwargs))        
        return func_wrapper
    return tags_decorator
@tags("p")
def get_text(name):
    return "Hello "+name
print get_text("John")
# Outputs <p>Hello John</p>
"""    

@case_sensitivity(re.UNICODE)
def replace_inString_CaseSensitive(case, line, pattern, substitute):
    replace_pattern = re.compile(pattern, case)
    return replace_pattern.sub(substitute, line)
## replace_inString_CaseInsensitive1
## pattern is not interpreted as regular expression
@case_sensitivity(re.IGNORECASE|re.UNICODE)
def replace_inString(case, line, pattern, substitute):
    ## create a regular expression pattern ignoring the case
    replace_pattern = re.compile(re.escape(pattern), case)
    return replace_pattern.sub(repl=substitute, string=line)
## replace_inString_CaseInsensitive2
## re interprets pattern as regular expression
@case_sensitivity(re.IGNORECASE|re.UNICODE)
def replace_inString_regExpr(case, line, pattern, substitute):
    ## create a regular expression pattern ignoring the case
    replace_pattern = re.compile(pattern, case)
    return replace_pattern.sub(repl=substitute, string=line)

    
"""    
def match_inString_CaseSensitive(line, pattern):
    ## create a regular expression pattern ignoring the case
    #match_pattern = re.compile(re.escape(pattern), re.IGNORECASE)
    ## apply the regular expression pattern
    #return match_pattern.match(line)
    match = re.search(re.escape(pattern), line, re.UNICODE)
    if match is None:
        return False
    else:
        #print 'match string', match.group(0)[0:]
        return True
"""
# use this for strings
@case_sensitivity(re.IGNORECASE|re.UNICODE)
def match_inString(case, line, pattern):
    p=re.compile(re.escape(pattern), case)
    if len(p.findall(line)) > 0:
        return True
    return False

# use this when regular expressions are used
@case_sensitivity(re.UNICODE)
def match_inString_CaseSensitive(case, line, pattern):
    p=re.compile(pattern, case)
    if len(p.findall(line)) > 0:
        return True
    return False       
    
# use this when regular expressions are used
@case_sensitivity(re.IGNORECASE|re.UNICODE)
def match_inString_regExpr(case, line, pattern):
    p=re.compile(pattern, case)
    if len(p.findall(line)) > 0:
        return True
    return False   
@case_sensitivity(re.UNICODE)
def match_inString_regExpr_CaseSensitive(case, line, pattern):
    p=re.compile(pattern, case)
    if len(p.findall(line)) > 0:
        return True
    return False       

@case_sensitivity(re.UNICODE)
def get_matching_text_in_line_CaseSensitive(case, line, pattern):
    ## from a line like "translate('~delete ~profile ...')"
    p=re.compile(pattern, case)   
    return p.findall(line)
@case_sensitivity(re.IGNORECASE|re.UNICODE)
def get_matching_text_in_line(case, line, pattern):
    ## from a line like "translate('~delete ~profile ...')"
    p=re.compile(pattern, case)
    return p.findall(line)


if __name__ == "__main__":
    url = "https://www.google.de"
    print 'replace'
    print replace_inString(url, 'https://', 'http://')