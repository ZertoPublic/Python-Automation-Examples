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
zerto_port = "9071"
peer_zvmip = "enterPeerZVMIp"
base_url = f"https://{zvm_ip}:9669/v1"
session = f"{base_url}/session/add"
peerbase_url= f"https://{peer_zvmip}:9669/v1"
peer_session = f"{peerbase_url}/session/add"
pairing_url = f"{base_url}/peersites"
token_url = f"{peerbase_url}/peersites/generatetoken"

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

peerzvm_token = login(peer_session, zvm_u, zvm_p)

# Creating Header with x-zerto-session 
headers = {
   'Accept': 'application/json',
   'Content-Type': 'application/json',
   'x-zerto-session': peerzvm_token
}

#Generating pairing token from recovery site
pairing_token = requests.post(token_url, headers=headers, verify=False)
pairing_token = pairing_token.json()

#Authenticate with Prod ZVM
prodzvm_token = login(session, zvm_u,zvm_p)

prod_headers = {
   "Accept": "application/json",
   "Content-Type": "application/json",
   "x-zerto-session": prodzvm_token
}

#Create Body for pairing request
pairing_body = {
   "HostName": peer_zvmip,
   "Port": zerto_port,
   "Token": pairing_token['Token']
}
body = json.dumps(pairing_body)

#Initiate Pairing Request 
pairing_request = requests.post(pairing_url, data=body, headers=prod_headers, verify=False)
if pairing_request.status_code == 200: 
   task_id = pairing_request.text
   print("Site Pairing Task: "+task_id)
else: 
   print("Pairing failed Status Code: "+pairing_request.status_code)
   print(pairing_request.text)
   pass

