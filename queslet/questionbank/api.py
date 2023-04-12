
import requests
from requests.auth import HTTPBasicAuth


def api_encode(text):
    
    link = 'http://127.0.0.1:8000/model/encode?mcq=' + text
    print(link)
    basic = HTTPBasicAuth('manhpd15', 'Test1508')
    response = requests.get(link,auth=basic)
    encode = response.json()['encode']
    return encode 
    # print(response.json() )
    