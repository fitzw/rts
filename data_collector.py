
# coding: utf-8

# In[303]:

from bs4 import BeautifulSoup
import sys
import time
import datetime
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


# In[277]:

def get_bus_info(stop_data,t_type,rount_n):
    if 'mode' not in stop_data.keys():
        print('service goes offline')
    else:
        for i in stop_data['mode']:
            if i['mode_name'] == t_type:
                for route in i['route']:
                    if route['route_name']==str(route_n):
                        return route['direction'][0]['trip']
    return 'This bus is unavailable or bus id not found.'


# In[147]:

#bus_data.keys() -> ['route_name', 'direction', 'route_id']


# In[168]:

#bus_data['direction'][0].keys() -> ['trip', 'direction_name', 'direction_id']


# In[312]:

#by default 
desired_stop = 175
t_type = 'Bus'
route_n = 39


# In[263]:

# parser = OptionParser()
# parser.add_option('-v', '--verbose', action='store_true')
# parser.add_option('-o', '--output-file')
# parser.add_option('-n', '--n_of_time', type = 'int')
# parser.add_option('-s', '--desired_stop', type='str')
# parser.add_option('-t', '--t_type', type='str')
# parser.add_option('-r', '--route_n', type='int')
# option, args = parser.parse_args()
# if not option.output_file:
#     print('specify input and output files')
#     parser.print_help()
#     sys.exit(1)
# if not (option.desired_stop and option.t_type and option.route_n):
#     print('specify correct input')
#     parser.print_help()
#     sys.exit(1)


# In[239]:

# if __name__ == "__main__":
#     desired_stop = sys.argv[1]
#     t_type = sys.argv[2]


# In[291]:

#import pickle
def writer(l,filename):
    with open(filename, "w") as fp: 
        for item in l:
            fp.write("%s\n" % item)


# In[331]:

from progressbar import*


# In[332]:

def worker(n,desired_stop,t_type,route_n,filename):
    count = 0
    result = []
    progress = ProgressBar(n, fmt=ProgressBar.FULL)
    while(count<n):
        progress.current += 1
        progress()
        stop_data = get_stop_info(desired_stop)
        bus_list = get_bus_info(stop_data,t_type,route_n)
        #print([count,bus_list])
        result.append([count,datetime.datetime.now(),bus_list])
        count+=1
        time.sleep(10)
    progress.done()
    writer(result,filename)
    return result
        
#worker(1800,171,'Bus',39,'test.txt')


# In[333]:

worker(3,175,'Bus',39,'t1.txt')

