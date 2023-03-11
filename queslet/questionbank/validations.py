import re 


def standardizedText(s):
    s = s.replace('\n', '').replace('\r', '').strip()
    standardized = re.sub(' +',' ', s)
    return standardized