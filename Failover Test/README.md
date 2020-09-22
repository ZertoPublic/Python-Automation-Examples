# Legal Disclaimer
This script is an example script and is not supported under any Zerto support program or service. The author and Zerto further disclaim all implied warranties including, without limitation, any implied warranties of merchantability or of fitness for a particular purpose.

In no event shall Zerto, its authors or anyone else involved in the creation, production or delivery of the scripts be liable for any damages whatsoever (including, without limitation, damages for loss of business profits, business interruption, loss of business information, or other pecuniary loss) arising out of the use of or the inability to use the sample scripts or documentation, even if the author or Zerto has been advised of the possibility of such damages. The entire risk arising out of the use or performance of the sample scripts and documentation remains with you.

# Failover Test 
Python based Zerto automated runbook for users to schedule boot delay between VPGs for Failover test operation. Automated example of how stop a failover test is included. Before initiating either example
user must complete the Failover-Test.ini file with the VPG name along with the desired boot delay in minutes

# Environment Requirements
- Python 3.7
- Network access to Zerto Virtual Manager(ZVM)

# Script Requirements 
- ZVM IP entered into file
- User, password with appropriate Zerto permissions entered when prompted 
- INI file completed and location specified within Python
