# Legal Disclaimer:
# ---------------------
# This script is an example script and is not supported under any Zerto
# support program or service. The author and Zerto further disclaim all implied warranties including,
# without limitation, any implied warranties of merchantability or of fitness for a particular purpose. In no event
# shall Zerto, its authors or anyone else involved in the creation, production or delivery of the scripts be liable
# for any damages whatsoever (including, without limitation, damages for loss of business profits,
# business interruption, loss of business information, or other pecuniary loss) arising out of the use of or the
# inability to use the sample scripts or documentation, even if the author or Zerto has been advised of the
# possibility of such damages.  The entire risk arising out of the use or performance of the sample scripts and
# documentation remains with you.

import time, requests, urllib3, getpass
from requests.auth import HTTPBasicAuth
from configparser import ConfigParser

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Declaring Environment variables
zvm_ip = "enterZVMip"
base_url = f"https://{zvm_ip}:9669/v1"
session = f"{base_url}/session/add"
vpgs_url = f"{base_url}/vpgs"
config_file = "Enterfilepath"


# vpg_list = []

###Functions####
def login(session_url, zvm_user, zvm_password):
    print("Getting ZVM API token...")
    auth_info = "{\r\n\t\"AuthenticationMethod\":1\r\n}"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = requests.post(session_url, headers=headers, data=auth_info, verify=False,
                             auth=HTTPBasicAuth(zvm_user, zvm_password))
    if response.ok:
        auth_token = response.headers['x-zerto-session']
        print("Api Token: " + auth_token)
        return auth_token
    else:
        print("HTTP %i - %s, Message %s" % (response.status_code, response.reason, response.text))

    # returned_token = login(session, zvm_u, zvm_p)


def main():

    print('Enter ZVM (likely vCenter administrator) credentials.')
    userName = str(input('Enter username (default: administrator@vsphere.local): ') or 'administrator@vsphere.local')
    passWd = getpass.getpass('Enter password: ')

    # Creating Header with x-zerto-session
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'x-zerto-session': login(session, userName, passWd)
    }

    # Gather VPG IDs from ZVM API
    vpg_response = requests.get(vpgs_url, headers=headers, verify=False)
    if vpg_response.ok:
        vpg_list = vpg_response.json()

    else:
        print("HTTP %i - %s, Message %s" % (vpg_response.status_code, vpg_response.reason, vpg_response.text))

        # Read in VPG INI File
    config = ConfigParser()
    config.read(config_file)
    vpg_length = len(vpg_list)

    for vpg in config.sections():
        x = 0
        while True:
            try:
                for i in range(vpg_length):

                    for key, value in vpg_list[x].items():
                        if key == 'VpgName':
                            if value == vpg:  # Once VpgName and VpgIdentifier match, execute a failover
                                print('Executing a failover of ' + value + ', VPG ID ' + str(
                                    vpg_list[x]['VpgIdentifier']))
                                requests.post(vpgs_url + '/' + str(vpg_list[x]['VpgIdentifier']) + '/FailoverTest',
                                              headers=headers, verify=False)
                                print('Waiting ' + (config.get(vpg_list[x]['VpgName'], 'bootdelay')) + ' minutes.')
                                time.sleep(int(config.get(vpg_list[x]['VpgName'], 'bootdelay')) * 60)
                    x = x + 1
            except IndexError:  # Break after x exceeds index length of vpg_list
                break  #

    endSession(headers)


def endSession(sessionHeader):
    print('Ending session.')
    response = requests.delete(base_url + '/session', headers=sessionHeader, verify=False)


main()

'''
To do:
* Hash password
#hashtag


'''
