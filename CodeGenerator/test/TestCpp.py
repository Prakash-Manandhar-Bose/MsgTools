import unittest
import yaml
import sys
sys.path.append(".")
import MsgParser
sys.path.append("Cpp")
import language

class TestCpp(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.msgIDL = """
Messages:
  - Name: MsgA
    Description: blah
    Fields:
      - Name: FieldA
        Type: uint32
        DefaultValue: 1
        Bitfields:
            - Name: BitsA
              NumBits: 31
      - Name: FieldB
        Type: uint16
        DefaultValue: 2
      - Name: FieldC
        Type: uint8
        DefaultValue: 3
        Count: 5
      - Name: FieldD
        Type: uint8
        Bitfields:
            - Name: BitsA
              NumBits: 4
              DefaultValue: 7
            - Name: BitsB
              NumBits: 3
            - Name: BitsC
              NumBits: 1
              DefaultValue: 1
      - Name: FieldE
        Type: Float32
        DefaultValue: 3.14159
        """
        self.msgDict = yaml.load(self.msgIDL)

    def test_accessors(self):
        expected = []
        expected.append("""\
uint32_t GetFieldA()
{
    return *(uint32_t*)&m_data[0];
}""")
        expected.append("""\
uint32_t GetFieldABitsA()
{
    return (GetFieldA() >> 0) & 0x7fffffff;
}""")
        expected.append("""\
uint16_t GetFieldB()
{
    return *(uint16_t*)&m_data[4];
}""")
        expected.append("""\
uint8_t GetFieldC(int idx)
{
    return *(uint8_t*)&m_data[6+idx*1];
}""")
        expected.append("""\
uint8_t GetFieldD()
{
    return *(uint8_t*)&m_data[11];
}""")
        expected.append("""\
uint8_t GetFieldDBitsA()
{
    return (GetFieldD() >> 0) & 0xf;
}""")
        expected.append("""\
uint8_t GetFieldDBitsB()
{
    return (GetFieldD() >> 4) & 0x7;
}""")
        expected.append("""\
uint8_t GetFieldDBitsC()
{
    return (GetFieldD() >> 7) & 0x1;
}""")
        expected.append("""\
float GetFieldE()
{
    return *(float*)&m_data[12];
}""")
        expected.append("""\
void SetFieldA(uint32_t& value)
{
    *(uint32_t*)&m_data[0] = value;
}""")
        expected.append("""\
void SetFieldABitsA(uint32_t& value)
{
    SetFieldA((GetFieldA() & ~(0x7fffffff << 0)) | ((value & 0x7fffffff) << 0));
}""")
        expected.append("""\
void SetFieldB(uint16_t& value)
{
    *(uint16_t*)&m_data[4] = value;
}""")
        expected.append("""\
void SetFieldC(uint8_t& value, int idx)
{
    *(uint8_t*)&m_data[6+idx*1] = value;
}""")
        expected.append("""\
void SetFieldD(uint8_t& value)
{
    *(uint8_t*)&m_data[11] = value;
}""")
        expected.append("""\
void SetFieldDBitsA(uint8_t& value)
{
    SetFieldD((GetFieldD() & ~(0xf << 0)) | ((value & 0xf) << 0));
}""")
        expected.append("""\
void SetFieldDBitsB(uint8_t& value)
{
    SetFieldD((GetFieldD() & ~(0x7 << 4)) | ((value & 0x7) << 4));
}""")
        expected.append("""\
void SetFieldDBitsC(uint8_t& value)
{
    SetFieldD((GetFieldD() & ~(0x1 << 7)) | ((value & 0x1) << 7));
}""")
        expected.append("""\
void SetFieldE(float& value)
{
    *(float*)&m_data[12] = value;
}""")
        expCount = len(expected)
        observed = language.accessors(MsgParser.Messages(self.msgDict)[0])
        obsCount = len(observed)
        self.assertEqual(expCount, obsCount)
        
        for i in range(expCount):
            self.assertMultiLineEqual(expected[i], observed[i])
        with self.assertRaises(IndexError):
            language.accessors(MsgParser.Messages(self.msgDict)[1])

    def test_msgNames(self):
        expected = "MsgA"
        observed = MsgParser.msgName(MsgParser.Messages(self.msgDict)[0])
        self.assertMultiLineEqual(expected, observed)
        with self.assertRaises(IndexError):
            MsgParser.msgName(MsgParser.Messages(self.msgDict)[1])
    
    def test_initCode(self):
        expected = []
        expected.append("SetFieldA(1);")
        expected.append("SetFieldB(2);")
        expected.append("SetFieldC(3);")
        expected.append("SetFieldDBitsA(7);")
        expected.append("SetFieldDBitsC(1);")
        expected.append("SetFieldE(3.14159);")
        expCount = len(expected)
        observed = language.initCode(MsgParser.Messages(self.msgDict)[0])
        obsCount = len(observed)
        self.assertEqual(expCount, obsCount)
        for i in range(expCount):
            self.assertMultiLineEqual(expected[i], observed[i])
        with self.assertRaises(IndexError):
            language.initCode(MsgParser.Messages(self.msgDict)[1])

if __name__ == '__main__':
    unittest.main()