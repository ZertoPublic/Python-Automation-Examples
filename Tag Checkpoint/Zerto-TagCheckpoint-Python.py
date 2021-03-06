# Legal Disclaimer:
#----------------------
#This script is an example script and is not supported under any Zerto support program or service.
#The author and Zerto further disclaim all implied warranties including, without limitation, any implied warranties of merchantability or of fitness for a particular purpose.
#In no event shall Zerto, its authors or anyone else involved in the creation, production or delivery of the scripts be liable for any damages whatsoever (including, without 
#limitation, damages for loss of business profits, business interruption, loss of business information, or other pecuniary loss) arising out of the use of or the inability 
#to use the sample scripts or documentation, even if the author or Zerto has been advised of the possibility of such damages.  The entire risk arising out of the use or 
#performance of the sample scripts and documentation remains with you.

#importing request, json
#importing HTTPBasicAuth library for ZVM basic authentication 
import requests 
import json 
from requests.auth import HTTPBasicAuth 

#Declaring Environment variables 
zvm_ip = "zvmip"
zvm_u = "zvmusername"
zvm_p = "zvmpassword" 
base_url = "https://"+zvm_ip+":9669/v1"
session = base_url+"/session/add"
vpg_url = base_url + "/vpgs"
vpg_name = "VPGName"

###Functions####
def login(session_url, zvm_user, zvm_password):
   print("Getting ZVM API token...")
   auth_info = "{\r\n\t\"AuthenticationMethod\":1\r\n}"
   headers = {
     'Accept': 'application/json',
     'Content-Type': 'application/json'
   }
   response = requests.post(session_url, headers=headers, data=auth_info, verify=False, auth=HTTPBasicAuth(zvm_user, zvm_password))
   if response.ok: 
      auth_token = response.headers['x-zerto-session']
      print("Api Token: " + auth_token)
      return auth_token
   else: 
      print("HTTP %i - %s, Message %s" % (response.status_code, response.reason, response.text))   

returned_token = login(session, zvm_u, zvm_p)

# Creating Header with x-zerto-session 
headers = {
   'Accept': 'application/json',
   'Content-Type': 'application/json',
   'x-zerto-session': returned_token
}

# Get VPG ID 
vpg_response = requests.get(vpg_url, headers=headers, verify=False)
vpg_response = vpg_response.json()

# Retrieve VPG ID from ZVM API 
for i in (range(len(vpg_response))):
   if vpg_response[i]['VpgName'] == vpg_name: 
      vpg_id = vpg_response[i]['VpgIdentifier']
   else:
      pass

#Post Tag Checkpoint to ZVM API
checkpoint_url = vpg_url + "/" + vpg_id + "/checkpoints"
checkpoint_body= {
   "CheckpointName" : "TestingCheckpointTagging"
}
tag_checkpoint = requests.post(checkpoint_url, headers=headers, data=json.dumps(checkpoint_body), verify=False)
if tag_checkpoint.status_code != 200:
      print(tag_checkpoint.text)
