import sys
import re
import csv
import time
import logging
from createCsv import csvOutput

from ncclient import manager
from xml.etree.ElementTree import Element, tostring, SubElement, XML
from xml.dom import minidom

global swMgr
global cnt
global xmlstr

xmlstr = ''

cnt = 1

logger = logging.getLogger('Polatis')
logger.setLevel(logging.INFO)

f = logging.FileHandler('demo.log')
f.setLevel(logging.INFO)


c = logging.StreamHandler()
c.setLevel(logging.INFO     )

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

def prettify(elem):
    ### create pretty xml ###
    reparsed = minidom.parseString(elem)
    return reparsed.toprettyxml(indent=" ")


def connectSwitch(host, port, userName, password, timeout):
    ### connecting to the Switch ###
    global swMgr

    logger.info("Connecting to  switch <IP:Port = %s:%s>\n" % (host,port))
    swMgr = manager.connect_ssh(host=host, port=port, username=userName, password=password,timeout=timeout, hostkey_verify=False)



def writeToFile(fileName, data):
    ### create switch output xml file ###
    f = open(fileName, 'w')
    f.write(data)
    f.close()



def productInformation(outFileName):
    ### create Product info xml and pass it and get output xml file from switch ###
    createBox('get - product_information')
    product_information = Element('opsw:product-information', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",

                                                               'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})

    xmlstr = tostring(product_information)
    get('get - product_information', xmlstr, outFileName)




def manufacturer(outFileName):
    ### create manufacturer xml and pass it and get output xml file from switch ###
    createBox('get - manufacturer')
    product_information = Element('opsw:product-information', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",

                                                               'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    manufacturer = SubElement(product_information, 'opsw:manufacturer')
    xmlstr = tostring(product_information)
    get('get - manufacturer', xmlstr, outFileName)



def serial_number(outFileName):
    ### create serial_number xml and pass it and get output xml file from switch ###
    createBox('get - serial_number') 
    product_information = Element('opsw:product-information', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",

                                                               'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    serial_number = SubElement(product_information, 'opsw:serial-number')
    xmlstr = tostring(product_information)
    get('get - serial_number', xmlstr, outFileName)


def model_name(outFileName):
    ### create model-name xml and pass it and get output xml file from switch ###
    createBox('get - model_name')

    product_information = Element('opsw:product-information', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                               'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    model_name = SubElement(product_information, 'opsw:model-name')
    xmlstr = tostring(product_information)
    get('get - model_name', xmlstr, outFileName)


def software_version(outFileName):
    ### create software-version xml and pass it and get output xml file from switch ###
    createBox('get - software_version')
    product_information = Element('opsw:product-information', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                               'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    software_version = SubElement(product_information, 'software-version')
    xmlstr = tostring(product_information)
    get('get - software_version', xmlstr, outFileName)


def ports(outFileName):
    ### create ports xml and pass it and get output xml file from switch ###
    createBox('get - ports')
    product_information = Element('opsw:product-information', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                               'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    ports = SubElement(product_information, 'opsw:ports')
    xmlstr = tostring(product_information)
    get('get - ports', xmlstr, outFileName)

def port_id(outFileName):
    ### create port_id xml and pass it and get output xml file from switch ###
    createBox('get - port_id')
    product_information = Element('opsw:product-information', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                               'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    ports = SubElement(product_information, 'opsw:ports')
    port_id = SubElement(ports, 'opsw:port-id')
    xmlstr = tostring(product_information)
    get('get - port_id', xmlstr, outFileName)


def port_type(outFileName):
    ### create port_type xml and pass it and get output xml file from switch ###
    createBox('get - port_type')
    product_information = Element('opsw:product-information', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                               'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    ports = SubElement(product_information, 'opsw:ports')
    port_type = SubElement(ports, 'opsw:port-type')
    xmlstr = tostring(product_information)
    get('get - port_type', xmlstr, outFileName)

def port_has_opm(outFileName):
    ### create port_has_opm xml and pass it and get output xml file from switch ###
    createBox('get - port_has_opm')
    product_information = Element('opsw:product-information', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                               'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    ports = SubElement(product_information, 'opsw:ports')
    has_opm = SubElement(ports, 'opsw:has_opm')
    xmlstr = tostring(product_information)
    get('get - port_has_opm', xmlstr, outFileName)


def port_has_oxc(outFileName):
    ### create port_has_oxc xml and pass it and get output xml file from switch ###
    createBox('get - port_has_oxc')
    product_information = Element('opsw:product-information', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                               'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
    ports = SubElement(product_information, 'opsw:ports')
    has_oxc = SubElement(ports, 'opsw:has_oxc')
    xmlstr = tostring(product_information)
    get('get - port_has_oxc', xmlstr, outFileName)



def selectedProductInfo(name, tagname, ids, outFileName):
    ### create xml from given info and pass it and get output xml file from switch ###
    createBox('get - selectedProductInfo')
    product_information = Element('opsw:product-information', {'xmlns:plts':"http://www.polatis.com/yang/polatis-switch",
                                                               'xmlns:opsw':"http://www.polatis.com/yang/optical-switch"})
   
    
    name = name.split(',')
    tagname = tagname.split(',')
    l = len(name)
    logger.info('<product information> sub tags name are  : %s\n\n' % tagname)


    for i,j in zip(range(0, l), range(0, l)):
        a = 'opsw:'+str(tagname[j])

        if name[i] == 'ports':
            if ids == 'allInfo':
                name[i] = SubElement(product_information, str(a))
            else:
                idTaglist = ids.split('/')
                logger.info('<ports> port-ids : %s\n\n' % idTaglist[0])
                logger.info('<ports> sub tags : %s\n\n' % idTaglist[1])

                idSymbol = re.split(r'[\d]', idTaglist[0])
                print "idSymbol : ", idSymbol
                ln = len(idTaglist[0])
                print "ln : ", ln
                if ln <= 2:
                    ids = idTaglist[0]
                    ports = SubElement(product_information, 'opsw:ports')
                    port_id = SubElement(ports, 'opsw:port-id')
                    port_id.text = str(ids)
                    if len(idTaglist[1]) == 0:
                        logger.info('There is no port info needed for this id\n\n')
                    else:
                        taglist = idTaglist[1].split(',')

                        l1 = len(taglist)

                        for i in range(0, l1):
                            symbol = re.split(r'[\w]', taglist[i])
                            if symbol[4] == '-':
                                name1 = taglist[i].split('-')
                            
                            elif symbol[4] == '_':
                                name1 = taglist[i].split('_')
                            a = 'opsw:'+str(taglist[i])
                            name1[1] = SubElement(ports, str(a))
                            #name1 = taglist[i].split('-')
                            #a = 'opsw:'+str(taglist[i])
                            #name1[1] = SubElement(ports, str(a))

                elif str(idSymbol[1]) == ',' or str(idSymbol[2]) == ',':
                    ids = idTaglist[0].split(',')
                    ln = len(ids)
                    for i in range(0, ln):
                        a = ids[i]
                        ports = SubElement(product_information, 'opsw:ports')
                        port_id = SubElement(ports, 'opsw:port-id')
                        port_id.text = str(a)
                        if len(idTaglist[1]) == 0:
                            logger.info('There is no port info needed for this id\n\n')
                        else:
                            taglist = idTaglist[1].split(',')
                            print "taglist :", taglist                            
                            l1 = len(taglist)
                            
                            for i in range(0, l1):
                                symbol = re.split(r'[\w]', taglist[i])
                                if symbol[4] == '-':
                                    name1 = taglist[i].split('-')
                                
                                elif symbol[4] == '_':
                                    name1 = taglist[i].split('_')
                                a = 'opsw:'+str(taglist[i])
                                name1[1] = SubElement(ports, str(a))
                                #try:
                                #    name1 = taglist[i].split('-')
                                #except:
                                #     name1 = taglist[i].split('_')
                                #print "name1 : ", name1
                                #a = 'opsw:'+str(taglist[i])
                                #print "name1 : ", name1[1]
                                #name1[1] = SubElement(ports, str(a))
                
                elif str(idSymbol[2]) == '-':
                    ids = idTaglist[0].split('-')
                    if ids[0] < ids[1]:
                        for i in range(int(ids[0]), int(ids[1])+1):
                            ports = SubElement(product_information, 'opsw:ports')
                            port_id = SubElement(ports, 'opsw:port-id')
                            port_id.text = str(i)
                            if len(idTaglist[1]) == 0:
                                logger.info('There is no port info needed for this id\n\n')
                            else:
                                taglist = idTaglist[1].split(',')

                                l1 = len(taglist)

                                for i in range(0, l1):
                                    symbol = re.split(r'[\w]', taglist[i])
                                    if symbol[4] == '-':
                                        name1 = taglist[i].split('-')
                                    
                                    elif symbol[4] == '_':
                                        name1 = taglist[i].split('_')
                                    a = 'opsw:'+str(taglist[i])
                                    name1[1] = SubElement(ports, str(a))
                    elif ids[0] > ids[1]:
                        for i in range(int(ids[1]), int(ids[0])+1):
                            ports = SubElement(product_information, 'opsw:ports')
                            port_id = SubElement(ports, 'opsw:port-id')
                            port_id.text = str(i)
                            if len(idTaglist[1]) == 0:
                                logger.info('There is no port info needed for this id\n\n')
                            else:
                                taglist = idTaglist[1].split(',')

                                l1 = len(taglist)

                                for i in range(0, l1):
                                    symbol = re.split(r'[\w]', taglist[i])
                                    if symbol[4] == '-':
                                        name1 = taglist[i].split('-')
                                    elif symbol[4] == '_':
                                        name1 = taglist[i].split('_')
                                    a = 'opsw:'+str(taglist[i])
                                    name1[1] = SubElement(ports, str(a))

        else:
            name[i] = SubElement(product_information, str(a))


    xmlstr = tostring(product_information)
    get('get - selectedProductInfo', xmlstr, outFileName)


def get(tcName, xmlstr, outFileName):
    ### get the given switch product information ####
    global swMgr

    try:
        logger.info('Quering for running configuration data from switch using get\n\n')
        logger.info('-------[[[Get  - pass xml query to switch]]]-------\n\n')
        prettyXmlstr = prettify(xmlstr)
        logger.info('xml str is : \n\n%s\n\n' %prettyXmlstr)
        print '\n\n'

        s = time.time()
        xmlData = swMgr.get(filter=('subtree',xmlstr)).data_xml
        print '\n\n'
        prettyXml = prettify(xmlData)
        logger.info('-------[[[Get - Output from the switch]]]-------\n\n%s\n' % prettyXml)

        e = time.time()
        t = int(round((e - s)* 1000))
        writeToFile(outFileName,prettyXml);
        csvOutput('productInformation', tcName, t, 'PASS')

    except Exception as err:
        print '\n\n'
        logger.error('\t\t-------[[[ Error from the Switch ]]]-------\n\n%s\n\n', err)
        csvOutput('productInformation', tcName, 0, 'FAIL')





