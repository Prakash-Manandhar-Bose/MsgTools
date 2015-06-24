#ifndef __DATABUS_MESSAGE_H__
#define __DATABUS_MESSAGE_H__

#include <QObject>
#include <stdint.h>
#include <assert.h>

#include <Cpp/Network.h>

class Message
{
    public:
        Message(uint16_t len)
        {
            hdr.SetLength(len);
        }
        static Message* New(uint16_t datalen)
        {
            uint8_t* buffer = new uint8_t[sizeof(Message)+datalen];
            Message* dbmsg = new(buffer) Message(datalen);
            return dbmsg;
        }
        void CopyHdr(Message& rhs)
        {
            memcpy(&hdr, &rhs.hdr, sizeof(hdr));
        }

        ~Message()
        {
        }
        static int HeaderSize()
        {
            return sizeof(hdr);
        }
        uint8_t* RawBuffer()
        {
            return (uint8_t*)&hdr;
        }
        uint8_t* GetDataPtr() { return (uint8_t*)(&hdr+1); }
        uint16_t GetTotalLength()
        {
            return hdr.GetLength();
        }
        void SetPayloadLength(int len) { hdr.SetLength(len); }
        void SetMessageID(uint32_t id) { hdr.SetID(id); }
        bool Exists() {return true;}
    public:
        NetworkHeader hdr;
        uint8_t       m_data[0];
};

#endif

