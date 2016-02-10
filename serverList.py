#!/usr/bin/env python

import os
import sys
import argparse
from novaclient import client

# This script creates comma separated VM details 
#Declare global variables
#Before running the script source openstacksetup so that below env varaibles are setup OS_USERNAME, OS_PASSWORD, OS_TENANT_NAME and  OS_AUTH_URL
#creds dictionary will store all the credential to connect Openstack server
creds = {};
#flavours_dict will store all the system flavours and attributes of the flavours
flavours_dict = {};
#The CSV file will be generated in list filename in the /tmp folder. 
filename = "/tmp/list"

#This method defines all credentails and store in global vaiable
def set_nova_creds():
    creds['username'] = os.environ['OS_USERNAME']
    creds['api_key'] = os.environ['OS_PASSWORD']
    creds['project_id'] = os.environ['OS_TENANT_NAME']
    creds['auth_url'] = os.environ['OS_AUTH_URL']

#This method sets flavour mappings 
def set_flavour_dictionary():
    nova = client.Client('2',creds['username'],creds['api_key'],creds['project_id'],creds['auth_url'])

    #To get list of flavors which are public not visible also,  pass is_pubic=None parameter 
    # this is eqt nova flavor-list --all command
    flavours = nova.flavors.list(is_public=None)

    for flavour in flavours:
       #print "flavour ID from object: " + flavour.id
       flavours_dict[flavour.id] = flavour

    #Iterate values and get the outputs
    #for flavour in flavours_dict.itervalues():
    #   print "ID is :"+ str(flavour.id)
    #   print "Number of CPUs:" + str(flavour.vcpus)
    #   print "RAM :" + str(flavour.ram)

    #for flavour in flavours_dict:
    #   print  flavours_dict[flavour].id
    #   print  flavours_dict[flavour].vcpus
    #   print  flavours_dict[flavour].ram
    #   

def main():
    set_nova_creds()
    set_flavour_dictionary()
    fileobject = open(filename , "w")
    fileobject.write("ID,Name,Hostname,IP,CPUs,Memory,Disk\n")
 
    nova = client.Client('2',creds['username'],creds['api_key'],creds['project_id'],creds['auth_url'])
    # Print a list of all the running servers.
    for server in nova.servers.list(search_opts={'all_tenants':'1'}):
        serverDetails=None;
	      server_ID= getattr(server,'id')
        server_name =  getattr(server,'name')
        server_hostname =  getattr(server,'OS-EXT-SRV-ATTR:host')
	      flavour_id = str(server.flavor.itervalues().next())
        #print  "flavour ID is : " +flavour_id
        #Search flavor dictionary searching the flavor_id as  key
        flavour = flavours_dict[flavour_id]
        #print "Flavour ID is " + str(flavour.id)
        CPUs = str(flavour.vcpus)
        Memory = str(flavour.ram)
        Disk = str(flavour.disk)
        #Find the main IP address assigned to the instance.
        #Definitely, there might be better way to get the IP address.
        addresses = server.addresses.itervalues()
        for address in addresses:
            address = str(address)
        ip_address = address[address.find("'addr'")+10:address.find("OS-EXT-IPS:type")-5]  
        #print "IP address is:" +ip_address
        fileobject.write(server_ID+","+server_name+","+server_hostname+","+ip_address+","+CPUs+","+Memory+","+Disk +"\n") 
    fileobject.close()

if __name__ == '__main__':
    main()
