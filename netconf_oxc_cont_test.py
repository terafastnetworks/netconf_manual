""" oxc continuous test """
from ncclient import manager
import time

create_xmlstr = """<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0"><cross-connects xmlns="http://www.polatis.com/yang/optical-switch"><pairs><ingress>1</ingress><egress>17</egress></pairs><pairs><ingress>2</ingress><egress>18</egress></pairs><pairs><ingress>3</ingress><egress>19</egress></pairs></cross-connects></config>"""


delete_xmlstr = """<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0"><cross-connects xmlns="http://www.polatis.com/yang/optical-switch"><pairs nc:operation = 'delete'><ingress>1</ingress><egress>17</egress></pairs><pairs nc:operation = 'delete'><ingress>2</ingress><egress>18</egress></pairs><pairs nc:operation = 'delete'><ingress>3</ingress><egress>19</egress></pairs></cross-connects></config>"""

cnt = 1

with manager.connect_ssh(host = '10.99.99.227', port = '830', username = 'admin', password = 'root', hostkey_verify=False) as m:
    while True:
        #print "m : %s\n" % m
        print "oxc create and delete operation  : %s\n\n" % cnt

        print "-----[ create oxc ]-----\n"
        xml_output = m.edit_config(target='running', config=create_xmlstr)
        print '\n\n'
        print "Response from the switch : \n\n%s\n" % xml_output
        print '\n\n'
        print "waiting for 20 sec\n"
        time.sleep(20)

        print "-----[ delete oxc ]-----\n"
        xml_output = m.edit_config(target='running', config=delete_xmlstr)
        print '\n\n'
        print "Response from the switch : \n\n%s\n" % xml_output
        print '\n\n'
        print "waiting for 20 sec\n"
        time.sleep(20)
 
        cnt = cnt+1
