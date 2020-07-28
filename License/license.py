#!/usr/bin/python
#This script is an example script and is not supported under any Zerto support program or service. The author and Zerto further disclaim all implied warranties including, without
#limitation, any implied warranties of merchantability or of fitness for a particular purpose.

#In no event shall Zerto, its authors or anyone else involved in the creation, production or delivery of the scripts be liable for any damages whatsoever (including, without 
#limitation, damages for loss of business profits, business interruption, loss of business information, or other pecuniary loss) arising out of the use of or the inability to use
#the sample scripts or documentation, even if the author or Zerto has been advised of the possibility of such damages. The entire risk arising out of the use or performance of 
#the sample scripts and documentation remains with you.
import requests 
import json 
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#Declaring Environment variables 
zvm_ip = "enterZVMip"
zvm_u = "enterZVMuser"
zvm_p = "enterZVMpass" 
base_url = f"https://{zvm_ip}:9669/v1"
session = f"{base_url}/session/add"
license_url = f"{base_url}/license"
key = "enterZERTOlicense"

###Functions####
#Function to get x-zerto-session key for API use
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

###End Functions####

# Creating Header with x-zerto-session 
headers = {
   'Accept': 'application/json',
   'Content-Type': 'application/json',
   'x-zerto-session': returned_token
}

# Creating license body to apply key
license_body = {
    "LicenseKey": key
}

#Put request for new license
license_request = json.dumps(license_body)
response = requests.put(license_url, data=license_request, headers=headers, verify=False)
if response.status_code != 200:
   print(response.text)
else: 
   exit()
