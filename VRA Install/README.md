# Legal Disclaimer
This script is an example script and is not supported under any Zerto support program or service. The author and Zerto further disclaim all implied warranties including, without limitation, any implied warranties of merchantability or of fitness for a particular purpose.

In no event shall Zerto, its authors or anyone else involved in the creation, production or delivery of the scripts be liable for any damages whatsoever (including, without limitation, damages for loss of business profits, business interruption, loss of business information, or other pecuniary loss) arising out of the use of or the inability to use the sample scripts or documentation, even if the author or Zerto has been advised of the possibility of such damages. The entire risk arising out of the use or performance of the sample scripts and documentation remains with you.

# Python---Zerto-VRA-Deployment-
Python based Zerto VRA deployment, user will need to fill out the vras.json file first for each host they would like to deploy a Zerto VRA on. The json file will then be read in by Python to determine the VRA installation options. Within the JSON example they will need to specificy required VRA install options including datastore, network, vra group, as well as static IP information 

# Environment Requirements
- Python 3.7
- Network access to Zerto Virtual Manager(ZVM)

Script Requirements 
- ZVM IP, user, password with permissions to access the API of the ZVM
- vras.json file completed and location specified within Python
- vras.json file accessible by host running Python
