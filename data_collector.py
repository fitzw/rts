
# coding: utf-8

# In[220]:

from bs4 import BeautifulSoup
import sys
import time
import os
import requests
import codecs
import json
from optparse import OptionParser
key = 'Z4Y7a0W330WT1m6DUoHXhQ'
#url = 'http://realtime.mbta.com/developer/api/v2/predictionsbystop?api_key=wX9NwuHnZU2ToO7GmGR9uw&stop=place-bbsta&format=json'


# * "70154","70154","Copley - Inbound","",42.349974,-71.077447,"","",0,"place-coecl",0
# 
# * "70155","70155","Copley - Outbound","",42.349974,-71.077447,"","",0,"place-coecl",0

# 1. * Route_type = 0 -> subway
#    * 1 -> rail way
#    * 2 -> bus
#    
# 2. * 39 bus "175","175","Boylston St @ Dartmouth St","",42.350011,-71.077432,"","",0,"",0
# 
# 

# In[241]:

def get_stop_info(stop_id):
    stop = str(stop_id)
    url = 'http://realtime.mbta.com/developer/api/v2/predictionsbystop?'          'api_key='+key+'&stop='+stop+'&format=json'
    response = requests.get(url) 
    #text = response.text.encode('utf-8')
    data = json.loads(response.text)
    return data


# In[146]:

#data.keys() -> ['mode', 'stop_id', 'stop_name', 'alert_headers']


# In[240]:

def get_bus_info(stop_data,t_type,rount_n):
    if 'error' in stop_data.keys():
        print(stop_data)
    else:
        for i in stop_data['mode']:
            if i['mode_name'] == t_type:
                for route in i['route']:
                    if route['route_name']==str(route_n):
                        return route['direction'][0]['trip']
                else:
                    return 'This bus is unavailable or bus id not found.'


# In[147]:

#bus_data.keys() -> ['route_name', 'direction', 'route_id']


# In[168]:

#bus_data['direction'][0].keys() -> ['trip', 'direction_name', 'direction_id']


# In[238]:

#by default 
desired_stop = 171
t_type = 'Bus'
route_n = 39


# In[251]:

parser = OptionParser()
parser.add_option('-v', '--verbose', action='store_true')
parser.add_option('-o', '--output-file')
parser.add_option('-n', '--n_of_time', type = 'int')
parser.add_option('-s', '--desired_stop', type='str')
parser.add_option('-t', '--t_type', type='str')
parser.add_option('-r', '--route_n', type='int')
option, args = parser.parse_args()
if not option.output_file:
    print('specify input and output files')
    parser.print_help()
    sys.exit(1)
if not (option.desired_stop and option.t_type and option.route_n):
    print('specify correct input')
    parser.print_help()
    sys.exit(1)


# In[239]:

# if __name__ == "__main__":
#     desired_stop = sys.argv[1]
#     t_type = sys.argv[2]


# In[252]:

import pickle
def writer(l,filename):
    with open(filename, "wb") as fp: 
        pickle.dump(l, fp)


# In[253]:

def worker(n,desired_stop,t_type,route_n,filename):
    count = 0
    result = []
    while(count<0):
        stop_data = get_stop_info(desired_stop)
        bus_list = get_bus_info(stop_data,t_type,route_n)
        writer([n,bus_list],filename)
        result.append([n,bus_list])
        count+=1
        time.sleep(10)
        
worker(option.n_of_time,option.desired_stop,option.t_type, option.route_n, option.output_file)

