#    <OUTPUTFILENAME>
#    Created <DATE> from:
#        Messages = <INPUTFILENAME>
#        Template = <TEMPLATEFILENAME>
#        Language = <LANGUAGEFILENAME>
#
#                     AUTOGENERATED FILE, DO NOT EDIT
import struct
import ctypes
from collections import OrderedDict
from <MESSAGINGMODULE> import *
import <MESSAGINGMODULE> as msg

class <MSGNAME> :
    SIZE = <MSGSIZE>
    MSG_OFFSET = 0
    # Enumerations
    <ENUMERATIONS>

    #@staticmethod
    #def Create() :
    #    message_buffer = ctypes.create_string_buffer(<MSGNAME>.SIZE)
    #    <INIT_CODE>
    #    return message_buffer
    
    def __init__(self, messageBuffer=None):
        doInit = 0
        if messageBuffer == None:
            doInit = 1
            messageBuffer = ctypes.create_string_buffer(<MSGNAME>.SIZE)
        else:
            try:
                messageBuffer.raw
            except AttributeError:
                newbuf = ctypes.create_string_buffer(len(messageBuffer))
                for i in range(0, len(messageBuffer)):
                    newbuf[i] = bytes(messageBuffer)[i]
                messageBuffer = newbuf
        # this is a trick to get us to store a copy of a pointer to a buffer, rather than making a copy of the buffer
        self.msg_buffer_wrapper = { "msg_buffer": messageBuffer }
        if doInit:
            self.initialize()

    def initialize(self):
            <INIT_CODE>
            pass
    
    def rawBuffer(self):
        # this is a trick to get us to store a copy of a pointer to a buffer, rather than making a copy of the buffer
        return self.msg_buffer_wrapper["msg_buffer"]

    @staticmethod
    def MsgName():
        return "<MSGNAME>"

    def SetMessageID(self, id):
        <SETMSGID>

    def GetMessageID(self):
        id = <GETMSGID>
        return id

    # Accessors
    <ACCESSORS>

    # Reflection information
    fields = [ \
        <REFLECTION>\
    ]
