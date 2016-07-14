import sys
import time
import re
import ConfigParser
import logging
import xml.dom.minidom
from createCsv import csvOutput

from ncclient import manager
from xml.etree.ElementTree import Element, SubElement, tostring

from xml.dom import minidom
from xml.dom.minidom import parse, parseString


global swMgr
global cnt
global xmlStr
global PrtLblNames
global prtIdLst

xmlStr = ''

PrtLblNames = []
prtIdLst = []

cnt = 1
xmlStr = ''

logger = logging.getLogger('Polatis')
logger.setLevel(logging.INFO)

f = logging.FileHandler('demo.log')
f.setLevel(logging.INFO)

c = logging.StreamHandler()
c.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f.setFormatter(formatter)
c.setFormatter(formatter)

logger.addHandler(f)
logger.addHandler(c)


def createBox(tcName):
    ### create box for test case name ###

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
    cnt = cnt + 1
    logger.info('\n\n%s\n       %s\n%s\n\n' % (p, q, p))

def connectSwitch(host, port, userName, password, timeout):
    ### connecting to the switch ###
    global swMgr

    logger.info('connecting ot switch <IP:port = %s:%s>\n' % (host, port))
    swMgr = manager.connect_ssh(host=host, port=port, username=userName, password=password, timeout=timeout, hostkey_verify=False)


def writeToFile(fileName, data):
    ### writing switch output in XML file ###

    f = open(fileName, 'w')
    f.write(data)
    f.close()

def prettify(elem):
    ### print the pretty xml ###

    reparsed =  minidom.parseString(elem)
    return reparsed.toprettyxml(indent=" ")


def get_ports(fileName):
    ### create XML for ports, pass it and get xml output file from switch ###
    
    createBox('get - Query ports')
    ports = Element("opsw:ports", {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                   'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})

    xmlStr = tostring(ports)
    get('get - Query ports', xmlStr, fileName)

def get_port_label(fileName):
    ### create XML for port label, pass it and get xml output file from switch ###
    
    createBox('get - Query port_label')
    ports = Element("opsw:ports", {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                   'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    port = SubElement(ports, 'opsw:port')
    port_label = SubElement(port, 'opsw:port-label')
    xmlStr = tostring(ports)
    get('get - Query port_label', xmlStr, fileName)


def get_port_state(fileName):
    ### create XML for port label, pass it and get output file from switch ###
 
    createBox('get - Query port_state')
    ports = Element("opsw:ports", {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                   'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    port = SubElement(ports, 'opsw:port')
    port_state = SubElement(port, 'opsw:port-state')
    xmlStr = tostring(ports)
    get('get - Query port_state', xmlStr, fileName)

def get_port_status(fileName):
    ### create XML for port_status, pass it to and get xml output file from switch ###

    createBox('get - Query port status')
    ports = Element("opsw:ports", {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                   'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    port = SubElement(ports, 'opsw:port')
    port_status = SubElement(port, 'opsw:port-status')
    xmlStr = tostring(ports)
    get('get - Query port status', xmlStr, fileName)

def get_opm(fileName):
    ### create XML for opm, pass it to and get xml output file from switch ###

    createBox('get - Query opm')
    ports = Element("opsw:ports", {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                   'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    port = SubElement(ports, 'opsw:port')
    opm = SubElement(port, 'opsw:opm')
    xmlStr = tostring(ports)
    get('get - Query opm', xmlStr, fileName)


def get_selectedPortsInfo(name, tagname, ids, outFileName):
    ### create xml from given info and pass it and get output xml file from switch ###
    createBox('get - selectedPortInfo')
    #ports = Element("opsw:ports", {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
    #                               'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    
    name = name.split(',')
    tagname = tagname.split(',')
    l = len(name)
    logger.info('<ports information> sub tags name are  : %s\n\n' % tagname)

    if 'port_id' in name:
        ports = Element("opsw:ports", {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                       'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
        for i,j in zip(range(0, l), range(0, l)):
            a = 'opsw:'+str(tagname[j])

            if name[i] == 'port_id':
                if ids == 'allInfo':
                    name[i] = SubElement(ports, str(a))
                else:
                    idTaglist = ids.split('/')
                    logger.info('<port> port-ids : %s\n\n' % idTaglist[0])
                    logger.info('<opm> sub tags : %s\n\n' % idTaglist[1])

                    idSymbol = re.split(r'[\d]', idTaglist[0])
                    print "idSymbol : ", idSymbol
                    ln = len(idTaglist[0])
                    if ln <= 2:
                        print "Pass"
                        ids = idTaglist[0]
                        ln = len(ids)
                        port = SubElement(ports, 'opsw:port')
                        port_id = SubElement(port, 'opsw:port-id')
                        port_id.text = str(idTaglist[0])
                        for i,j in zip(range(0, l), range(0, l)):
                                if name[i] == 'port_id':
                                    pass
                                elif name[i] == 'opm':
                                    if idTaglist[1] == 'none':
                                        pass
                                    else:
                                        taglist = idTaglist[1].split(',')

                                        l1 = len(taglist)
                                        varNames = ['opm1','opm2','opm3', 'opm4','opm5', 'opm6', 'opm7','opm8','opm9', 'opm10', 'opm11', 'opm12']

                                        opm = SubElement(port, 'opsw:opm')
                                        for i in range(0, l1):
                                            a = 'opsw:'+str(taglist[i])
                                            varNames[i] = SubElement(opm, str(a))

                                else:
                                    a = 'opsw:'+str(tagname[j])
                                    name[i] = SubElement(port, str(a))

                    elif str(idSymbol[0]) == ',' or str(idSymbol[1]) == ',':
                        print "second elif ................"
                        ids = idTaglist[0].split(',')
                        ln = len(ids)
                        for b in range(0, ln):
                            a = ids[b]
                            port = SubElement(ports, 'opsw:port')
                            port_id = SubElement(port, 'opsw:port-id')
                            port_id.text = str(a)
                            for i,j in zip(range(0, l), range(0, l)):
                                if name[i] == 'port_id':
                                    pass
                                elif name[i] == 'opm':
                                    if idTaglist[1] == 'none':
                                        pass
                                    else:
                                        taglist = idTaglist[1].split(',')

                                        l1 = len(taglist)
                                        varNames = ['opm1','opm2','opm3', 'opm4','opm5', 'opm6', 'opm7','opm8','opm9', 'opm10', 'opm11', 'opm12']

                                        opm = SubElement(port, 'opsw:opm')
                                        for i in range(0, l1):
                                            a = 'opsw:'+str(taglist[i])
                                            varNames[i] = SubElement(opm, str(a))

                                else:
                                    a = 'opsw:'+str(tagname[j])
                                    name[i] = SubElement(port, str(a))
                
                    elif str(idSymbol[1]) == '-' or str(idSymbol[2]) == '-':
                        print "Third elif ................"
                        ids = idTaglist[0].split('-')
                        if ids[0] < ids[1]:
                            for b in range(int(ids[0]), int(ids[1])+1):
                                port = SubElement(ports, 'opsw:port')
                                port_id = SubElement(port, 'opsw:port-id')
                                port_id.text = str(b)
                                for i,j in zip(range(0, l), range(0, l)):
                                    if name[i] == 'port_id':
                                        pass
                                    elif name[i] == 'opm':
                                        if idTaglist[1] == 'none':
                                            pass
                                        else:
                                            taglist = idTaglist[1].split(',')

                                            l1 = len(taglist)
                                            varNames = ['opm1','opm2','opm3', 'opm4','opm5', 'opm6', 'opm7','opm8','opm9', 'opm10', 'opm11', 'opm12']

                                            opm = SubElement(port, 'opsw:opm')
                                            for i in range(0, l1):
                                                a = 'opsw:'+str(taglist[i])
                                                varNames[i] = SubElement(opm, str(a))

                                    else:
                                        a = 'opsw:'+str(tagname[j])
                                        name[i] = SubElement(port, str(a))
                        elif ids[0] > ids[1]:
                            for b in range(int(ids[1]), int(ids[0])+1):
                                port = SubElement(ports, 'opsw:port')
                                port_id = SubElement(port, 'opsw:port-id')
                                port_id.text = str(b)
                                for i,j in zip(range(0, l), range(0, l)):
                                    if name[i] == 'port_id':
                                        pass
                                    elif name[i] == 'opm':
                                        if idTaglist[1] == 'none':
                                            pass
                                        else:
                                            taglist = idTaglist[1].split(',')

                                            l1 = len(taglist)
                                            varNames = ['opm1','opm2','opm3', 'opm4','opm5', 'opm6', 'opm7','opm8','opm9', 'opm10', 'opm11', 'opm12']

                                            opm = SubElement(port, 'opsw:opm')
                                            for i in range(0, l1):
                                                a = 'opsw:'+str(taglist[i])
                                                varNames[i] = SubElement(opm, str(a))

                                    else:
                                        a = 'opsw:'+str(tagname[j])
                                        name[i] = SubElement(port, str(a))

            else:
                #logger.info("port-id should present in the <tagname> & <name>")
                pass
        xmlstr = tostring(ports)
        get('get - selectedProductInfo', xmlstr, outFileName)

    else:
        logger.error('port-id should present in <tagname> and <name> \n\n')


def get(tcName, xmlstr, fileName):
    ### get - configuration for required operation ###

    global swMgr
    global cnt

    try:
       logger.info('Quering for running configuration data from switch using get\n\n')
       logger.info('Get  - pass XML str to the switch...\n\n')
       prettyXml = prettify(xmlstr)
       logger.info('xml str is : \n\n%s\n\n' % prettyXml)

       s = time.time()
       xmlData = swMgr.get(filter=('subtree',xmlstr)).data_xml
       print '\n\n'
       prettyXml = prettify(xmlData)
       logger.info('Get - Output from the switch\n\n%s\n' % prettyXml)

       e = time.time()
       t = int(round((e - s)* 1000))
       #t = (e - s)* 1000
       writeToFile(fileName,prettyXml);
       csvOutput('Ports', tcName, t, 'PASS')

    except Exception as err:
       print '\n\n'
       logger.error('\t\t-----[ Error from the Switch ]-----\n\n%s\n\n', err)
       csvOutput('Ports', tcName, 0, 'FAIL')

def getConfig_ports(fileName):
    ### create XML for ports, pass it and get xml output file from switch ###
    
    createBox('getConfig - Query ports')
    ports = Element("opsw:ports", {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                   'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})

    xmlStr = tostring(ports)
    getConfig('getConfig - Query ports', xmlStr, fileName)

def getConfig_port_label(fileName):
    ### create XML for port label, pass it and get xml output file from switch ###
    
    createBox('getConfig - Query port_label')
    ports = Element("opsw:ports", {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                   'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    port = SubElement(ports, 'opsw:port')
    port_label = SubElement(port, 'opsw:port-label')
    xmlStr = tostring(ports)
    getConfig('getConfig - Query port_label', xmlStr, fileName)


def getConfig_port_state(fileName):
    ### create XML for port label, pass it and get output file from switch ###
 
    createBox('getConfig - Query port_state')
    ports = Element("opsw:ports", {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                   'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    port = SubElement(ports, 'opsw:port')
    port_state = SubElement(port, 'opsw:port-state')
    xmlStr = tostring(ports)
    getConfig('getConfig - Query port_state', xmlStr, fileName)


def getConfig_opm(fileName):
    ### create XML for opm, pass it to and get xml output file from switch ###

    createBox('getConfig - Query opm')
    ports = Element("opsw:ports", {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                   'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    port = SubElement(ports, 'opsw:port')
    opm = SubElement(port, 'opsw:opm')
    xmlStr = tostring(ports)
    getConfig('getConfig - Query opm', xmlStr, fileName)

def getConfig_selectedPortsInfo(name, tagname, ids, outFileName):
    ### create xml from given info and pass it and get output xml file from switch ###
    createBox('getConfig - selectedPortInfo')
    #ports = Element("opsw:ports", {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
    #                               'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    
    name = name.split(',')
    tagname = tagname.split(',')
    l = len(name)
    logger.info('<ports information> sub tags name are  : %s\n\n' % tagname)

    if 'port_id' in name:
        ports = Element("opsw:ports", {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                       'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
        for i,j in zip(range(0, l), range(0, l)):
            a = 'opsw:'+str(tagname[j])

            if name[i] == 'port_id':
                if ids == 'allInfo':
                    name[i] = SubElement(ports, str(a))
                else:
                    idTaglist = ids.split('/')
                    logger.info('<port> port-ids : %s\n\n' % idTaglist[0])
                    logger.info('<opm> sub tags : %s\n\n' % idTaglist[1])

                    idSymbol = re.split(r'[\d]', idTaglist[0])
                    ln = len(idTaglist[0])
                    if ln <= 2:
                        print "Pass"
                        ids = idTaglist[0]
                        ln = len(ids)
                        port = SubElement(ports, 'opsw:port')
                        port_id = SubElement(port, 'opsw:port-id')
                        port_id.text = str(idTaglist[0])
                        for i,j in zip(range(0, l), range(0, l)):
                                if name[i] == 'port_id':
                                    pass
                                elif name[i] == 'opm':
                                    if idTaglist[1] == 'none':
                                        pass
                                    else:
                                        taglist = idTaglist[1].split(',')

                                        l1 = len(taglist)
                                        varNames = ['opm1','opm2','opm3', 'opm4','opm5', 'opm6', 'opm7','opm8','opm9', 'opm10', 'opm11', 'opm12']

                                        opm = SubElement(port, 'opsw:opm')
                                        for i in range(0, l1):
                                            a = 'opsw:'+str(taglist[i])
                                            varNames[i] = SubElement(opm, str(a))

                                else:
                                    a = 'opsw:'+str(tagname[j])
                                    name[i] = SubElement(port, str(a))


                    elif str(idSymbol[0]) == ',' or str(idSymbol[1]) == ',':
                        ids = idTaglist[0].split(',')
                        ln = len(ids)
                        for b in range(0, ln):
                            a = ids[b]
                            port = SubElement(ports, 'opsw:port')
                            port_id = SubElement(port, 'opsw:port-id')
                            port_id.text = str(a)
                            for i,j in zip(range(0, l), range(0, l)):
                                if name[i] == 'port_id':
                                    pass
                                elif name[i] == 'opm':
                                    if idTaglist[1] == 'none':
                                        pass
                                    else:
                                        taglist = idTaglist[1].split(',')

                                        l1 = len(taglist)
                                        varNames = ['opm1','opm2','opm3', 'opm4','opm5', 'opm6', 'opm7','opm8','opm9', 'opm10', 'opm11', 'opm12']

                                        opm = SubElement(port, 'opsw:opm')
                                        for i in range(0, l1):
                                            a = 'opsw:'+str(taglist[i])
                                            varNames[i] = SubElement(opm, str(a))

                                else:
                                    a = 'opsw:'+str(tagname[j])
                                    name[i] = SubElement(port, str(a))
                
                    elif str(idSymbol[1]) == '-' or str(idSymbol[2]) == '-':
                        ids = idTaglist[0].split('-')
                        if ids[0] < ids[1]:
                            for b in range(int(ids[0]), int(ids[1])+1):
                                port = SubElement(ports, 'opsw:port')
                                port_id = SubElement(port, 'opsw:port-id')
                                port_id.text = str(b)
                                for i,j in zip(range(0, l), range(0, l)):
                                    if name[i] == 'port_id':
                                        pass
                                    elif name[i] == 'opm':
                                        if idTaglist[1] == 'none':
                                            pass
                                        else:
                                            taglist = idTaglist[1].split(',')

                                            l1 = len(taglist)
                                            varNames = ['opm1','opm2','opm3', 'opm4','opm5', 'opm6', 'opm7','opm8','opm9', 'opm10', 'opm11', 'opm12']

                                            opm = SubElement(port, 'opsw:opm')
                                            for i in range(0, l1):
                                                a = 'opsw:'+str(taglist[i])
                                                varNames[i] = SubElement(opm, str(a))

                                    else:
                                        a = 'opsw:'+str(tagname[j])
                                        name[i] = SubElement(port, str(a))
                        elif ids[0] > ids[1]:
                            for b in range(int(ids[1]), int(ids[0])+1):
                                port = SubElement(ports, 'opsw:port')
                                port_id = SubElement(port, 'opsw:port-id')
                                port_id.text = str(b)
                                for i,j in zip(range(0, l), range(0, l)):
                                    if name[i] == 'port_id':
                                        pass
                                    elif name[i] == 'opm':
                                        if idTaglist[1] == 'none':
                                            pass
                                        else:
                                            taglist = idTaglist[1].split(',')

                                            l1 = len(taglist)
                                            varNames = ['opm1','opm2','opm3', 'opm4','opm5', 'opm6', 'opm7','opm8','opm9', 'opm10', 'opm11', 'opm12']

                                            opm = SubElement(port, 'opsw:opm')
                                            for i in range(0, l1):
                                                a = 'opsw:'+str(taglist[i])
                                                varNames[i] = SubElement(opm, str(a))

                                    else:
                                        a = 'opsw:'+str(tagname[j])
                                        name[i] = SubElement(port, str(a))

            else:
                #logger.info("port-id should present in the <tagname> & <name>")
                pass
        xmlstr = tostring(ports)
        getConfig('getConfig - selectedProductInfo', xmlstr, outFileName)

    else:
        logger.error('port-id should present in <tagname> and <name> \n\n')

def getConfig(tcName, xmlstr, fileName):
    ### getConfig - configuration for required operation ###

    global swMgr
    global cnt

    try:
       logger.info('Quering for running configuration data from switch using getConfig\n\n')
       logger.info('Get  - pass XML str to the switch...\n\n')
       prettyXml = prettify(xmlstr)
       logger.info('xml str is : \n\n%s\n\n' % prettyXml)

       s = time.time()
       xmlData = swMgr.get_config(source='running', filter=('subtree',xmlstr)).data_xml
       print '\n\n'
       prettyXml = prettify(xmlData)
       logger.info('Get - Output from the switch\n\n%s\n' % prettyXml)

       e = time.time()
       t = int(round((e - s)* 1000))
       #t = (e - s)* 1000
       writeToFile(fileName,prettyXml);
       csvOutput('Ports', tcName, t, 'PASS')

    except Exception as err:
       print '\n\n'
       logger.error('\t\t-----[ Error from the Switch ]-----\n\n%s\n\n', err)
       csvOutput('Ports', tcName, 0, 'FAIL')

### create XML for edit-config ###

def editConfig_createPortLabel(prtIds):

    global PrtLblNames
    global prtIdLst
    global xmlStr
   
    createBox('editConfig - create port label')

    prtNames = []
    config = ConfigParser.ConfigParser()
    config.read('config.txt')
    egressPrtRange = (config.get("crossconnect", "egressPortRange")).split('-')

    for i in range(1, int(egressPrtRange[1])+1):
        s = 'RajaGanesh'+str(i)
        prtNames.append(s)
    logger.info('prtNames is : %s' % prtNames)


    config = Element('config')
    ports = SubElement(config, 'ports', {'xmlns':"http://www.polatis.com/yang/optical-switch",
                                         'xmlns:ns':"urn:ietf:params:xml:ns:netconf:base:1.0"})
    #ports = SubElement(config, 'ports', {'xmlns':"http://www.polatis.com/yang/optical-switch"})
    #port = SubElement(ports, 'port')
    #port_id = SubElement(port, 'port-id')
    #port_id.text = '1'
    #port_label = SubElement(port, 'port-label')
    #port_label.text = 'P1'


    prtIdSymbol = re.split(r'[\d]', prtIds)
    #logger.info('prtIdSymbol is : %s\n\n' % prtIdSymbol)

    if str(prtIdSymbol[1]) == ',' or str(prtIdSymbol[1]) == '' and str(prtIdSymbol[0]) == ',' or str(prtIdSymbol[0]) == '':
        prtIdLst = prtIds.split(',')
        logger.info('ingress port list: %s' % prtIdLst)
    
    if len(prtIdSymbol) >=3:
    
        if prtIdSymbol[1] == '-' or prtIdSymbol[2] == '-':
            #logger.info('***********      - -   ********************')
            prtIdLst = []
            prtIdLst1 = prtIds.split('-')
        
            if int(prtIdLst1[0]) > int(prtIdLst1[1]):
                prtIdLst1.reverse()
                for i in range(int(prtIdLst1[0]), int(prtIdLst1[1])+1):
                   prtIdLst.append(i)
                logger.info('ingress port list: %s' % prtIdLst)
            else:
                logger.info("inside else loop")
                #prtIdLst1.reverse()
                for i in range(int(prtIdLst1[0]), int(prtIdLst1[1])+1):
                    prtIdLst.append(i)
                logger.info('ingress port list: %s' % prtIdLst)

        #for i in range(int(prtIdLst1[0]), int(prtIdLst1[1])+1):
        #    prtIdLst.append(i)
        #logger.info('ingress port list: %s' % prtIdLst)
    else:
        pass
        #logger.error('Give for example comma or hypen seperated values ...\n\n')
        
    l = len(prtIdLst)
    for i in range(0, l):
        a = prtIdLst[i]
        port = SubElement(ports, 'port')
        port_id = SubElement(port, 'port-id')
        port_id.text = str(a)
        port_label = SubElement(port, 'port-label')
        #logger.info('type of a ', type(a))
        c = int(a) - 1
        b = prtNames[c]
        PrtLblNames.append(b)
        port_label.text = str(b)
           
    xmlstr = tostring(config)
    editConfig('editConfig_deletePrtLabel', xmlstr)

def editConfig_deleteLabel(prtIds):
    ### create XML for ports, pass it and get xml output file from switch ###
    global PrtLblNames
    global prtIdLst
    global xmlStr
    
    createBox('editConfig - delete port label')
    """
    #config = Element('config', {'xmlns:nc':"urn:ietf:params:xml:ns:netconf:base:1.0"})
    config = Element('config')
    ports = SubElement(config, 'ports', {'xmlns':"http://www.polatis.com/yang/optical-switch"})
    port = SubElement(ports, 'port', {'xmlns:ns':"urn:ietf:params:xml:ns:netconf:base:1.0"})
    port_id = SubElement(port, 'port-id')
    port_id.text = str(prtId)
    port_label = SubElement(port, 'port-label', {'ns:operation':'delete'})
    xmlStr = createXml('delete')
    xmlStr = tostring(config)
    logger.info('xmlstr is : %s\n\n' % xmlStr)
    editConfig('editConfig - Query ports', xmlStr)
    """
    prtNames = []
    config = ConfigParser.ConfigParser()
    config.read('config.txt')
    egressPrtRange = (config.get("crossconnect", "egressPortRange")).split('-')

    for i in range(1, int(egressPrtRange[1])+1):
        s = "Raja123"
        prtNames.append(s)
    #print prtNames


    config = Element('config')
    ports = SubElement(config, 'ports', {'xmlns':"http://www.polatis.com/yang/optical-switch",
                                         'xmlns:ns':"urn:ietf:params:xml:ns:netconf:base:1.0"})
    #ports = SubElement(config, 'ports', {'xmlns':"http://www.polatis.com/yang/optical-switch"})
    #port = SubElement(ports, 'port')
    #port_id = SubElement(port, 'port-id')
    #port_id.text = '1'
    #port_label = SubElement(port, 'port-label')
    #port_label.text = 'P1'


    prtIdSymbol = re.split(r'[\d]', prtIds)

    if str(prtIdSymbol[1]) == ',' or str(prtIdSymbol[1]) == '' and str(prtIdSymbol[0]) == ',' or str(prtIdSymbol[0]) == '':
        prtIdLst = prtIds.split(',')
        logger.info('ingress port list: %s' % prtIdLst)
   
    if len(prtIdSymbol) >= 3: 
        if str(prtIdSymbol[2]) == '-' or str(prtIdSymbol[1]) == '-':
            prtIdLst = []
            prtIdLst1 = prtIds.split('-')

            if int(prtIdLst1[0]) > int(prtIdLst1[1]):
                prtIdLst1.reverse()
                for i in range(int(prtIdLst1[0]), int(prtIdLst1[1])+1):
                    prtIdLst.append(i)
                logger.info('ingress port list: %s' % prtIdLst)
            else:
                logger.info("inside else loop")
                #prtIdLst1.reverse()
                for i in range(int(prtIdLst1[0]), int(prtIdLst1[1])+1):
                    prtIdLst.append(i)
                logger.info('ingress port list: %s' % prtIdLst)

    else:
        logger.error('Give for example comma or hypen seperated values ...\n\n')
        
    l = len(prtIdLst)
    for i in range(0, l):
        a = prtIdLst[i]
        port = SubElement(ports, 'port')
        port_id = SubElement(port, 'port-id')
        port_id.text = str(a)
        b = prtNames[i]
        PrtLblNames.append(b)
        port_label = SubElement(port, 'port-label', {'ns:operation':'delete'})
           
    xmlstr = tostring(config)
    editConfig('editConfig_deletePrtLabel', xmlstr)


### Enable ports ###

def editConfig_enablePorts(prtIds):

    global PrtLblNames
    global prtIdLst
    global xmlStr
   
    createBox('editConfig - enable port state')

    config = Element('config')
    ports = SubElement(config, 'ports', {'xmlns':"http://www.polatis.com/yang/optical-switch",
                                         'xmlns:ns':"urn:ietf:params:xml:ns:netconf:base:1.0"})
    

    prtIdSymbol = re.split(r'[\d]', prtIds)
    #logger.info('prtIdSymbol is : %s\n\n' % prtIdSymbol)

    if str(prtIdSymbol[1]) == ',' or str(prtIdSymbol[1]) == '' and str(prtIdSymbol[0]) == ',' or str(prtIdSymbol[0]) == '':
        prtIdLst = prtIds.split(',')
        logger.info('ingress port list: %s' % prtIdLst)
   

    if len(prtIdSymbol) >= 3: 
        if prtIdSymbol[1] == '-' or prtIdSymbol[2] == '-':
            #logger.info('***********      - -   ********************')
            prtIdLst = []
            prtIdLst1 = prtIds.split('-')
        
            if int(prtIdLst1[0]) > int(prtIdLst1[1]):
                prtIdLst1.reverse()
                for i in range(int(prtIdLst1[0]), int(prtIdLst1[1])+1):
                    prtIdLst.append(i)
                logger.info('ingress port list: %s' % prtIdLst)
            else:
                logger.info("inside else loop")
                #prtIdLst1.reverse()
                for i in range(int(prtIdLst1[0]), int(prtIdLst1[1])+1):
                    prtIdLst.append(i)
                logger.info('ingress port list: %s' % prtIdLst)

    
    else:
        pass
        #logger.error('Give for example comma or hypen seperated values ...\n\n')
        
    l = len(prtIdLst)
    for i in range(0, l):
        a = prtIdLst[i]
        port = SubElement(ports, 'port')
        port_id = SubElement(port, 'port-id')
        port_id.text = str(a)
        port_state = SubElement(port, 'port-state')
        port_state.text = 'PC_ENABLED'

    xmlstr = tostring(config)
    editConfig('editConfig_deletePrtLabel', xmlstr)

### Disable ports ###

def editConfig_disablePorts(prtIds):

    global PrtLblNames
    global prtIdLst
    global xmlStr
   
    createBox('editConfig - disable port state')

    config = Element('config')
    ports = SubElement(config, 'ports', {'xmlns':"http://www.polatis.com/yang/optical-switch",
                                         'xmlns:ns':"urn:ietf:params:xml:ns:netconf:base:1.0"})
    

    prtIdSymbol = re.split(r'[\d]', prtIds)
    #logger.info('prtIdSymbol is : %s\n\n' % prtIdSymbol)

    if str(prtIdSymbol[1]) == ',' or str(prtIdSymbol[1]) == '' and str(prtIdSymbol[0]) == ',' or str(prtIdSymbol[0]) == '':
        prtIdLst = prtIds.split(',')
        logger.info('ingress port list: %s' % prtIdLst)
   

    if len(prtIdSymbol) >= 3: 
        if prtIdSymbol[1] == '-' or prtIdSymbol[2] == '-':
            #logger.info('***********      - -   ********************')
            prtIdLst = []
            prtIdLst1 = prtIds.split('-')
        
            if int(prtIdLst1[0]) > int(prtIdLst1[1]):
                prtIdLst1.reverse()
                for i in range(int(prtIdLst1[0]), int(prtIdLst1[1])+1):
                    prtIdLst.append(i)
                logger.info('ingress port list: %s' % prtIdLst)
            else:
                logger.info("inside else loop")
                #prtIdLst1.reverse()
                for i in range(int(prtIdLst1[0]), int(prtIdLst1[1])+1):
                    prtIdLst.append(i)
                logger.info('ingress port list: %s' % prtIdLst)
    else:
        pass
        #logger.error('Give for example comma or hypen seperated values ...\n\n')
        
    l = len(prtIdLst)
    for i in range(0, l):
        a = prtIdLst[i]
        port = SubElement(ports, 'port')
        port_id = SubElement(port, 'port-id')
        port_id.text = str(a)
        port_state = SubElement(port, 'port-state')
        port_state.text = 'PC_DISABLED'

    xmlstr = tostring(config)
    editConfig('editConfig_deletePrtLabel', xmlstr)



def cmpIngEgrPortLst(xmlData):
    global xmlstr
    print "*************************"
    xmlprtIdLst = []
    xmlPrtLblNames = []
    global prtIdLst

    p = 'PASS'
    f = 'FAIL'

    DOMTree = xml.dom.minidom.parseString(xmlData)
    collection = DOMTree.documentElement

    ports = collection.getElementsByTagName("port")

    for port in ports:

        prtId = port.getElementsByTagName('port-id')[0]
        iD =  str(prtId.childNodes[0].data)

        xmlprtIdLst.append(iD)

        prtLabel = port.getElementsByTagName('port-label')[0]
        lblName =  str(prtLabel.childNodes[0].data)

        xmlPrtLblNames.append(lblName)

    logger.info('Port Ids and Port Label Names from getConfig\n\n')
    logger.info('req port Id list: %s' % str(prtIdLst))
    logger.info('req port label list: %s' % PrtLblNames)
    logger.info('parsed port Id list: %s' %xmlprtIdLst)
    logger.info('parsed Port Label Names list: %s\n\n' % xmlPrtLblNames)

    
    if str(prtIdLst) ==  str(xmlprtIdLst) and str(PrtLblNames) == str(xmlPrtLblNames):
        logger.info('compare the ports from switch edit config and get config ----> PASS\n')
        return p

    else:
        logger.error('compare the ports from switch edit config and get config ----> FAIL\n')
        return f



def editConfig(tcName, xmlstr):
    ### editConfig - configuration for required operation ###

    global swMgr
    global cnt
    global prtIdLst

    try:
       logger.info('Quering for running configuration data from switch using editConfig\n\n')
       logger.info('edit  - the XML str & passs it to the switch...\n\n')
       prettyXml = prettify(xmlstr)
       logger.info('xml str is : \n\n%s\n\n' % prettyXml)

       s = time.time()
       xmlData = swMgr.edit_config(target='running', config=xmlstr)

       prettyXml = prettify(str(xmlData))
       logger.info('EditConfig - Output from the switch\n\n%s\n' % prettyXml)

       ports = Element('opsw:ports', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                      'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
       try:
          l = len(prtIdLst)
          for i in range(0, l):
              a = prtIdLst[i]
              port = SubElement(ports, 'opsw:port')
              port_id = SubElement(port, 'opsw:port-id')
              port_id.text = str(a)
              port_label = SubElement(port, 'opsw:port-label')
       except Exception as err:
          logger.error('\t\t-----[ Error from the Switch ]-----\n\n%s\n\n' % err)


       #logger.info('-----[ Compare the Edit Config and Get Config Ports ]-----\n\n')
       #xmlstr = tostring(ports)
       #xmlData = swMgr.get_config(source='running',  filter=('subtree',xmlstr)).data_xml
       #print "\n\n"
     
       #prettyXml = prettify(xmlData)
       #logger.info('Get  config -  Response from the switch\n\n%s \n\n' % prettyXml)
       
       #result = cmpIngEgrPortLst(xmlData)
       
       e = time.time()
       t = int(round((e - s)* 1000))
       csvOutput('Ports', tcName, t, 'PASS')

    except Exception as err:
       print '\n\n'
       logger.error('\t\t-----[ Error from the Switch ]-----\n\n%s\n\n', err)
       csvOutput('Ports', tcName, 0, 'FAIL')




