#!/usr/bin/env python3
#
# Creates a SynchronousMsg Client or Server, and uses it for a message console.
# Reads are JSON, writes are CSV.
#
import os
import sys
from SynchronousMsgServer import SynchronousMsgServer
from SynchronousMsgClient import SynchronousMsgClient

def main(args=None):
    # annoying stuff to start Messaging.
    # this should be simpler!
    thisFileDir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(thisFileDir+"/../..")
    from msgtools.lib.messaging import Messaging
    msgLib = Messaging(thisFileDir+"/../../../obj/CodeGenerator/Python/", 0, "NetworkHeader")

    if len(sys.argv) > 1 and sys.argv[1] == "server":
        connection = SynchronousMsgServer(msgLib)
    else:
        connection = SynchronousMsgClient(msgLib, "CLI")

    _cmd = ""
    try:
        while True:
            cmd = input("")
            #print("got input cmd [" + cmd + "]")
            if cmd:
                if cmd == "getmsg":
                    # this blocks until message received, or timeout occurs
                    timeout = 10.0 # value in seconds
                    msg = connection.get_message(timeout, [msgLib.Messages.Network.Connect.ID, msgLib.Messages.Debug.AccelData.Status.ID])
                    if msg:
                        # print as JSON for debug purposes
                        json = Messaging.toJson(msg)
                        print(json)
                    else:
                        print("{}")
                else:
                    # this translates the input command from CSV to a message, and sends it.
                    msg = Messaging.csvToMsg(cmd)
                    if msg:
                        connection.send_message(msg)
    # I can't get exit on Ctrl-C to work!
    except KeyboardInterrupt:
        print('You pressed Ctrl+C!')
        connection.stop()

if __name__ == "__main__":
    main()
