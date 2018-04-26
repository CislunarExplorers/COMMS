import ctypes
#import enum

#macros
c_uint8 = ctypes.c_uint8
c_uint16 = ctypes.c_uint16
c_uint32 = ctypes.c_uint32
c_float = ctypes.c_float
c_longdouble = ctypes.c_longdouble

ccsds_packet_size = 1024

"""
#packet type enum
class CMD_DATA_ENUM(Enum):
    CMD_PACKET = 0
    DATA_PACKET = 1
"""

#CCSDS Primary Header
class PriHeader(ctypes.LittleEndianStructure):
    _fields_ = [
            ("version", c_uint16, 3),
            ("type", c_uint16, 1),
            ("secHeaderFlag", c_uint16, 1),
            ("apid", c_uint16, 11),
            ("seqFlag", c_uint16, 2),
            ("seqCount", c_uint16, 14),
            ("packetLen", c_uint16, 16)
        ]

#CCSDS Secondary Header Flags
class SecHeaderFlags(ctypes.LittleEndianStructure):
    _fields_ = [
            ("checkwordIndicator", c_uint16, 1),
            ("reserved", c_uint16, 1)
        ]

#CCSDS Secondary Header
class SecHeader(ctypes.Union):
    _fields_ = [
            ("secHeaderFlags", SecHeaderFlags), #Check Python Doc to see how classes can be used as type (need enum or struct)
            ("timeSeconds", c_uint32),
            #Placeholder for Time struct from RTC
            ("timeSubseconds", c_uint32)
        ]

#CCSDS Full Header
class CCSDSHeader(ctypes.Union):
    _fields_ = [
            ("PriHeader", PriHeader),
            ("SecHeader", SecHeader)
        ]

#Data Packet
class Data(ctypes.Union):
    _fields_ = [
#           Power Health & Status
            ("Temperature", c_float),
            ("CurrInPPC0", c_float), #Current Into Photovoltaic Power Converter
            ("CurrInPPC1", c_float),
            ("CurrInPPC2", c_float),
            ("CurrOutPPC0", c_float),
            ("CurrOutPPC1", c_float),
            ("CurrOutPPC2", c_float),
            ("VoltInPPC0", c_float), 
            ("VoltInPPC1", c_float),
            ("VoltInPPC2", c_float),
            ("BatVolt", c_float),
            ("CurrInBC0", c_float), #Current Into Bus Converter
            ("CurrInBC1", c_float),
            ("CurrOutPC0", c_float), #Current Into Photovoltaic Power Converter
            ("CurrOutPC1", c_float), #Current Out Power Output Channels
            ("NumLatchPC0", c_uint16), #Number of Latch-Up Events for each Power Output Channel
            ("NumLatchPC1", c_uint16),
#           ADCNS
            ("Position0", c_longdouble),
            ("Position1", c_longdouble),
            ("Position2", c_longdouble),
            ("Attitude0", c_longdouble),
            ("Attitude1", c_longdouble),
            ("Attitude2", c_longdouble),
            ("Attitude3", c_longdouble),
            ("Time", c_longdouble),
#           CDH
            ("Pressure0", c_float),
            ("Pressure1", c_float)
        ]

#Basic Data Packet
class Data(ctypes.Union):
    _fields_ = [
#           Power Health & Status
            ("Temperature", c_float),
#           ADCNS
            ("Position0", c_longdouble),
            ("Position1", c_longdouble),
            ("Position2", c_longdouble),
            ("Attitude0", c_longdouble),
            ("Attitude1", c_longdouble),
            ("Attitude2", c_longdouble),
            ("Attitude3", c_longdouble),
#           CDH
            ("Time", c_longdouble),
            ("Pressure0", c_float),
            ("Pressure1", c_float)
        ]

#Full Message
class CCSDSData(ctypes.Union):
    _fields_ = [
            ("PriHeader", PriHeader),
            ("SecHeader", SecHeader),
            ("Data", Data)
        ]

#Full Command
class CCSDSCommand(ctypes.Union):
    _fields_ = [
            ("PriHeader", PriHeader),
            ("SecHeader", SecHeader),
            ("OpCode", c_uint16),
            ("ApId", c_uint16),
            ("Arg0", c_uint16),
            ("Arg1", c_uint16),
            ("Arg2", c_uint16),
            ("Arg3", c_uint16),
            ("Arg4", c_uint16),
            ("Arg5", c_uint16),
	    ("Delay", c_uint16)
        ]