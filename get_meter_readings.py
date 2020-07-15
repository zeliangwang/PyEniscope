#%%
# -*- coding: utf-8 -*-
"""An example Python script used to retrieve Eniscope metering data via ENISCOPE CORE API.

Created by Z. Wang @ Best.Energy
22/07/2019

"""

import requests
import json
import datetime
import calendar
from requests.auth import HTTPBasicAuth

#########################################################################################
# Before using Eniscope Core API, you have to specify your API key, usename and password,
# Please contact Best.Energy to request the API access.
#########################################################################################
# API header
headers = {'X-Eniscope-API': "<API Key>", # specify your API key
            'Accept': "/",
            'Host': "core.eniscope.com"}
# API usename and password
auth = HTTPBasicAuth('<Username>', '<Password>')  # specify your username and password

r = requests.get('https://core.eniscope.com/', headers=headers, auth=auth)
print(r)  # Sucessfully accessed if the response code is "200"

#%%
#########################################################################################
# Request all meters info under the specified org_id
#########################################################################################
org_id = '17158'  # Specify Organisation ID
meters_url = f"https://core.eniscope.com/v1/organizations/{org_id}/metersbelow"
resp_meters = requests.request("GET", meters_url, headers=headers, auth=auth)
# print("\nReturned meters-below:\n")
# print(json.dumps(resp_meters.json(), ensure_ascii=False, indent=2))

fname = f'meters-below-{org_id}.json'
with open('results/'+fname,'w', encoding='utf-8') as outfile:
    json.dump(resp_meters.json(), outfile, ensure_ascii=False, indent=2)

#%%
#########################################################################################
# Request all data view IDs based on a meter UUID
#########################################################################################
UUID = '5410eca8722e0001' # UUID of a Eniscope meter channel 
url_channelList = f"https://core.eniscope.com/v1/channels/?uuid={UUID}"
respChannels = requests.request("GET", url_channelList, headers=headers, auth=auth)
# print("\nReturned data channel IDs for the UUID ({}):\n".format(url_channelList[-16:]))
# print(json.dumps(respChannels.json(), ensure_ascii=False, indent=2))

fname2 = f'data-view-ids-{UUID}.json'
with open('results/'+fname2,'w', encoding='utf-8') as outfile:
    json.dump(respChannels.json(), outfile, ensure_ascii=False, indent=2)

# data channel infomation
dc_info = {'organizationName':[], 'organizationId':[], 'uuId':[], 
            'dataChannelId':[], 'channelName':[], 'displayedPhase':[]}
for dc_dict in respChannels.json()["channels"]:
    dc_info['organizationName'].append(dc_dict['organizationName'])
    dc_info['organizationId'].append(dc_dict['organizationId'])
    dc_info['uuId'].append(dc_dict['uuId'])
    dc_info['dataChannelId'].append(dc_dict['dataChannelId'])
    dc_info['channelName'].append(dc_dict['channelName'])
    dc_info['displayedPhase'].append(dc_dict['displayedPhase'])
print(dc_info)

#%%
#########################################################################################
# Request all data view IDs based on a meter UUID
#########################################################################################
# specify the date range of meter readings
start_date = "20200701"  
end_date = "20200707"

# covert to datetime object
dt_1 = datetime.datetime.strptime(start_date, "%Y%m%d")
dt_2 = datetime.datetime.strptime(end_date, "%Y%m%d")
ts_1 = int(calendar.timegm(dt_1.timetuple()))  # utc timestamp
ts_2 = int(calendar.timegm(dt_2.timetuple()))  # utc timestamp
print("Start date: {}, timestamp: {}\n End date: {}, timestamp: {}".format(dt_1,ts_1, dt_2,ts_2))

# API query string
# note that "daterange" doesn't include "str(ts_2 + 86400)"
querystring = {"action":"summarize","daterange[]":[str(ts_1), str(ts_2 + 86400)], 
                "res":"60",  # choose one minute resolution
                "fields[]":["ts", "E","E1","E2","E3","P", "P1","P2","P3","I","I1","I2", "I3"]
                }
dc_id = '59155'  # specify the data view id of meter readings 
url_readings = f"https://core.eniscope.com/v1/readings/{dc_id}/"

fname = f'readings-{dc_id}.json'
respReadings = requests.request("GET", url_readings, headers=headers, auth=auth, params=querystring)
# print(respReadings.status_code)

# save readings into json file
with open('results/' + fname,'w', encoding='utf-8') as outfile:
    json.dump(respReadings.json(), outfile, ensure_ascii=False, indent=2)

# %%
