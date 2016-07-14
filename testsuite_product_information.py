import os
import sys

from lib.productInfo import *


### product information operations 

def productInfo(opr):

    if opr == "connectSwitch":
        """Usage: <hostIP> <netconf-port> <username> <password> <timeout>\n"""
        connectSwitch('10.99.99.225', '830', 'admin', 'root', 60)

    if opr == "product-Information":
        """Usage: <output XML file>"""
        productInformation('productInfo.xml')

    if opr == "manufacturer":
        """Usage: <output XML file>"""
        manufacturer('manufacturer.xml')

    if opr == "serial_number":
        """Usage: <output XML file>"""
        serial_number('serial_number.xml')

    if opr == "model_name":
        """Usage: <output XML file>"""
        model_name('model_name.xml')

    if opr == "software_version":
        """Usage: <output XML file>"""
        software_version('software_version.xml')

    if opr == "ports":
        """Usage: <output XML file>"""
        ports('ports.xml')

    if opr == "port_id":
        """Usage: <output XML file>"""
        port_id('port_id.xml')

    if opr == "port_type":
        """Usage: <output XML file>"""
        port_type('port_type.xml')

    if opr == "port_has_opm":
        """Usage: <output XML file>"""
        port_has_opm('port_has_opm.xml')

    if opr == "port_has_oxc":
        """Usage: <output XML file>"""
        port_has_oxc('port_has_oxc.xml')

    if opr == "selectedProductInfo":
        """Usage: <tags variable name> <tags name> <'port-id's range':'subtags of ports'> <output XML file>"""
        #<tags variable name>                   : ports,serial_number,manufacturer,model_name,software_version
        #<tags name>                            : ports,serial-number,manufacturer,model-name,software-version
        #<port-id's range/subtags of ports>     : see below three format
        #<port-id's range>                      : 1-5, 1,2,3
        #subtags of ports                       : port-type,has_opm,has_oxc
        # 1.                                    : 1-24/port-type,has_opm,has_oxc
        # 2.                                    : 1,2,3...24/has_opm
        # 3.                                    : 'allInfo'  (If you need all ports info)

        selectedProductInfo('ports,serial_number,manufacturer,model_name,software_version','ports,serial-number,manufacturer,model-name,software-version', '1/port-type,has_opm,has_oxc', 'selectedProductInfo.xml')



### main

if __name__ == '__main__':
    productInfo('connectSwitch')
    #productInfo('product-Information')
    productInfo('selectedProductInfo')
    #productInfo('product-Information')
    #productInfo('port_has_oxc')
    #productInfo('port_has_opm')
    #productInfo('port_type')
    #productInfo('port_id')
    #productInfo('ports')
    #productInfo('software_version')
    #productInfo('model_name')
    #productInfo('manufacturer')


