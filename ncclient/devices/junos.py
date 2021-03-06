"""
Handler for Juniper device specific information.

Note that for proper import, the classname has to be:

    "<Devicename>DeviceHandler"

...where <Devicename> is something like "Default", "Junos", etc.

All device-specific handlers derive from the DefaultDeviceHandler, which implements the
generic information needed for interaction with a Netconf server.

"""

from .default import DefaultDeviceHandler
from ncclient.operations.third_party.juniper.rpc import GetConfiguration, LoadConfiguration, CompareConfiguration
from ncclient.operations.third_party.juniper.rpc import ExecuteRpc, Command, Reboot, Halt, Commit

class JunosDeviceHandler(DefaultDeviceHandler):
    """
    Juniper handler for device specific information.

    """
    def __init__(self, device_params):
        super(JunosDeviceHandler, self).__init__(device_params)

    def add_additional_operations(self):
        dict = {}
        dict["rpc"] = ExecuteRpc
        dict["get_configuration"] = GetConfiguration
        dict["load_configuration"] = LoadConfiguration
        dict["compare_configuration"] = CompareConfiguration
        dict["command"] = Command
        dict["reboot"] = Reboot
        dict["halt"] = Halt
        dict["commit"] = Commit
        return dict

    def perform_qualify_check(self):
        return False

    def handle_raw_dispatch(self, raw):
        if 'routing-engine' in raw:
                raw = re.sub(r'<ok/>', '</routing-engine>\n<ok/>', raw)
                return raw
        else:
            return False

    def handle_connection_exceptions(self, sshsession):
        c = sshsession._channel = sshsession._transport.open_channel(kind="session")
        c.set_name("netconf-command-" + str(sshsession._channel_id))
        c.exec_command("xml-mode netconf need-trailer")
        return True
    
    def transform_reply(self):
        return '''<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
        <xsl:output method="xml" indent="no"/>

        <xsl:template match="/|comment()|processing-instruction()">
            <xsl:copy>
                <xsl:apply-templates/>
            </xsl:copy>
        </xsl:template>

        <xsl:template match="*">
            <xsl:element name="{local-name()}">
                <xsl:apply-templates select="@*|node()"/>
            </xsl:element>
        </xsl:template>

        <xsl:template match="@*">
            <xsl:attribute name="{local-name()}">
                <xsl:value-of select="."/>
            </xsl:attribute>
        </xsl:template>
        </xsl:stylesheet>
        '''
