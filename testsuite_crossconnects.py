import os
import sys

from lib.crossconnects import *


### cross connects operations 

def oxC(opr):
    
    if opr == "connectSwitch":
        """Usage: <hostIP> <netconf-port> <username> <password> <timeout>\n"""
        connectSwitch('10.99.99.225', '830', 'admin', 'root', 60)

    if opr == "getExistingPortList":
        getExistingPortList()

    if opr == "crossconnects_get":
        """Usage: <outputXml file>"""
        crossconnects_get('crossConnects.xml')

    if opr == "pairs_get":
        """Usage: <outputXml file>"""
        pairs_get('pairs.xml')

    if opr == "ingress_get":
        """Usage: <outputXml file>"""
        ingress_get('ingress.xml')

    if opr == "ingressports_get":
        """Usage: <outputXml file> <port list : only ',' & '-' seperated values>"""
        ingressports_get('get_ingressPrt.xml', '10')
        ingressports_get('get_ingressPrt.xml', '10-14')
        ingressports_get('get_ingressPrt.xml', '14-10')
        ingressports_get('get_ingressPrt.xml', '10,11,16')

    if opr == "egress_get":
        """Usage: <outputXml file>"""
        egress_get('egress.xml')

    if opr == "egressports_get":
        """Usage: <outputXml file> <port list : only ',' & '-' seperated values>"""
        egressports_get('get_egressPrt.xml', '24-17')
        egressports_get('get_egressPrt.xml', '17')
        egressports_get('get_egressPrt.xml', '24,15,17')
        egressports_get('get_egressPrt.xml', '17-24')
        

    if opr == "editconfig_get":
        """Usage: <outputXml file>"""
        editconfig_get('get_edit_config.xml')

        
    if opr == "crossconnects_getConfig":
        """Usage: <outputXml file>"""
        crossconnects_getConfig('getConfig_crossConnects.xml')

    if opr == "pairs_getConfig":
        """Usage: <outputXml file>"""
        pairs_getConfig('getConfig_pairs.xml')

    if opr == "ingress_getConfig":
        """Usage: <outputXml file>"""
        ingress_getConfig('getConfig_ingress.xml')

    if opr == "ingressports_getConfig":
        """Usage: <outputXml file> <port list : only ',' & '-' seperated values>"""
        ingressports_getConfig('getConfig_ingressPrt.xml', '10-14')
        ingressports_getConfig('getConfig_ingressPrt.xml', '10,14')
        ingressports_getConfig('getConfig_ingressPrt.xml', '10')
        ingressports_getConfig('getConfig_ingressPrt.xml', '16-1')
        ingressports_getConfig('getConfig_ingressPrt.xml', '16,1,15')


    if opr == "egress_getConfig":
        """Usage: <outputXml file>"""
        egress_getConfig('getConfig_egress.xml')

    if opr == "egressports_getConfig":
        """Usage: <outputXml file> <port list : only ',' & '-' seperated values>"""
        egressports_getConfig('getConfig_egressPrt.xml', '17-21')
        egressports_getConfig('getConfig_egressPrt.xml', '24-18')
        egressports_getConfig('getConfig_egressPrt.xml', '17,21,24')
        egressports_getConfig('getConfig_egressPrt.xml', '17')

    if opr == "editconfig_getConfig":
        """Usage: <outputXml file>"""
        editconfig_getConfig('getConfig_edit_config.xml')

    if opr == "createOxcWO_Opr_editConfig":
        """<ingress port list : only ',' & '-' seperated values> <egress port list : only ',' & '-' seperated values>"""
        createOxcWO_Opr_editConfig('1-48', '49-96')

    if opr == "createOXC_editConfig":
        """<ingress port list : only ',' & '-' seperated values> <egress port list : only ',' & '-' seperated values>"""
        createOXC_editConfig('1,2,3', '17,18,19')

    if opr == "deleteOXC_editConfig":
        """<ingress port list : only ',' & '-' seperated values> <egress port list : only ',' & '-' seperated values>"""
        deleteOXC_editConfig('1-48', '49-98')

    if opr == "replaceOXC_editConfig":
        """<ingress port list : only ',' & '-' seperated values> <egress port list : only ',' & '-' seperated values>"""
        replaceOXC_editConfig('11', '23')


### main 


if __name__ == '__main__':
    oxC('connectSwitch')
    oxC('getExistingPortList')
   
    #oxC('crossconnects_get')
    #oxC('pairs_get')
    #oxC('ingress_get')
    #oxC('ingressports_get')
    #oxC('egress_get')
    #oxC('egressports_get')
       
 
    #oxC('crossconnects_getConfig')
    #oxC('pairs_getConfig')
    #oxC('ingress_getConfig')
    #oxC('ingressports_getConfig')
    #oxC('egress_getConfig')
    #oxC('egressports_getConfig')
    
    #oxC('replaceOXC_editConfig')
    #oxC('deleteOXC_editConfig')
    oxC('createOxcWO_Opr_editConfig')
    #oxC('createOXC_editConfig')
