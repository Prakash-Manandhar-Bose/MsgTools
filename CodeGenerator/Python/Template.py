#    <OUTPUTFILENAME>
#    Created <DATE> from:
#        Messages = <INPUTFILENAME>
#        Template = <TEMPLATEFILENAME>
#        Language = <LANGUAGEFILENAME>
#
#                     AUTOGENERATED FILE, DO NOT EDIT
import struct
import ctypes
from Messaging import Messaging
import Messaging as msg

class <MSGNAME> :
    ID = <MSGID>
    MSG_SIZE = <MSGSIZE>
    @staticmethod
    def Create() :
        bytes = ctypes.create_string_buffer(<MSGNAME>.MSG_SIZE)
        <INIT_CODE>
        return bytes

    @staticmethod
    def MsgName():
        return "<MSGNAME>"
    <ENUMERATIONS>
    <ACCESSORS>
