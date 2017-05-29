#!/usr/bin/env python3
import sys
from PyQt5 import QtGui, QtWidgets, QtCore

import os
srcroot=os.path.abspath(os.path.dirname(os.path.abspath(__file__))+"/..")

# import the MsgApp baseclass, for messages, and network I/O
sys.path.append(srcroot+"/MsgApp")
import MsgGui

from Messaging import Messaging

class BandwidthTester(MsgGui.MsgGui):
    def __init__(self, argv, parent=None):
        MsgGui.MsgGui.__init__(self, "Bandwidth Tester 0.1", argv, [], parent)
        
        self.lastTxSequence = 0
        self.lastRxSequence = 0
        self.txMsgCount = 0
        self.txLen = 0
        self.txByteCount = 0
        self.rxByteCount = 0
        self.rxBytesPerSec = 0
        self.txBytesPerSec = 0
        
        self.bandwidthTestMsgClass = Messaging.MsgClassFromName["Debug.BandwidthTest"]
        self.maxSeq = int(Messaging.findFieldInfo(self.bandwidthTestMsgClass.fields, "SequenceNumber").maxVal)
        self.maxLen = Messaging.findFieldInfo(self.bandwidthTestMsgClass.fields, "TestData").count
        
        # event-based way of getting messages
        self.RxMsg.connect(self.ProcessMessage)

        self.msgTimer = QtCore.QTimer(self)
        self.msgTimer.setInterval(10)
        self.msgTimer.timeout.connect(self.msgTimeout)

        self.displayTimer = QtCore.QTimer(self)
        self.displayTimer.setInterval(1000)
        self.displayTimer.timeout.connect(self.updateDisplay)
        self.displayTimer.start()

        vbox = QtWidgets.QVBoxLayout()
        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(vbox)
        self.setCentralWidget(centralWidget)
        
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        hbox.addWidget(QtWidgets.QLabel("Tx bytes"))
        self.txByteCountLabel = QtWidgets.QLabel()
        hbox.addWidget(self.txByteCountLabel)
        hbox.addWidget(QtWidgets.QLabel("Rx bytes"))
        self.rxByteCountLabel = QtWidgets.QLabel()
        hbox.addWidget(self.rxByteCountLabel)

        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        hbox.addWidget(QtWidgets.QLabel("Tx bytes/sec"))
        self.txBytesPerSecLabel = QtWidgets.QLabel()
        hbox.addWidget(self.txBytesPerSecLabel)
        hbox.addWidget(QtWidgets.QLabel("Rx bytes/sec"))
        self.rxBytesPerSecLabel = QtWidgets.QLabel()
        hbox.addWidget(self.rxBytesPerSecLabel)

        clearBtn = QtWidgets.QPushButton(self)
        clearBtn.setText('Clear')
        clearBtn.clicked.connect(self.clearStats)
        vbox.addWidget(clearBtn)
        
        timerSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        timerSlider.valueChanged.connect(self.msgTimer.setInterval)
        timerLabel = QtWidgets.QLabel()
        timerSlider.valueChanged.connect(lambda newVal: timerLabel.setText(str(newVal)+" ms"))
        timerSlider.setMinimum(10)
        timerSlider.setMaximum(1000)
        timerSlider.setValue(500)
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        hbox.addWidget(QtWidgets.QLabel("Timer (ms)"))
        hbox.addWidget(timerSlider)
        hbox.addWidget(timerLabel)
        
        txMsgCountSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        txMsgCountSlider.valueChanged.connect(self.setTxMsgCount)
        msgCountLabel = QtWidgets.QLabel()
        txMsgCountSlider.valueChanged.connect(lambda newVal: msgCountLabel.setText(str(newVal)+" msgs"))
        txMsgCountSlider.setMinimum(1)
        txMsgCountSlider.setMaximum(100)
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        hbox.addWidget(QtWidgets.QLabel("Msg Count"))
        hbox.addWidget(txMsgCountSlider)
        hbox.addWidget(msgCountLabel)

        txDataLenSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        txDataLenSlider.valueChanged.connect(self.setTxLen)
        txDataLenLabel = QtWidgets.QLabel()
        txDataLenSlider.valueChanged.connect(lambda newVal: txDataLenLabel.setText(str(newVal-1)+" bytes"))
        txDataLenSlider.setMinimum(1)
        txDataLenSlider.setMaximum(self.maxLen)
        txDataLenSlider.setValue(10)
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        hbox.addWidget(QtWidgets.QLabel("Msg Len"))
        hbox.addWidget(txDataLenSlider)
        hbox.addWidget(txDataLenLabel)

        self.startStop = QtWidgets.QPushButton(self)
        self.startStop.setText('Stop')
        self.startStop.clicked.connect(self.startStopFn)
        vbox.addWidget(self.startStop)
        
        self.msgTimer.start()
        
    def startStopFn(self):
        if self.msgTimer.isActive():
            self.msgTimer.stop()
            self.startStop.setText('Start')
        else:
            self.msgTimer.start()
            self.startStop.setText('Stop')
    
    def setTxMsgCount(self, txCount):
        self.txMsgCount = txCount

    def setTxLen(self, txLen):
        self.txLen = txLen

    def msgTimeout(self):
        bytesTransmitted = 0
        for i in range(0, self.txMsgCount):
            msg = self.bandwidthTestMsgClass()
            self.lastTxSequence += 1
            if self.lastTxSequence > self.maxSeq:
                self.lastTxSequence = 0
            msg.SetSequenceNumber(self.lastTxSequence)
            msgLen = 1
            for i in range(0, self.txLen-1):
                msg.SetTestData(i,i)
                msgLen += 1
            msg.hdr.SetDataLength(msgLen)
            self.txByteCount += msgLen
            self.txBytesPerSec += msgLen
            self.SendMsg(msg)
        self.txByteCountLabel.setText(str(self.txByteCount))

    def ProcessMessage(self, msg):
        if type(msg) == self.bandwidthTestMsgClass:
            desiredSeq = self.lastRxSequence+1
            if desiredSeq > self.maxSeq:
                desiredSeq = 0
            if msg.GetSequenceNumber() == desiredSeq:
                self.rxByteCount += 1 # 1 byte for sequence count
                self.rxBytesPerSec += 1
                for i in range(0, msg.hdr.GetDataLength()-1):
                    if i != msg.GetTestData(i):
                        print("ERROR! TestData["+str(i)+"] == " + str( msg.GetTestData(i)))
                    else:
                        self.rxByteCount += 1
                        self.rxBytesPerSec += 1
            else:
                print("ERROR!  Got sequence " + str(msg.GetSequenceNumber()) + ", but wanted " + str(self.lastRxSequence))
            self.lastRxSequence = msg.GetSequenceNumber()
            self.rxByteCountLabel.setText(str(self.rxByteCount))
    
    def clearStats(self):
        self.txByteCount = 0
        self.rxByteCount = 0
        self.txByteCountLabel.setText("0")
        self.rxByteCountLabel.setText("0")
    
    def updateDisplay(self):
        self.rxBytesPerSecLabel.setText(str(self.rxBytesPerSec))
        self.txBytesPerSecLabel.setText(str(self.txBytesPerSec))
        self.rxBytesPerSec = 0
        self.txBytesPerSec = 0

# main starts here
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    msgApp = BandwidthTester(sys.argv)
    msgApp.show()
    sys.exit(app.exec_())