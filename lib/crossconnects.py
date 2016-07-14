import re
import os
import csv
import time
import sys
import logging
import ConfigParser
import xml.dom.minidom
from createCsv import csvOutput


from xml.dom import minidom
from ncclient import manager
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom.minidom import parse, parseString

global ingPorts 
global egrPorts 

global ingPLst
global egrPLst

global swMgr

global xmlstr
global cnt

global xmlIngPLst
global xmlEgrPLst


ingPorts = []
egrPorts = []

ingPLst = []
egrPLst = []

xmlIngPLst = []
xmlEgrPLst = []

xmlstr = ''

cnt = 1



logger = logging.getLogger('Polatis')
logger.setLevel(logging.INFO)


### remove demo.log ###
#try:
#   os.remove("demo.log")
#except:
#   pass

f = logging.FileHandler('demo.log')
f.setLevel(logging.INFO)


c = logging.StreamHandler()
c.setLevel(logging.INFO     )

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f.setFormatter(formatter)
c.setFormatter(formatter)


logger.addHandler(f)
logger.addHandler(c)


### Connecting Switch ###

def connectSwitch(host, port, userName, password, timeout):
    ### Connecting to  switch ###
    global swMgr

    logger.info("Connecting to  switch <IP:Port = %s:%s>\n" % (host,port))
    swMgr = manager.connect_ssh(host=host, port=port, username=userName, password=password,timeout=timeout,hostkey_verify=False)


### Ouput Xml file ###

def writeToFile(fileName, data):

		f = open(fileName,'w')
		f.write(data)
		f.close()

"""
### Final result in csv format ###

def csvOutput(sNo, testCase, time, result):
    global cnt
    s = 'ms'
    o = 'OXC:\t'
    testCase = o+str(testCase)
    t = str(time)+s
    with open('finalLog.csv', 'a') as f:
        a = csv.writer(f, delimiter = ',')
        data = (sNo, testCase, t, result )
        a.writerow(data)
"""


def prettify(elem):
    #rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(elem)
    return reparsed.toprettyxml(indent=" ")


### getting switch ingress and egress Port list ###

def getExistingPortList():
    global ingPorts
    global egrPorts

    config = ConfigParser.ConfigParser()
    config.read('config.txt')

    ingressPrtRange = (config.get("crossconnect", "ingressPortRange")).split('-')
    egressPrtRange = (config.get("crossconnect", "egressPortRange")).split('-')


    for i in range(int(ingressPrtRange[0]), int(ingressPrtRange[1])+1):
        ingPorts.append(i)


    for j in range(int(egressPrtRange[0]), int(egressPrtRange[1])+1):
        egrPorts.append(j)


### get - cross-connects ###


def crossconnects_get(fileName):
	
    crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",

                                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})

    xmlstr = tostring(crossconnects)
    get('get - Query crossconnets', xmlstr, fileName)


### get - pairs ###

def pairs_get(fileName):

    crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    pairs = SubElement(crossconnects, 'opsw:pairs')

    xmlstr = tostring(crossconnects)
    getConfig('get - Query pairs', xmlstr, fileName)


### get - ingress port list ###
    
def ingress_get(fileName):

    crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                    'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    pairs = SubElement(crossconnects, 'opsw:pairs')
    ingress = SubElement(pairs, 'opsw:ingress')

    xmlstr = tostring(crossconnects)
    get('get - Query ingress', xmlstr, fileName)


### get - required ingress port list ###

def ingressports_get(fileName, portList):
    global ingPorts
    global ingPLst
    
    crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                    'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    ingSymbol = re.split(r'[\d]', portList)
    #logger.info('ingSymbol is : %s' % ingSymbol)

    
    if str(ingSymbol[1]) == ',' or str(ingSymbol[0] == ''):
        #logger.info('inside this , -------------------')
        ingPLst = portList.split(',')
        logger.info('ingress port list: %s' % ingPLst)
   
    if len(ingSymbol) >= 3: 
        if str(ingSymbol[1]) == '-' or str(ingSymbol[2]) == '-':
            ingPLst = []
            ingPLst1 = portList.split('-')

            if int(ingPLst1[0]) > int(ingPLst1[1]):
                ingPLst1.reverse()
                for i in range(int(ingPLst1[0]), int(ingPLst1[1])+1):
                    ingPLst.append(i)
                logger.info('ingress port list: %s' % ingPLst)
            elif int(ingPLst1[0]) < int(ingPLst1[1]):
                for i in range(int(ingPLst1[0]), int(ingPLst1[1])+1):
                    ingPLst.append(i)
                logger.info('ingress port list: %s' % ingPLst)
            else:
                pass

    else:
        #logger.error('Give for example comma or hypen seperated values ...\n\n')
        pass
        
    l = len(ingPLst)
    for i in range(0, l):
        a = ingPLst[i]
        if a in ingPorts:
           pairs = SubElement(crossconnects, 'opsw:pairs')
           ingress = SubElement(pairs, 'opsw:ingress')
           ingress.text = str(a)
        else:
           pairs = SubElement(crossconnects, 'opsw:pairs')
           ingress = SubElement(pairs, 'opsw:ingress')
           ingress.text = str(a)
           
    xmlstr = tostring(crossconnects)
    get('get - Query given ingress ports', xmlstr, fileName)

### get - egress port list ###
    
def egress_get(fileName):   
    
    crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                    'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    pairs = SubElement(crossconnects, 'opsw:pairs')
    egress = SubElement(pairs, 'opsw:egress')
    
    xmlstr = tostring(crossconnects)
    get('get - Query egress ports', xmlstr, fileName)

### get - required egress port list ### 

def egressports_get(fileName, portList):
    global egrPorts 
    global egrPLst
    
    crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})

    egrSymbol = re.split(r'[\d]', portList)
    #logger.info('egrSymbol : %s' % egrSymbol)
    
    if str(egrSymbol[1]) == ',' or str(egrSymbol[1]) == '':
        #logger.info("inside , ---------------------------------")
        egrPLst = portList.split(',')
        logger.info('egress port list: %s' % egrPLst)
    
    if str(egrSymbol[2]) == '-' or str(egrSymbol[1]) == '-':
        #logger.info("inside - --------------------------")
        egrPLst = []
        egrPLst1 = portList.split('-')
        logger.info('egress port list: %s' % egrPLst)
  
        if int(egrPLst1[0]) > int(egrPLst1[1]):
            egrPLst1.reverse()
            for i in range(int(egrPLst1[0]), int(egrPLst1[1])+1):
                egrPLst.append(i)
            logger.info('egress port list: %s' % egrPLst)
        elif int(egrPLst1[0]) < int(egrPLst1[1]):
            for i in range(int(egrPLst1[0]), int(egrPLst1[1])+1):
                egrPLst.append(i)
            logger.info('egress port list: %s' % egrPLst)
        else:
             pass

    else:
        pass
        #logger.error('Give for example comma or hypen seperated values ...\n\n')
        
    l = len(egrPLst)
    for i in range(0, l):
        a = egrPLst[i]
        if a in egrPorts:
           pairs = SubElement(crossconnects, 'opsw:pairs')
           egress = SubElement(pairs, 'opsw:egress')
           egress.text = str(a)
        else:
           pairs = SubElement(crossconnects, 'opsw:pairs')
           egress = SubElement(pairs, 'opsw:egress')
           egress.text = str(a)

    xmlstr = tostring(crossconnects)
    get('get - Query given egress ports', xmlstr, fileName)


### get - querying configuration from "edit-config" ###
    
def editconfig_get(fileName):
    global ingPorts
    global ingPLst
    global egrPorts 
    global egrPLst
    
    crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    try:
        l = len(egrPLst)
        for i in range(0, l):
            a = ingPLst[i]
            b = egrPLst[i]
            if a in ingPorts and b in egrPorts:
               pairs = SubElement(crossconnects, 'opsw:pairs')
               ingress = SubElement(pairs, 'opsw:ingress')
               ingress.text = str(a)
               egress = SubElement(pairs, 'opsw:egress')
               egress.text = str(b)
            else:
               pairs = SubElement(crossconnects, 'opsw:pairs')
               ingress = SubElement(pairs, 'opsw:ingress')
               ingress.text = str(a)
               egress = SubElement(pairs, 'opsw:egress')
               egress.text = str(b)
    except Exception as err:
        logger.error('\t\t-----[ Error from the Switch ]-----\n\n%s\n\n', err)


    xmlstr = tostring(crossconnects)
    get('get - Query ports list connected by using edit-config', xmlstr, fileName)


### get - configuration for required operation ###
def get(tcName, xmlstr, fileName):
    global swMgr
    global cnt


    c = len(tcName)+7
    l = len(str(cnt))
    if l == 2:
        c = c + 1
        p = '       +' + (c * '-') + '+       '
        q = '| ' +str(cnt) +' -  '+ str(tcName) + ' |'
    else:
        p = '       +' + (c * '-') + '+       '
        q = '| ' +str(cnt) +' -  '+ str(tcName) + ' |'

    try:
        logger.info('\n\n%s\n       %s\n%s\n\n' % (p, q, p))
        logger.info('created xmlstr : \n%s\n\n' % xmlstr)
        

        s = time.time()
        xmlData = swMgr.get(filter=('subtree',xmlstr)).data_xml
        print '\n\n'
        prettyXml = prettify(xmlData)
        logger.info('response from the switch : \n%s\n\n' % prettyXml)


        e = time.time()
        t = int(round((e - s)* 1000))
        writeToFile(fileName,prettyXml);
        csvOutput('crossconnects', tcName, t, 'PASS')
		
    except Exception as err:
        print '\n\n'
        logger.error('\t\t-----[ Error from the Switch ]-----\n\n%s\n\n', err)
        csvOutput('crossconnects', tcName, 0, 'FAIL')

    cnt = cnt+1

        
   
### get-config - cross-connects ###


def crossconnects_getConfig(fileName):
	
    crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",

                                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})

    xmlstr = tostring(crossconnects)
    getConfig('getConfig - Query crossconnets', xmlstr, fileName)

### get-config - pairs ###

def pairs_getConfig(fileName):

    crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    pairs = SubElement(crossconnects, 'opsw:pairs')

    xmlstr = tostring(crossconnects)
    getConfig('getConfig - Query pairs', xmlstr, fileName)

### get-config - ingress ports ###

def ingress_getConfig(fileName):

    crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                    'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    pairs = SubElement(crossconnects, 'opsw:pairs')
    ingress = SubElement(pairs, 'opsw:ingress')

    xmlstr = tostring(crossconnects)
    getConfig('getConfig - Query ingress', xmlstr, fileName)

### get-config - required ingress port list ###

def ingressports_getConfig(fileName, portList):
    global ingPorts
    global ingPLst
    
    crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                    'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    ingSymbol = re.split(r'[\d]', portList)
    #logger.info('ingSymbol is : %s' % ingSymbol)

    if str(ingSymbol[1]) == ',' or str(ingSymbol[1]) == '':
        #logger.info("inside , ---------------------")
        ingPLst = portList.split(',')
        logger.info('ingress port list: %s' % ingPLst)
    
    if str(ingSymbol[2]) == '-' or str(ingSymbol[1]) == '-':
        #logger.info("inside - -----------------------")
        ingPLst = []
        ingPLst1 = portList.split('-')

        if int(ingPLst1[0]) > int(ingPLst1[1]):
            ingPLst1.reverse()
            for i in range(int(ingPLst1[0]), int(ingPLst1[1])+1):
                ingPLst.append(i)
            logger.info('ingress port list: %s' % ingPLst)
        elif int(ingPLst1[0]) < int(ingPLst1[1]):
            for i in range(int(ingPLst1[0]), int(ingPLst1[1])+1):
                ingPLst.append(i)
            logger.info('ingress port list: %s' % ingPLst)
        else:
             pass


    else:
        pass
        #logger.error('Give for example comma or hypen seperated values ...\n\n')
        
    l = len(ingPLst)
    for i in range(0, l):
        a = ingPLst[i]
        if a in ingPorts:
           pairs = SubElement(crossconnects, 'opsw:pairs')
           ingress = SubElement(pairs, 'opsw:ingress')
           ingress.text = str(a)
        else:
           pairs = SubElement(crossconnects, 'opsw:pairs')
           ingress = SubElement(pairs, 'opsw:ingress')
           ingress.text = str(a)
           
    xmlstr = tostring(crossconnects)
    getConfig('getConfig - Query given ingress ports', xmlstr, fileName)

### get-config - egress ports ###

def egress_getConfig(fileName):   
    
    crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                    'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    pairs = SubElement(crossconnects, 'opsw:pairs')
    egress = SubElement(pairs, 'opsw:egress')
    xmlstr = tostring(crossconnects)
    getConfig('getConfig - Query egress ports', xmlstr, fileName)

### get-config - required egress port list ###

def egressports_getConfig(fileName, portList):
    global egrPorts 
    global egrPLst
    
    crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                    'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})

    egrSymbol = re.split(r'[\d]', portList)
    #logger.info('egrSymbol symbol is : %s' % egrSymbol)
    
    if str(egrSymbol[1]) == ',' or str(egrSymbol[1]) == '':
        #logger.info("Inside this , ---------------------------------")
        egrPLst = portList.split(',')
        logger.info('egrress port list: %s' % egrPLst)
    
    if str(egrSymbol[2]) == '-' or str(egrSymbol[1]) == '-':
        #logger.info("Inside this - ---------------------------------")
        egrPLst = []
        egrPLst1 = portList.split('-')
        #logger.info('egrress port list: %s' % egrPLst)
        #logger.info('egrPLst1[0] list: %s' % egrPLst1[0])
 
        if int(egrPLst1[0]) > int(egrPLst1[1]):
            egrPLst1.reverse()
            for i in range(int(egrPLst1[0]), int(egrPLst1[1])+1):
                egrPLst.append(i)
            logger.info('egress port list: %s' % egrPLst)
       
        if int(egrPLst1[0]) < int(egrPLst1[1]):
            egrPLst = []
            for i in range(int(egrPLst1[0]), int(egrPLst1[1])+1):
                egrPLst.append(i)
            logger.info('egress port list: %s' % egrPLst)
        else:
             pass

    else:
        pass
        #logger.error('Give for example comma or hypen seperated values ...\n\n')
        
    l = len(egrPLst)
    for i in range(0, l):
        a = egrPLst[i]
        if a in egrPorts:
           pairs = SubElement(crossconnects, 'opsw:pairs')
           egress = SubElement(pairs, 'opsw:egress')
           egress.text = str(a)
        else:
           pairs = SubElement(crossconnects, 'opsw:pairs')
           egress = SubElement(pairs, 'opsw:egress')
           egress.text = str(a)

    xmlstr = tostring(crossconnects)
    getConfig('getConfig - Query given egress ports', xmlstr, fileName)


### get-config - from edit-config configuration ###
    
def editconfig_getConfig(fileName):
    global ingPorts
    global ingPLst
    global egrPorts 
    global egrPLst
       
    crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                    'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    try:
        l = len(egrPLst)
        for i in range(0, l):
            a = ingPLst[i]
            b = egrPLst[i]
            if a in ingPorts and b in egrPorts:
               pairs = SubElement(crossconnects, 'opsw:pairs')
               ingress = SubElement(pairs, 'opsw:ingress')
               ingress.text = str(a)
               egress = SubElement(pairs, 'opsw:egress')
               egress.text = str(b)
            else:
               pairs = SubElement(crossconnects, 'opsw:pairs')
               ingress = SubElement(pairs, 'opsw:ingress')
               ingress.text = str(a)
               egress = SubElement(pairs, 'opsw:egress')
               egress.text = str(b)
    except Exception as err:
        logger.error('\t\t-----[ Error from the Switch ]-----\n\n%s\n\n', err)

    xmlstr = tostring(crossconnects)
    getConfig('getConfig - Query ports list connected by using edit-config', xmlstr, fileName)
    
### get-config - for required switch operation ###

def getConfig(tcName, xmlstr, fileName):
    global swMgr
    global cnt

    c = len(tcName)+7
    l = len(str(cnt))
    if l == 2:
        c = c + 1
        p = '       +' + (c * '-') + '+       '
        q = '| ' +str(cnt) +' -  '+ str(tcName) + ' |'
    else:
        p = '       +' + (c * '-') + '+       '
        q = '| ' +str(cnt) +' -  '+ str(tcName) + ' |'

    try:
        logger.info('\n\n%s\n       %s\n%s\n\n' % (p, q, p))
        logger.info('created xmlstr : \n%s\n\n' % xmlstr)
        logger.info('Get Config - Response from the switch...\n\n')

        s = time.time()
        xmlData = swMgr.get_config(source='running',  filter=('subtree',xmlstr)).data_xml
        print '\n\n'


        prettyXml = prettify(xmlData)
        logger.info('response from the switch :\n%s\n\n' % prettyXml)

        e = time.time()
        t = int(round((e - s)* 1000))
        writeToFile(fileName, prettyXml);
        csvOutput('crossconnects', tcName, t, 'PASS')

		
    except Exception as err:
        print '\n\n'
        logger.error('\t\t-----[ Error from the Switch ]-----\n\n%s\n\n', err)
        csvOutput('crossconnects', tcName, 0, 'FAIL')
    
    cnt = cnt+1


### create XML for edit-config ###

def createXml(operation):

    global ingPorts
    global egrPorts
    global ingPLst
    global egrPLst
    global xmlstr
    
    l = len(ingPLst)
    config = Element('config', {'xmlns:xc':"urn:ietf:params:xml:ns:netconf:base:1.0"})
    crossconnect = SubElement(config, 'cross-connects', {'xmlns':"http://www.polatis.com/yang/optical-switch"})


    for i in range(0, l):
        a = ingPLst[i]
        b = egrPLst[i]
        if a in ingPorts and b in egrPorts:
            pairs = SubElement(crossconnect, 'pairs', {'ns:operation':operation})
            ingress = SubElement(pairs, 'ingress')
            ingress.text = str(a)
            egress = SubElement(pairs, 'egress')
            egress.text = str(b)
        else:
            pairs = SubElement(crossconnect, 'pairs', {'ns:operation':operation})
            ingress = SubElement(pairs, 'ingress')
            ingress.text = str(a)
            egress = SubElement(pairs, 'egress')
            egress.text = str(b)
    
    xmlstr = tostring(config)

def SplitPortList(ingressPorts, egressPorts):
    global ingPLst
    global egrPLst
    global ingPorts
    global egrPorts

    ingSymbol = re.split(r'[\d]', ingressPorts)
    #logger.info("ing symbol is : %s" % ingSymbol)

    ### if-else loop is used to check the connecting operation(random/direct) ###
    if str(ingSymbol[0]) == ',' or str(ingSymbol[0]) == '':
        logger.info("inside , -----------------------------")
        ingPLst = ingressPorts.split(',')
        egrPLst = egressPorts.split(',')
    
    if str(ingSymbol[2]) == '-' or str(ingSymbol[1]) == '-':
        logger.info("inside - ---------------------------------")
        ingPLst = []
        egrPLst = []


        list1 = ingressPorts.split('-')
        list2 = egressPorts.split('-')
        

        if int(list1[0]) > int(list1[1]) and int(list2[0]) > int(list2[1]):
            list1.reverse()
            list2.reverse()
            for i,j in zip(range(int(list1[0]), int(list1[1])+1), range(int(list2[0]), int(list2[1])+1)):
                ingPLst.append(i)
                egrPLst.append(j)
            ingPLst.reverse()
            egrPLst.reverse()
        elif int(list1[0]) > int(list1[1]) and int(list2[0]) < int(list2[1]):
            list1.reverse()
            for i,j in zip(range(int(list1[0]), int(list1[1])+1), range(int(list2[0]), int(list2[1])+1)):
                ingPLst.append(i)
                egrPLst.append(j)
            ingPLst.reverse()
        elif int(list2[0]) > int(list2[1]) and int(list1[0]) < int(list1[1]):
            list2.reverse()
            for i,j in zip(range(int(list1[0]), int(list1[1])+1), range(int(list2[0]), int(list2[1])+1)):
                ingPLst.append(i)
                egrPLst.append(j)
            egrPLst.reverse()
        else:
            for i,j in zip(range(int(list1[0]), int(list1[1])+1), range(int(list2[0]), int(list2[1])+1)):
                ingPLst.append(i)
                egrPLst.append(j)

    else:
         pass
    #    logger.error('Give for example comma or hypen seperated values ...\n\n')



def createOxcWO_Opr_editConfig(ingressPorts, egressPorts):
    global ingPLst
    global egrPLst
    global ingPorts
    global egrPorts
    global xmlstr
    
    SplitPortList(ingressPorts, egressPorts)
    
    l = len(ingPLst)
    config = Element('config', {'xmlns:xc':"urn:ietf:params:xml:ns:netconf:base:1.0"})
    crossconnect = SubElement(config, 'cross-connects', {'xmlns':"http://www.polatis.com/yang/optical-switch"})

    for i in range(0, l):
        a = ingPLst[i]
        b = egrPLst[i]
        if a in ingPorts and b in egrPorts:
            pairs = SubElement(crossconnect, 'pairs')
            ingress = SubElement(pairs, 'ingress')
            ingress.text = str(a)
            egress = SubElement(pairs, 'egress')
            egress.text = str(b)
        else:
            pairs = SubElement(crossconnect, 'pairs')
            ingress = SubElement(pairs, 'ingress')
            ingress.text = str(a)
            egress = SubElement(pairs, 'egress')
            egress.text = str(b)
    
    xmlstr = tostring(config)
    editConfig('editConfig - create OXC without opr')


### create OXC for given ports ###
    
def createOXC_editConfig(ingressPorts, egressPorts):
    global xmlstr
    
    SplitPortList(ingressPorts, egressPorts)
    createXml('create')
    editConfig('editConfig - create OXC')

### delete OXC for given ports ###
def deleteOXC_editConfig(ingressPorts, egressPorts):
    global xmlstr
    
    SplitPortList(ingressPorts, egressPorts)
    createXml('delete')
    editConfig('editConfig - delete OXC')

### replace OXC for given ports ###
def replaceOXC_editConfig(ingressPorts, egressPorts):
    global xmlstr
    
    SplitPortList(ingressPorts, egressPorts)
    createXml('replace')
    editConfig('editConfig - replace OXC')

### remove OXC for given ports ###
def removeOXC_editConfig(ingressPorts, egressPorts):
    global xmlstr
    
    SplitPortList(ingressPorts, egressPorts)
    createXml('remove')
    editConfig('editConfig - remove OXC')
    
### merge OXC for given ports ###
def mergeOXC_editConfig(ingressPorts, egressPorts):
    global xmlstr
    
    SplitPortList(ingressPorts, egressPorts)
    createXml('merge')
    editConfig('editConfig - merge OXC')



def cmpIngEgrPortLst(xmlData):
    global xmlstr
    global xmlIngPLst
    global xmlEgrPLst

    global ingPLst
    global egrPLst
 
    xmlIngPLst = []
    xmlEgrPLst = []

    p = 'PASS'
    f = 'FAIL'

    DOMTree = xml.dom.minidom.parseString(xmlData)
    collection = DOMTree.documentElement

    pairs = collection.getElementsByTagName("pairs")

    for port in pairs:

        ingress = port.getElementsByTagName('ingress')[0]
        ingPrt =  str(ingress.childNodes[0].data)

        xmlIngPLst.append(ingPrt)

        egress = port.getElementsByTagName('egress')[0]
        egrPrt =  str(egress.childNodes[0].data)

        xmlEgrPLst.append(egrPrt)

    logger.info('Ports list from getConfig\n\n')
    logger.info('Ingress port list: %s' % xmlIngPLst)
    logger.info('Egress port list: %s\n\n' % xmlEgrPLst)

    
    if cmp(ingPLst, xmlIngPLst) == cmp(egrPLst, xmlEgrPLst):
        logger.info('compare the ports from switch edit config and get config ----> PASS\n')
        return p

    else:
        logger.error('compare the ports from switch edit config and get config ----> FAIL\n')
        return f

    
    



### edit-config - for modify the OXC connection ###   

def editConfig(tcName):
    global swMgr
    global xmlstr
    global cnt
    global ingPorts
    global ingPLst
    global egrPorts 
    global egrPLst
    s = time.time()
    
    global cnt
    c = len(tcName)+7
    l = len(str(cnt))
    if l == 2:
        c = c + 1
        p = '       +' + (c * '-') + '+       '
        q = '| ' +str(cnt) +' -  '+ str(tcName) + ' |'
    else:
        p = '       +' + (c * '-') + '+       '
        q = '| ' +str(cnt) +' -  '+ str(tcName) + ' |'
 

    try:
       logger.info('\n\n%s\n       %s\n%s\n\n' % (p, q, p))

       logger.info('Existing ingress port list: %s' % ingPorts)
       logger.info('Existing egress port list : %s\n\n' %  egrPorts)

       logger.info('ingress port list: %s' % ingPLst)
       logger.info('egress port list : %s\n\n' % egrPLst)
       
       logger.info("pass xml to the switch : \n\n%s\n" % xmlstr)


       xmldata = swMgr.edit_config(target='running', config=xmlstr)
       print "\n\n"

    
       logger.info('Edit config - Response from the switch\n\n%s\n\n' % xmldata)

       crossconnects = Element('opsw:cross-connects', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                        'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
       try:
          l = len(egrPLst)
          for i in range(0, l):
              a = ingPLst[i]
              b = egrPLst[i]
              if a in ingPorts and b in egrPorts:
                 pairs = SubElement(crossconnects, 'opsw:pairs')
                 ingress = SubElement(pairs, 'opsw:ingress')
                 ingress.text = str(a)
                 egress = SubElement(pairs, 'opsw:egress')
                 egress.text = str(b)
              else:
                 pairs = SubElement(crossconnects, 'opsw:pairs')
                 ingress = SubElement(pairs, 'opsw:ingress')
                 ingress.text = str(a)
                 egress = SubElement(pairs, 'opsw:egress')
                 egress.text = str(b)
       except Exception as err:
          logger.error('\t\t-----[ Error from the Switch ]-----\n\n%s\n\n' % err)


       logger.info('-----[ Compare the Edit Config and Get Config Ports ]-----\n\n')
       xmlstr = tostring(crossconnects)
       xmlData = swMgr.get_config(source='running',  filter=('subtree',xmlstr)).data_xml
       print "\n\n"
     
       prettyXml = prettify(xmlData)
       logger.info('Get  config -  Response from the switch\n\n%s \n\n' % prettyXml)
       
       result = cmpIngEgrPortLst(xmlData)

       e = time.time()
       t = int(round((e - s)* 1000))
       csvOutput('oxC', tcName, t, result)

    except Exception as err:
       print "\n\n"
       logger.error('\t\t-----[ Error from the Switch ]-----\n\n%s\n\n' %  err)
       e = time.time()
       t = int(round((e - s)* 1000))

       csvOutput('oxC', tcName, t, 'FAIL')

    cnt = cnt+1
