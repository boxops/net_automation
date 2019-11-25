# Set Up an IOS Router or Switch as SSH Client
# There are four steps required to enable SSH support on a Cisco IOS router:

# 1. Configure the hostname command.
# 2. Configure the DNS domain.
# 3. Generate the SSH key to be used.
# 4. Enable SSH transport support for the virtual type terminal (vtys).


# configure terminal
# hostname R1
# ip domain name cisco.com
# username admin privilege 15 password Cisco123
# line vty 0 4
# login local
# transport input all
# exit
# crypto key generate rsa
# 1024
# ip ssh version 2
# banner motd # Unauthorised access is strictly prohibited! #
# end
# wr
