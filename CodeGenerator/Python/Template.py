#    <OUTPUTFILENAME>
#    Created <DATE> from:
#        Messages = <INPUTFILENAME>
#        Template = <TEMPLATEFILENAME>
#        Language = <LANGUAGEFILENAME>
#
#                     AUTOGENERATED FILE, DO NOT EDIT
import struct
import ctypes
from Messaging import *
import Messaging as msg

class <MSGNAME> :
    ID = <MSGID>
    SIZE = <MSGSIZE>
    MSG_OFFSET = Messaging.hdrSize
    fields = [ \
        <REFLECTION>\
    ]
    
    @staticmethod
    def set(message_buffer, fieldInfo, value, index=1):
        Messaging.set(<MSGNAME>, message_buffer, fieldInfo, value, index)

    @staticmethod
    def get(message_buffer, fieldInfo, index=1):
        return Messaging.get(<MSGNAME>, message_buffer, fieldInfo, index)

    @staticmethod
    def Create() :
        message_buffer = ctypes.create_string_buffer(<MSGNAME>.MSG_OFFSET + <MSGNAME>.SIZE)

        Messaging.hdr.SetSource(message_buffer, 0)
        Messaging.hdr.SetDestination(message_buffer, 0)
        Messaging.hdr.SetID(message_buffer, <MSGNAME>.ID)
        Messaging.hdr.SetLength(message_buffer, <MSGNAME>.SIZE)
        Messaging.hdr.SetPriority(message_buffer, 0)
        Messaging.hdr.SetType(message_buffer, 0)

        <INIT_CODE>
        return message_buffer

    @staticmethod
    def MsgName():
        return "<MSGNAME>"
    # Enumerations
    <ENUMERATIONS>
    # Accessors
    <ACCESSORS>

Messaging.Register("<MSGNAME>", <MSGNAME>.ID, <MSGNAME>)
