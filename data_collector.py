
# coding: utf-8

# In[44]:

from bs4 import BeautifulSoup
import sys
import time as tm
from datetime import datetime, time
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

# In[56]:

def get_stop_info(stop_id):
    stop = str(stop_id)
    url = 'http://realtime.mbta.com/developer/api/v2/predictionsbystop?'          'api_key='+key+'&stop='+stop+'&format=json'
    response = requests.get(url) 
    #text = response.text.encode('utf-8')
    data = json.loads(response.text)
    return data


# In[146]:

#data.keys() -> ['mode', 'stop_id', 'stop_name', 'alert_headers']


# In[87]:



# In[79]:

def get_bus_info(stop_data,t_type,route_n):
    if 'mode' not in stop_data.keys():
        print('service goes offline @ %d:%d'%(datetime.now().hour,datetime.now().minute))
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


# In[38]:

#import pickle
def writer(l,filename):
    with open(filename+'.txt', "w") as fp: 
        for item in l:
            fp.write("%s\n" % item)
    #print(filename+' is written @ '+str(datetime.now()))
    return str(filename+' is written @ '+str(datetime.now()))


# In[331]:

from progressbar import*


# In[45]:

# def worker(n,desired_stop,t_type,route_n,filename):
#     count = 0
#     result = []
#     progress = ProgressBar(n, fmt=ProgressBar.FULL)
#     while(count<n):
#         progress.current += 1
#         progress()
#         stop_data = get_stop_info(desired_stop)
#         bus_list = get_bus_info(stop_data,t_type,route_n)
#         #print([count,bus_list])
#         result.append([count,datetime.now(),bus_list])
#         count+=1
#         tm.sleep(10)
#     progress.done()
#     writer(result,filename)
#     return result
        
# #worker(1800,171,'Bus',39,'test.txt')


# In[55]:
now = datetime.now()
now_time = now.time()
n,desired_stop, t_type, route_n = \
                    input("Please enter parameters in format of: n, stop_id, type, route_n =>").split(',')

#360,175,'Bus',39
count = 0
while(True):
    if (time(4,30) <= now.time() <= time(23,59)) or (time(0,0) <= now.time() <= time(1,0)):
        filename = 'output/'+tm.strftime("%b")+str(datetime.now().day)+'_'
        saved_ = filename+"%d" %(count//int(n))
        curr = 0
        result = []
        progress = ProgressBar(int(n), fmt=ProgressBar.FULL)
        while(curr<int(n)):
            progress.current += 1
            progress()
            stop_data = get_stop_info(desired_stop)
            bus_list = get_bus_info(stop_data,t_type,route_n)
            #print([count,bus_list])
            result.append([count,datetime.now(),bus_list])
            curr+=1
            count+=1
            tm.sleep(10)
        progress.done()
        print('Data_%d collected, writting to file: ' %(count//int(n)-1)+saved_ )
        msg = writer(result,saved_)
        if msg:
            print(msg)
# In[32]:

# #by default 
# desired_stop = 175
# t_type = 'Bus'
# route_n = 39

