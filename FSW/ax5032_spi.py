from ctypes import *
from pigpio import *
import sys
import numpy as np
import time

#TODO: NEED TO REDO POINTER BUMPS


#Macros from ax5043_spi.h
#Addresses from = 0x000 to = 0x06F are reserved for ?dynamic registers?, i.e. registers that are expected to be frequently accessed during normal operation
#Addresses from = 0x070 to = 0x0FF have been left unused (they could only be accessed using the two address byte SPI format).
#Addresses from = 0x100 to = 0x1FF have been reserved for physical layer parameter registers, for example receiver, transmitter, PLL, crystal oscillator.
#Addresses from = 0x200 to = 0x2FF have been reserved for medium access parameters, such as framing, packet handling.
#Addresses from = 0x300 to = 0x3FF have been reserved for special functions, such as GPADC.

AX_REG_SILICONREVISION = 0x000 #Silicon Revision
AX_REG_SCRATCH = 0x001 #Scratch
AX_REG_PWRMODE = 0x002 #Power Mode
AX_REG_POWSTAT = 0x003 #Power Management Status 
AX_REG_POWSTICKYSTAT = 0x004 	#Power Management Sticky Status 
AX_REG_POWIRQMASK = 0x005 	#Power Management Interrupt Mask 
AX_REG_IRQMASK1 = 0x006 	#IRQ Mask 1 
AX_REG_IRQMASK0 = 0x007 	#IRQ Mask 0 
AX_REG_RADIOEVENTMASK1 = 0x008 	#Radio Event Mask 1 
AX_REG_RADIOEVENTMASK0 = 0x009 	#Radio Event Mask 0 
AX_REG_IRQINVERSION1 = 0x00A 	#IRQ Inversion 1 
AX_REG_IRQINVERSION0 = 0x00B 	#IRQ Inversion 0 
AX_REG_IRQREQUEST1 = 0x00C 	#IRQ Request 1 
AX_REG_IRQREQUEST0 = 0x00D 	#IRQ Request 0 
AX_REG_RADIOEVENTREQ1 = 0x00E 	#Radio Event Request 1 
AX_REG_RADIOEVENTREQ0 = 0x00F 	#Radio Event Request 0 
AX_REG_MODULATION = 0x010 	#Modulation 
AX_REG_ENCODING = 0x011 	#Encoding 
AX_REG_FRAMING = 0x012 	#Framing Mode 
AX_REG_CRCINIT3 = 0x014 	#CRC Initial Value 3 
AX_REG_CRCINIT2 = 0x015 	#CRC Initial Value 2 
AX_REG_CRCINIT1 = 0x016 	#CRC Initial Value 1 
AX_REG_CRCINIT0 = 0x017 	#CRC Initial Value 0 
AX_REG_FEC = 0x018 	#Forward Error Correction 
AX_REG_FECSYNC = 0x019 	#Forward Error Correction Sync Threshold 
AX_REG_FECSTATUS = 0x01A 	#Forward Error Correction Status 
AX_REG_RADIOSTATE = 0x01C 	#Radio Controller State 
AX_REG_XTALSTATUS = 0x01D 	#Crystal Oscillator Status 
AX_REG_PINSTATE = 0x020 	#Pin State 
AX_REG_PINFUNCSYSCLK = x021 	#Pin Function SYSCLK 
AX_REG_PINFUNCDCLK = 0x022 	#Pin Function DCLK 
AX_REG_PINFUNCDATA = 0x023 	#Pin Function DATA 
AX_REG_PINFUNCIRQ = 0x024 	#Pin Function IRQ 
AX_REG_PINFUNCANTSEL = 0x025 	#Pin Function ANTSEL 
AX_REG_PINFUNCPWRAMP = 0x026 	#Pin Function PWRAMP 
AX_REG_PWRAMP = 0x027 	#PWRAMP Control 
AX_REG_FIFOSTAT = 0x028 	#FIFO Control 
AX_REG_FIFODATA = 0x029 	#FIFO Data 
AX_REG_FIFOCOUNT1 = 0x02A 	#Number of Words currently in FIFO 1 
AX_REG_FIFOCOUNT0 = 0x02B 	#Number of Words currently in FIFO 0 
AX_REG_FIFOFREE1 = 0x02C 	#Number of Words that can be written to FIFO 1 
AX_REG_FIFOFREE0 = 0x02D 	#Number of Words that can be written to FIFO 0 
AX_REG_FIFOTHRESH1 = 0x02E 	#FIFO Threshold 1 
AX_REG_FIFOTHRESH0 = 0x02F 	#FIFO Threshold 0 
AX_REG_PLLLOOP = 0x030 	#PLL Loop Filter Settings 
AX_REG_PLLCPI = 0x031 	#PL Charge Pump Current 
AX_REG_PLLVCODIV = 0x032 	#PLL Divider Settings 
AX_REG_PLLRANGINGA = 0x033 	#PLL Autoranging A 
AX_REG_FREQA3 = 0x034 	#Frequency A 3 
AX_REG_FREQA2 = 0x035 	#Frequency A 2 
AX_REG_FREQA1 = 0x036 	#Frequency A 1 
AX_REG_FREQA0 = 0x037 	#Frequency A 0 
AX_REG_PLLLOOPBOOST = 0x038 	#PLL Loop Filter Settings (Boosted) 
AX_REG_PLLCPIBOOST = 0x039 	#PLL Charge Pump Current (Boosted) 
AX_REG_PLLRANGINGB = 0x03B 	#PLL Autoranging B 
AX_REG_FREQB3 = 0x03C 	#Frequency B 3 
AX_REG_FREQB2 = 0x03D 	#Frequency B 2 
AX_REG_FREQB1 = 0x03E 	#Frequency B 1 
AX_REG_FREQB0 = 0x03F 	#Frequency B 0 
AX_REG_RSSI = 0x040 	#Received Signal Strength Indicator 
AX_REG_BGNDRSSI = 0x041 	#Background RSSI 
AX_REG_DIVERSITY = 0x042 	#Antenna Diversity Configuration 
AX_REG_AGCCOUNTER = 0x043 	#AGC Counter 
AX_REG_TRKDATARATE2 = 0x045 	#Datarate Tracking 2 
AX_REG_TRKDATARATE1 = 0x046 	#Datarate Tracking 1 
AX_REG_TRKDATARATE0 = 0x047 	#Datarate Tracking 0 
AX_REG_TRKAMPL1 = 0x048 	#Amplitude Tracking 1 
AX_REG_TRKAMPL0 = 0x049 	#Amplitude Tracking 0 
AX_REG_TRKPHASE1 = 0x04A 	#Phase Tracking 1 
AX_REG_TRKPHASE0 = 0x04B 	#Phase Tracking 0 
AX_REG_TRKRFFREQ2 = 0x04D 	#RF Frequency Tracking 2 
AX_REG_TRKRFFREQ1 = 0x04E 	#RF Frequency Tracking 1 
AX_REG_TRKRFFREQ0 = 0x04F 	#RF Frequency Tracking 0 
AX_REG_TRKFREQ1 = 0x050 	#Frequency Tracking 1 
AX_REG_TRKFREQ0 = 0x051 	#Frequency Tracking 0 
AX_REG_TRKFSKDEMOD1 = 0x052 	#FSK Demodulator Tracking 1 
AX_REG_TRKFSKDEMOD0 = 0x053 	#FSK Demodulator Tracking 0 
AX_REG_TRKAFSKDEMOD1 = 0x054 	#AFSK Demodulator Tracking 1 
AX_REG_TRKAFSKDEMOD0 = 0x055 	#AFSK Demodulator Tracking 0 
AX_REG_TIMER2 = 0x059 	#1MHz Timer 2 
AX_REG_TIMER1 = 0x05A 	#1Mz Timer 1 
AX_REG_TIMER0 = 0x05B 	#1MHz Timer 0 
AX_REG_WAKEUPTIMER1 = 0x068 	#Wakeup Timer 1 
AX_REG_WAKEUPTIMER0 = 0x069 	#Wakeup Timer 0 
AX_REG_WAKEUP1 = 0x06A 	#Wakeup Time 1 
AX_REG_WAKEUP0 = 0x06B 	#Wakeup Time 0 
AX_REG_WAKEUPFREQ1 = 0x06C 	#Wakeup Frequency 1 
AX_REG_WAKEUPFREQ0 = 0x06D 	#Wakeup Frequency 0 
AX_REG_WAKEUPXOEARLY = 0x06E 	#Wakeup Crystal Oscillator Early 
AX_REG_IFFREQ1 = 0x100 	#2nd LO / IF Frequency 1 
AX_REG_IFFREQ0 = 0x101 	#2nd LO / IF Frequency 0 
AX_REG_DECIMATION = 0x102 	#Decimation Factor 
AX_REG_RXDATARATE2 = 0x103 	#Receiver Datarate 2 
AX_REG_RXDATARATE1 = 0x104 	#Receiver Datarate 1 
AX_REG_RXDATARATE0 = 0x105 	#Receiver Datarate 0 
AX_REG_MAXDROFFSET2 = 0x106 	#Maximum Receiver Datarate Offset 2 
AX_REG_MAXDROFFSET1 = 0x107 	#Maximum Receiver Datarate Offset 1 
AX_REG_MAXDROFFSET0 = 0x108 	#Maximum Receiver Datarate Offset 0 
AX_REG_MAXRFOFFSET2 = 0x109 	#Maximum Receiver RF Offset 2 
AX_REG_MAXRFOFFSET1 = 0x10A 	#Maximum Receiver RF Offset 1 
AX_REG_MAXRFOFFSET0 = 0x10B 	#Maximum Receiver RF Offset 0 
AX_REG_FSKDMAX1 = 0x10C 	#Four FSK Rx Maximum Deviation 1 
AX_REG_FSKDMAX0 = 0x10D 	#Four FSK Rx Maximum Deviation 0 
AX_REG_FSKDMIN1 = 0x10E 	#Four FSK Rx Minimum Deviation 1 
AX_REG_FSKDMIN0 = 0x10F 	#Four FSK Rx Minimum Deviation 0 
AX_REG_AFSKSPACE1 = 0x110 	#AFSK Space (0) Frequency 1 
AX_REG_AFSKSPACE0 = 0x111 	#AFSK Space (0) Frequency 0 
AX_REG_AFSKMARK1 = 0x112 	#AFSK Mark =(1) Frequency 1 
AX_REG_AFSKMARK0 = 0x113 	#AFSK Mark =(1) Frequency 0 
AX_REG_AFSKCTRL = 0x114 	#AFSK Control 
AX_REG_AMPLFILTER = 0x115 	#Amplitude Filter 
AX_REG_FREQUENCYLEAK = 0x116 	#Baseband Frequency Recovery Loop Leakiness 
AX_REG_RXPARAMSETS = 0x117 	#Receiver Parameter Set Indirection 
AX_REG_RXPARAMCURSET = 0x118 	#Receiver Parameter Current Set 
AX_REG_AGCGAIN0 = 0x120 	#AGC Speed 
AX_REG_AGCTARGET0 = 0x121 	#AGC Target 
AX_REG_AGCAHYST0 = 0x122 	#AGC Analog Hysteresis 
AX_REG_AGCMINMAX0 = 0x123 	#AGC Analog Update Behaviour 
AX_REG_TIMEGAIN0 = 0x124 	#Time Estimator Bandwidth 
AX_REG_DRGAIN0 = 0x125 	#Data Rate Estimator Bandwidth 
AX_REG_PHASEGAIN0 = 0x126 	#Phase Estimator Bandwidth 
AX_REG_FREQUENCYGAINA0 = 0x127 	#Frequency Estimator Bandwidth A 
AX_REG_FREQUENCYGAINB0 = 0x128 	#Frequency Estimator Bandwidth B 
AX_REG_FREQUENCYGAINC0 = 0x129 	#Frequency Estimator Bandwidth C 
AX_REG_FREQUENCYGAIND0 = 0x12A 	#Frequency Estimator Bandwidth D 
AX_REG_AMPLITUDEGAIN0 = 0x12B 	#Amplitude Estimator Bandwidth 
AX_REG_FREQDEV10 = 0x12C 	#Receiver Frequency Deviation 1 
AX_REG_FREQDEV00 = 0x12D 	#Receiver Frequency Deviation 0 
AX_REG_FOURFSK0 = 0x12E 	#Four FSK Control 
AX_REG_BBOFFSRES0 = 0x12F 	#Baseband Offset Compensation Resistors 
AX_REG_AGCGAIN1 = 0x130 	#AGC Speed 
AX_REG_AGCTARGET1 = 0x131 	#AGC Target 
AX_REG_AGCAHYST1 = 0x132 	#AGC Analog Hysteresis 
AX_REG_AGCMINMAX1 = 0x133 	#AGC Analog Update Behaviour 
AX_REG_TIMEGAIN1 = 0x134 	#Time Estimator Bandwidth 
AX_REG_DRGAIN1 = 0x135 	#Data Rate Estimator Bandwidth 
AX_REG_PHASEGAIN1 = 0x136 	#Phase Estimator Bandwidth 
AX_REG_FREQUENCYGAINA1 = 0x137 	#Frequency Estimator Bandwidth A 
AX_REG_FREQUENCYGAINB1 = 0x138 	#Frequency Estimator Bandwidth B 
AX_REG_FREQUENCYGAINC1 = 0x139 	#Frequency Estimator Bandwidth C 
AX_REG_FREQUENCYGAIND1 = 0x13A 	#Frequency Estimator Bandwidth D 
AX_REG_AMPLITUDEGAIN1 = 0x13B 	#Amplitude Estimator Bandwidth 
AX_REG_FREQDEV11 = 0x13C 	#Receiver Frequency Deviation 1 
AX_REG_FREQDEV01 = 0x13D 	#Receiver Frequency Deviation 0 
AX_REG_FOURFSK1 = 0x13E 	#Four FSK Control 
AX_REG_BBOFFSRES1 = 0x13F 	#Baseband Offset Compensation Resistors 
AX_REG_AGCGAIN2 = 0x140 	#AGC Speed 
AX_REG_AGCTARGET2 = 0x141 	#AGC Target 
AX_REG_AGCAHYST2 = 0x142 	#AGC Analog Hysteresis 
AX_REG_AGCMINMAX2 = 0x143 	#AGC Analog Update Behaviour 
AX_REG_TIMEGAIN2 = 0x144 	#Time Estimator Bandwidth 
AX_REG_DRGAIN2 = 0x145 	#Data Rate Estimator Bandwidth 
AX_REG_PHASEGAIN2 = 0x146 	#Phase Estimator Bandwidth 
AX_REG_FREQUENCYGAINA2 = 0x147 	#Frequency Estimator Bandwidth A 
AX_REG_FREQUENCYGAINB2 = 0x148 	#Frequency Estimator Bandwidth B 
AX_REG_FREQUENCYGAINC2 = 0x149 	#Frequency Estimator Bandwidth C 
AX_REG_FREQUENCYGAIND2 = 0x14A 	#Frequency Estimator Bandwidth D 
AX_REG_AMPLITUDEGAIN2 = 0x14B 	#Amplitude Estimator Bandwidth 
AX_REG_FREQDEV12 = 0x14C 	#Receiver Frequency Deviation 1 
AX_REG_FREQDEV02 = 0x14D 	#Receiver Frequency Deviation 0 
AX_REG_FOURFSK2 = 0x14E 	#Four FSK Control 
AX_REG_BBOFFSRES2 = 0x14F 	#Baseband Offset Compensation Resistors 
AX_REG_AGCGAIN3 = 0x150 	#AGC Speed 
AX_REG_AGCTARGET3 = 0x151 	#AGC Target 
AX_REG_AGCAHYST3 = 0x152 	#AGC Analog Hysteresis 
AX_REG_AGCMINMAX3 = 0x153 	#AGC Analog Update Behaviour 
AX_REG_TIMEGAIN3 = 0x154 	#Time Estimator Bandwidth 
AX_REG_DRGAIN3 = 0x155 	#Data Rate Estimator Bandwidth 
AX_REG_PHASEGAIN3 = 0x156 	#Phase Estimator Bandwidth 
AX_REG_FREQUENCYGAINA3 = 0x157 	#Frequency Estimator Bandwidth A 
AX_REG_FREQUENCYGAINB3 = 0x158 	#Frequency Estimator Bandwidth B 
AX_REG_FREQUENCYGAINC3 = 0x159 	#Frequency Estimator Bandwidth C 
AX_REG_FREQUENCYGAIND3 = 0x15A 	#Frequency Estimator Bandwidth D 
AX_REG_AMPLITUDEGAIN3 = 0x15B 	#Amplitude Estimator Bandwidth 
AX_REG_FREQDEV13 = 0x15C 	#Receiver Frequency Deviation 1 
AX_REG_FREQDEV03 = 0x15D 	#Receiver Frequency Deviation 0 
AX_REG_FOURFSK3 = 0x15E 	#Four FSK Control 
AX_REG_BBOFFSRES3 = 0x15F 	#Baseband Offset Compensation Resistors 
AX_REG_MODCFGF = 0x160 	#Modulator Configuration F 
AX_REG_FSKDEV2 = 0x161 	#FSK Deviation 2 
AX_REG_FSKDEV1 = 0x162 	#FSK Deviation 1 
AX_REG_FSKDEV0 = 0x163 	#FSK Deviation 0 
AX_REG_MODCFGA = 0x164 	#Modulator Configuration A 
AX_REG_TXRATE2 = 0x165 	#Transmitter Bitrate 2 
AX_REG_TXRATE1 = 0x166 	#Transmitter Bitrate 1 
AX_REG_TXRATE0 = 0x167 	#Transmitter Bitrate 0 
AX_REG_TXPWRCOEFFA1 = 0x168 	#Transmitter Predistortion Coefficient A 1 
AX_REG_TXPWRCOEFFA0 = 0x169 	#Transmitter Predistortion Coefficient A 0 
AX_REG_TXPWRCOEFFB1 = 0x16A 	#Transmitter Predistortion Coefficient B 1 
AX_REG_TXPWRCOEFFB0 = 0x16B 	#Transmitter Predistortion Coefficient B 0 
AX_REG_TXPWRCOEFFC1 = 0x16C 	#Transmitter Predistortion Coefficient C 1 
AX_REG_TXPWRCOEFFC0 = 0x16D 	#Transmitter Predistortion Coefficient C 0 
AX_REG_TXPWRCOEFFD1 = 0x16E 	#Transmitter Predistortion Coefficient D 1 
AX_REG_TXPWRCOEFFD0 = 0x16F 	#Transmitter Predistortion Coefficient D 0 
AX_REG_TXPWRCOEFFE1 = 0x170 	#Transmitter Predistortion Coefficient E 1 
AX_REG_TXPWRCOEFFE0 = 0x171 	#Transmitter Predistortion Coefficient E 0 
AX_REG_PLLVCOI = 0x180 	#PLL VCO Current 
AX_REG_PLLVCOIR = 0x181 	#PLL VCO Current Readback 
AX_REG_PLLLOCKDET = 0x182 	#PLL Lock Detect Delay 
AX_REG_PLLRNGCLK = 0x183 	#PLL Autoranging Clock 
AX_REG_XTALCAP = 0x184 	#Crystal Oscillator Load Capacitance 
AX_REG_BBTUNE = 0x188 	#Baseband Tuning 
AX_REG_BBOFFSCAP = 0x189 	#Baseband Offset Compensation Capacitors 
AX_REG_PKTADDRCFG = 0x200 	#Packet Address Config 
AX_REG_PKTLENCFG = 0x201 	#Packet Length Configuration 
AX_REG_PKTLENOFFSET = 0x202 	#Packet Length Offset 
AX_REG_PKTMAXLEN = 0x203 	#Packet Maximum Length 
AX_REG_PKTADDR3 = 0x204 	#Packet Address 3 
AX_REG_PKTADDR2 = 0x205 	#Packet Address 2 
AX_REG_PKTADDR1 = 0x206 	#Packet Address 1 
AX_REG_PKTADDR0 = 0x207 	#Packet Address 0 
AX_REG_PKTADDRMASK3 = 0x208 	#Packet Address Mask 3 
AX_REG_PKTADDRMASK2 = 0x209 	#Packet Address Mask 2 
AX_REG_PKTADDRMASK1 = 0x20A 	#Packet Address Mask 1 
AX_REG_PKTADDRMASK0 = 0x20B 	#Packet Address Mask 0 
AX_REG_MATCH0PAT3 = 0x210 	#Pattern Match Unit 0 Pattern 3 
AX_REG_MATCH0PAT2 = 0x211 	#Pattern Match Unit 0 Pattern 2 
AX_REG_MATCH0PAT1 = 0x212 	#Pattern Match Unit 0 Pattern 1 
AX_REG_MATCH0PAT0 = 0x213 	#Pattern Match Unit 0 Pattern 0 
AX_REG_MATCH0LEN = 0x214 	#Pattern Match Unit 0 Pattern Length 
AX_REG_MATCH0MIN = 0x215 	#Pattern Match Unit 0 Minimum Match 
AX_REG_MATCH0MAX = 0x216 	#Pattern Match Unit 0 Maximum Match 
AX_REG_MATCH1PAT1 = 0x218 	#Pattern Match Unit 1 Pattern 1 
AX_REG_MATCH1PAT0 = 0x219 	#Pattern Match Unit 1 Pattern 0 
AX_REG_MATCH1LEN = 0x21C 	#Pattern Match Unit 1 Pattern Length 
AX_REG_MATCH1MIN = 0x21D 	#Pattern Match Unit 1 Minimum Match 
AX_REG_MATCH1MAX = 0x21E 	#Pattern Match Unit 1 Maximum Match 
AX_REG_TMGTXBOOST = 0x220 	#Transmit PLL Boost Time 
AX_REG_TMGTXSETTLE = 0x221 	#Transmit PLL (post Boost) Settling Time 
AX_REG_TMGRXBOOST = 0x223 	#Receive PLL Boost Time 
AX_REG_TMGRXSETTLE = 0x224 	#Receive PLL (post Boost) Settling Time 
AX_REG_TMGRXOFFSACQ = 0x225 	#Receive Baseband DC Offset Acquisition Time 
AX_REG_TMGRXCOARSEAGC = 0x226 	#Receive Coarse AGC Time 
AX_REG_TMGRXAGC = 0x227 	#Receiver AGC Settling Time 
AX_REG_TMGRXRSSI = 0x228 	#Receiver RSSI Settling Time 
AX_REG_TMGRXPREAMBLE1 = 0x229 	#Receiver Preamble 1 Timeout 
AX_REG_TMGRXPREAMBLE2 = 0x22A 	#Receiver Preamble 2 Timeout 
AX_REG_TMGRXPREAMBLE3 = 0x22B 	#Receiver Preamble 3 Timeout 
AX_REG_RSSIREFERENCE = 0x22C 	#RSSI Offset 
AX_REG_RSSIABSTHR = 0x22D 	#RSSI Absolute Threshold 
AX_REG_BGNDRSSIGAIN = 0x22E 	#Background RSSI Averaging Time Constant 
AX_REG_BGNDRSSITHR = 0x22F 	#Background RSSI Relative Threshold 
AX_REG_PKTCHUNKSIZE = 0x230 	#Packet Chunk Size 
AX_REG_PKTMISCFLAGS = 0x231 	#Packet Controller Miscellaneous Flags 
AX_REG_PKTSTOREFLAGS = 0x232 	#Packet Controller Store Flags 
AX_REG_PKTACCEPTFLAGS = 0x233 	#Packet Controller Accept Flags 
AX_REG_GPADCCTRL = 0x300 	#General Purpose ADC Control 
AX_REG_GPADCPERIOD = 0x301 	#GPADC Sampling Period 
AX_REG_GPADC13VALUE1 = 0x308 	#GPADC13 Value 1 
AX_REG_GPADC13VALUE0 = 0x309 	#GPADC13 Value 0 
AX_REG_LPOSCCONFIG = 0x310 	#Low Power Oscillator Calibration Configuration 
AX_REG_LPOSCSTATUS = 0x311 	#Low Power Oscillator Calibration Status 
AX_REG_LPOSCKFILT1 = 0x312 	#Low Power Oscillator Calibration Filter Constant High Byte 
AX_REG_LPOSCKFILT0 = 0x313 	#Low Power Oscillator Calibration Filter Constant Low Byte 
AX_REG_LPOSCREF1 = 0x314 	#Low Power Oscillator Reference Frequency High Byte 
AX_REG_LPOSCREF0 = 0x315 	#Low Power Oscillator Reference Frequency Low Byte 
AX_REG_LPOSCFREQ1 = 0x316 	#Low Power Oscillator Frequency Tuning High Byte 
AX_REG_LPOSCFREQ0 = 0x317 	#Low Power Oscillator Frequency Tuning Low Byte 
AX_REG_LPOSCPER1 = 0x318 	#Low Power Oscillator Period High Byte 
AX_REG_LPOSCPER0 = 0x319 	#Low Power Oscillator Period Low Byte 
AX_REG_DACVALUE1 = 0x330 	#DAC Value 1 
AX_REG_DACVALUE0 = 0x331 	#DAC Value 0 
AX_REG_DACCONFIG = 0x332 	#DAC Configuration 
AX_REG_POWCTRL1 = 0xF08 	#Power Control 1 
AX_REG_REF = 0xF0D 	#Reference 
AX_REG_XTALOSC = 0xF10 	#Crystal Oscillator Control 
AX_REG_XTALAMPL = 0xF11 	#Crystal Oscillator Amplitude Control 

AX_REG_TUNE_F00 = 0xF00 	#Tuning Registers 
AX_REG_TUNE_F0C = 0xF0C 	#Tuning Registers 
AX_REG_TUNE_F0D = 0xF0D 	#Tuning Registers 
AX_REG_TUNE_F10 = 0xF10 	#Tuning Registers 
AX_REG_TUNE_F11 = 0xF11 	#Tuning Registers 
AX_REG_TUNE_F18 = 0xF18 	#Tuning Registers 
AX_REG_TUNE_F1C = 0xF1C 	#Tuning Registers 
AX_REG_TUNE_F21 = 0xF21 	#Tuning Registers 
AX_REG_TUNE_F22 = 0xF22 	#Tuning Registers 
AX_REG_TUNE_F23 = 0xF23 	#Tuning Registers 
AX_REG_TUNE_F26 = 0xF26 	#Tuning Registers 
AX_REG_TUNE_F30 = 0xF30 	#Tuning Registers 
AX_REG_TUNE_F31 = 0xF31 	#Tuning Registers 
AX_REG_TUNE_F32 = 0xF32 	#Tuning Registers 
AX_REG_TUNE_F33 = 0xF33 	#Tuning Registers 
AX_REG_TUNE_F34 = 0xF34 	#Tuning Registers 
AX_REG_TUNE_F35 = 0xF35 	#Tuning Registers 
AX_REG_TUNE_F44 = 0xF44 	#Tuning Registers 
AX_REG_TUNE_F72 = 0xF72 	#Tuning Registers 

AX_REG_MODCFGP = 0xF5F

AX_REG_POWSTAT_SVIO_MASK 	  =(1<<0)  # IOVoltage good
AX_REG_POWSTAT_SBEVMODEM_MASK =(1<<1)  # Modem Voltage Good
AX_REG_POWSTAT_SBEVANA_MASK   =(1<<2)  # Analog voltage okay
AX_REG_POWSTAT_SVMODEM_MASK   =(1<<3)  # Modem Vreg ready
AX_REG_POWSTAT_SVANA_MASK 	  =(1<<4)  # Analog vreg ready
AX_REG_POWSTAT_SVREF_MASK 	  =(1<<5)  # Ref Vreg ready
AX_REG_POWSTAT_SREF_MASK 	  =(1<<6)  # Reference ready
AX_REG_POWSTAT_SSUM_MASK 	  =(1<<7)  # Indicates all power sources are ready, Just check this guy. 

AX_REG_POWIRQMASK_MSVIO_MASK 	  =(1<<0)  # IOVoltage good
AX_REG_POWIRQMASK_MSBEVMODEM_MASK =(1<<1)  # Modem Voltage Good
AX_REG_POWIRQMASK_MSBEVANA_MASK   =(1<<2)  # Analog voltage okay
AX_REG_POWIRQMASK_MSVMODEM_MASK   =(1<<3)  # Modem Vreg ready
AX_REG_POWIRQMASK_MSVANA_MASK 	  =(1<<4)  # Analog vreg ready
AX_REG_POWIRQMASK_MSVREF_MASK     =(1<<5)  # Ref Vreg ready
AX_REG_POWIRQMASK_MSREF_MASK 	  =(1<<6)  # Reference ready
AX_REG_POWIRQMASK_MSSUM_MASK 	  =(1<<7)  # Indicates all power sources are ready, Just check this bit 

AX_REG_PWRMODE_POWERDOWN_MASK 	 = (0x00) # All circuits powered down
AX_REG_PWRMODE_DEEP_SLEEP_MASK 	 = (0x01) # Deep sleep, all registers dead, lost contents
AX_REG_PWRMODE_XTALEN_MASK       = (0x05) # Xtal osc is en
AX_REG_PWRMODE_FIFOEN_MASK       = (0x07)
AX_REG_PWRMODE_SYNTH_RUN_RX_MASK = (0x08) # Synth is running , its in receive mode
AX_REG_PWRMODE_RX_RUN_MASK       = (0x09)
AX_REG_IRQINVERSION0_FIFO_NOTFULL_MASK 	=(1<<1) # FIFO not full inturrupt inversion
AX_REG_IRQINVERSION0_FIFO_THRCNT_MASK 	=(1<<2) # FIFO count > threshold interrupt inversion
AX_REG_IRQINVERSION0_FIFO_THRFREE_MASK 	=(1<<3) # FIFO free > threshold interrupt inversion
AX_REG_IRQINVERSION0_FIFO_ERROR_MASK 	=(1<<4) # FIFO error interrupt inversion
AX_REG_IRQINVERSION0_PLL_UNLOCK_MASK 	=(1<<5) # PLL lock lost inturrupt inversion
AX_REG_IRQINVERSION0_RADIO_CTRL_MASK 	=(1<<6) # Radio controller inturrupt inversion
AX_REG_IRQINVERSION0_POWER_MASK 	 	=(1<<7) # Power interrupt inversion
AX_REG_IRQINVERSION1_XTAL_READY_MASK 	=(1<<0) # Crystal oscillator ready interrupt inversion
AX_REG_IRQINVERSION1_WAKEUP_TIMER_MASK 	=(1<<1) # Wakeup timer interrupt inversion
AX_REG_IRQINVERSION1_LP_OSC_MASK 		=(1<<2) # Low power oscillator inturrupt inversion
AX_REG_IRQINVERSION1_GPADC_MASK 		=(1<<3) # GPADC interrupt inversion
AX_REG_IRQINVERSION1_PLL_RNG_DONE_MASK 	=(1<<4) # PLL autoranging done interrupt inversion

AX_REG_MODULATION_ASK_MASK          = (0x00)
AX_REG_MODULATION_ASK_COHERENT_MASK = (0x01)
AX_REG_MODULATION_PSK_MASK          = (0x04)
AX_REG_MODULATION_OQSK_MASK 		= (0x06)
AX_REG_MODULATION_MSK_MASK          = (0x07)
AX_REG_MODULATION_FSK_MASK          = (0x08)
AX_REG_MODULATION_4FSK_MASK 		= (0x09)
AX_REG_MODULATION_AFSK_MASK 		= (0x0A)
AX_REG_MODULATION_FM_MASK           = (0x0B)
AX_REG_MODULATION_RX_HALFSPEED_MASK =(1<<4) # Sets the receiver to half speed bitrate

AX_REG_ENCODING_INV_MASK 		=(1<<0)  # Invert data if set to 1
AX_REG_ENCODING_DIFF_MASK 		=(1<<1)  # Enable differential encode/decode
AX_REG_ENCODING_SCRAM_MASK 		=(1<<2)  # Enable the scrambler
AX_REG_ENCODING_MANCH_MASK 		=(1<<3)  # Enable manchester encoding
AX_REG_ENCODING_NOSYNC_MASK 	=(1<<4)  # Disable dibit sync in 4fsk mode
# To use NRZI, set inv to high, and set diff to 1

AX_REG_FRAMING_FABORT_MASK                  =(1<<0)
AX_REG_FRAMING_FRMMODE_RAW_MASK             = (0x00 << 1)
AX_REG_FRAMING_FRMMODE_RAW_SOFT_MASK        = (0x01 << 1)
AX_REG_FRAMING_FRMMODE_HDLC_MASK            = (0x02 << 1)
AX_REG_FRAMING_FRMMODE_RAW_PAT_MATCH_MASK   = (0x03 << 1)
AX_REG_FRAMING_FRMMODE_MBUS_MASK            = (0x04 << 1)
AX_REG_FRAMING_FRMMODE_MBUS_4TO6_MASK       = (0x05 << 1)

AX_REG_FRAMING_CRC_OFF_MASK 		= (0x00 << 4)
AX_REG_FRAMING_CRC_CCITT_MASK 		= (0x01 << 4)
AX_REG_FRAMING_CRC_CRC16_MASK 		= (0x02 << 4)
AX_REG_FRAMING_CRC_DNP_MASK 		= (0x03 << 4)
AX_REG_FRAMING_CRC_CRC32_MASK 		= (0x04 << 4)

AX_REG_FRAMING_FRMRX_MASK 		= (0x01 << 7) # Flag set when flag is detected in HDLC mode or when preamble matches in raw pattern mode. Cleared by writting 1 to FABORT

AX_REG_FEC_FECEN_MASK 			=(1<<0) # Enable FEC

AX_REG_RADIOSTATE_IDLE_MASK             = (0x00)
AX_REG_RADIOSTATE_POWER_DOWN_MASK       = (0x01)
AX_REG_RADIOSTATE_TX_PLL_MASK           = (0x04)
AX_REG_RADIOSTATE_TX_MASK               = (0x06)
AX_REG_RADIOSTATE_TX_TAIL_MASK          = (0x07)
AX_REG_RADIOSTATE_RX_PLL_MASK           = (0x08)
AX_REG_RADIOSTATE_RX_ANT_MASK           = (0x09)
AX_REG_RADIOSTATE_RX_PREAMBLE_1_MASK    = (0x0C)
AX_REG_RADIOSTATE_RX_PREAMBLE_2_MASK 	= (0x0D)
AX_REG_RADIOSTATE_RX_PREAMBLE_3_MASK 	= (0x0E)
AX_REG_RADIOSTATE_RX_MASK               = (0x0F)

AX_REG_XTALSTATUS_MASK 			= (0x01) # A 1 indicates that the crystal oscilator is up and running. 

AX_REG_PINSTATE_SYSCLK_MASK 	=(1<<0)
AX_REG_PINSTATE_DCLK_MASK 		=(1<<1)
AX_REG_PINSTATE_DATA_MASK 		=(1<<2)
AX_REG_PINSTATE_IRQ_MASK 		=(1<<3)
AX_REG_PINSTATE_ANTSEL_MASK 	=(1<<4)
AX_REG_PINSTATE_PWRAMP_MASK 	=(1<<5)

AX_REG_PINFUNSYSCLK_OUT_ZERO_MASK           = (0x00)
AX_REG_PINFUNSYSCLK_OUT_ONE_MASK            = (0x01)
AX_REG_PINFUNSYSCLK_OUT_HIGHZ_MASK          = (0x02)
AX_REG_PINFUNSYSCLK_OUT_INV_XTAL_MASK       = (0x03)
AX_REG_PINFUNSYSCLK_OUT_XTAL_MASK           = (0x04)
AX_REG_PINFUNSYSCLK_OUT_XTAL_DIV2_MASK      = (0x05)
AX_REG_PINFUNSYSCLK_OUT_XTAL_DIV4_MASK      = (0x06)
AX_REG_PINFUNSYSCLK_OUT_XTAL_DIV8_MASK      = (0x07)
AX_REG_PINFUNSYSCLK_OUT_XTAL_DIV16_MASK     = (0x08)
AX_REG_PINFUNSYSCLK_OUT_XTAL_DIV32_MASK     = (0x09)
AX_REG_PINFUNSYSCLK_OUT_XTAL_DIV64_MASK     = (0x0A)
AX_REG_PINFUNSYSCLK_OUT_XTAL_DIV128_MASK 	= (0x0B)
AX_REG_PINFUNSYSCLK_OUT_XTAL_DIV256_MASK 	= (0x0C)
AX_REG_PINFUNSYSCLK_OUT_XTAL_DIV512_MASK 	= (0x0D)
AX_REG_PINFUNSYSCLK_OUT_XTAL_DIV1024_MASK 	= (0x0E)
AX_REG_PINFUNSYSCLK_OUT_LP_OSC_MASK 		= (0x0F)
AX_REG_PINFUNSYSCLK_OUT_TEST_OBS_OSC_MASK 	= (0x1F)

AX_REG_PINFUNSYSCLK_PUSYCLK_MASK 	=(1<<7) # Enables the weak pullup

AX_REG_PINFUNCIRQ_ZERO_MASK 		= (0x00)
AX_REG_PINFUNCIRQ_ONE_MASK          = (0x01)
AX_REG_PINFUNCIRQ_HIGH_Z_MASK 		= (0x02)
AX_REG_PINFUNCIRQ_IRQ_MASK          = (0x03) # Enables the IRQ output
AX_REG_PINFUNCIRQ_TEST_OBS_MASK 	= (0x07)
AX_REG_PINFUNCIRQ_PIIRQ_MASK 		=(1 << 6) # Inverts the data on the IRQ line
AX_REG_PINFUNCIRQ_PUIRQ_MASK 		=(1 << 7) # Enables the weak pullup on the IRQ line

AX_REG_PINFUNCANTSEL_ZERO_MASK              = (0x00) # Outputs zero on the antenna select pin
AX_REG_PINFUNCANTSEL_ONE_MASK               = (0x01)
AX_REG_PINFUNCANTSEL_HIGH_Z_MASK            = (0x02)
AX_REG_PINFUNCANTSEL_BASEBAND_CLK_MASK      = (0x03)
AX_REG_PINFUNCANTSEL_EXTERNAL_TCXO_MASK     = (0x04)
AX_REG_PINFUNCANTSEL_DAC_MASK               = (0x05)
AX_REG_PINFUNCANTSEL_DIVERSITY_ANT_SEL_MASK = (0x06)
AX_REG_PINFUNCANTSEL_TEST_OBS_MASK          = (0x07)
AX_REG_PINFUNCANTSEL_INV_MASK               =(1<<6)
AX_REG_PINFUNCANTSEL_PULLUP_MASK            =(1<<7)

PWRMODE_POWERDOWN = 0x00 # All circuits dead. Except the register.  
PWRMODE_DEEPSLEEP = 0x01 # Now I really mean all circuits are dead. Data loss 
PWRMODE_STANDBY = 0x05 # Xtal OSC enabled 
PWRMODE_FIFOON = 0x07  # The FIFO and the crystal are enabled 
PWRMODE_SYNTHRX = 0x08 # The synth is running, in receive mode 
PWRMODE_FULLRX = 0x09 # The receiver is running 
PWRMODE_WORRX = 0x0B # Wake on radio mode 
PWRMODE_SYNTHTX = 0x0C # The synth is running, transmit mode 
PWRMODE_FULLTX = 0x0D # The transmitter is running.

class reg_pair(BigEndianStructure):
    _fields_ = [
        ("address",              c_uint16),
        ("data",               c_uint8),
    ]

class radio_settings(BigEndianStructure):
    _fields_ = [
        (" MODULATION ",             reg_pair),
        (" ENCODING ",             reg_pair),
        (" FRAMING ",             reg_pair),
        (" PINFUNCSYSCLK ",             reg_pair),
        (" IFFREQ1 ",             reg_pair),
        (" IFFREQ0 ",             reg_pair),
        (" DECIMATION ",             reg_pair),
        (" RXDATARATE2 ",             reg_pair),
        (" RXDATARATE1 ",             reg_pair),
        (" RXDATARATE0 ",             reg_pair),
        (" MAXDROFFSET2 ",             reg_pair),
        (" MAXDROFFSET1 ",             reg_pair),
        (" MAXDROFFSET0 ",             reg_pair),
        (" MAXRFOFFSET2 ",             reg_pair),
        (" MAXRFOFFSET1 ",             reg_pair),
        (" MAXRFOFFSET0 ",             reg_pair),
        (" AMPLFILTER ",             reg_pair),
        (" RXPARAMSETS ",             reg_pair),
        (" AGCGAIN0 ",             reg_pair),
        (" AGCTARGET0 ",             reg_pair),
        (" TIMEGAIN0 ",             reg_pair),
        (" DRGAIN0 ",             reg_pair),
        (" PHASEGAIN0 ",             reg_pair),
        (" FREQUENCYGAINA0 ",             reg_pair),
        (" FREQUENCYGAINB0 ",             reg_pair),
        (" FREQUENCYGAINC0 ",             reg_pair),
        (" FREQUENCYGAIND0 ",             reg_pair),
        (" AMPLITUDEGAIN0 ",             reg_pair),
        (" FREQDEV10 ",             reg_pair),
        (" FREQDEV00 ",             reg_pair),
        (" BBOFFSRES0 ",             reg_pair),
        (" AGCGAIN1 ",             reg_pair),
        (" AGCTARGET1 ",             reg_pair),
        (" AGCAHYST1 ",             reg_pair),
        (" AGCMINMAX1 ",             reg_pair),
        (" TIMEGAIN1 ",             reg_pair),
        (" DRGAIN1 ",             reg_pair),
        (" PHASEGAIN1 ",             reg_pair),
        (" FREQUENCYGAINA1 ",             reg_pair),
        (" FREQUENCYGAINB1 ",             reg_pair),
        (" FREQUENCYGAINC1 ",             reg_pair),
        (" FREQUENCYGAIND1 ",             reg_pair),
        (" AMPLITUDEGAIN1 ",             reg_pair),
        (" FREQDEV11 ",             reg_pair),
        (" FREQDEV01 ",             reg_pair),
        (" FOURFSK1 ",             reg_pair),
        (" BBOFFSRES1 ",             reg_pair),
        (" AGCGAIN3 ",             reg_pair),
        (" AGCTARGET3 ",             reg_pair),
        (" AGCAHYST3 ",             reg_pair),
        (" AGCMINMAX3 ",             reg_pair),
        (" TIMEGAIN3 ",             reg_pair),
        (" DRGAIN3 ",             reg_pair),
        (" PHASEGAIN3 ",             reg_pair),
        (" FREQUENCYGAINA3 ",             reg_pair),
        (" FREQUENCYGAINB3 ",             reg_pair),
        (" FREQUENCYGAINC3 ",             reg_pair),
        (" FREQUENCYGAIND3 ",             reg_pair),
        (" AMPLITUDEGAIN3 ",             reg_pair),
        (" FREQDEV13 ",             reg_pair),
        (" FREQDEV03 ",             reg_pair),
        (" FOURFSK3 ",             reg_pair),
        (" BBOFFSRES3 ",             reg_pair),
        (" MODCFGF ",             reg_pair),
        (" FSKDEV2 ",             reg_pair),
        (" FSKDEV1 ",             reg_pair),
        (" FSKDEV0 ",             reg_pair),
        (" MODCFGA ",             reg_pair),
        (" TXRATE2 ",             reg_pair),
        (" TXRATE1 ",             reg_pair),
        (" TXRATE0 ",             reg_pair),
        (" TXPWRCOEFFB1 ",             reg_pair),
        (" TXPWRCOEFFB0 ",             reg_pair),
        (" PLLVCOI ",             reg_pair),
        (" PLLRNGCLK ",             reg_pair),
        (" BBTUNE ",             reg_pair),
        (" BBOFFSCAP ",             reg_pair),
        (" TMGTXBOOST ",             reg_pair),
        (" TMGTXSETTLE ",             reg_pair),
        (" TMGRXBOOST ",             reg_pair),
        (" TMGRXSETTLE ",             reg_pair),
        (" TMGRXOFFSACQ ",             reg_pair),
        (" TMGRXCOARSEAGC ",             reg_pair),
        (" TMGRXPREAMBLE2 ",             reg_pair),
        (" PKTCHUNKSIZE ",             reg_pair),
        (" PKTACCEPTFLAGS ",             reg_pair),
        (" REF ",             reg_pair),
        (" XTALOSC ",             reg_pair),
        (" XTALAMPL ",             reg_pair),
        (" TUNE_F1C ",             reg_pair),
        (" TUNE_F21 ",             reg_pair),
        (" TUNE_F22 ",             reg_pair),
        (" TUNE_F23 ",             reg_pair),
        (" TUNE_F26 ",             reg_pair),              
        (" TUNE_F34 ",             reg_pair),
        (" TUNE_F35 ",             reg_pair),
        (" TUNE_F44 ",             reg_pair),
        (" PLLLOOP ",             reg_pair),
        (" PLLCPI ",             reg_pair),
        (" PLLVCODIV ",             reg_pair),
        (" XTALCAP ",             reg_pair),
        (" TUNE_F00 ",             reg_pair),
        (" TUNE_F18 ",             reg_pair),
        (" TMGRXAGC ",             reg_pair),
        (" TMGRXPREAMBLE1 ",             reg_pair),
        (" PKTMISCFLAGS ",             reg_pair),
        (" FREQA0 ",             reg_pair),
        (" FREQA1 ",             reg_pair),
        (" FREQA2 ",             reg_pair),
        (" FREQA3 ",             reg_pair),
        (" RSSIREFERENCE ",             reg_pair),
        (" MATCH0PAT3 ",             reg_pair),
        (" MATCH0PAT2 ",             reg_pair),
        (" MATCH0PAT1 ",             reg_pair),
        (" MATCH0PAT0 ",             reg_pair),
        (" MATCH0LEN ",             reg_pair),
        (" MATCH0MAX ",             reg_pair),
        (" MATCH1PAT1 ",             reg_pair),
        (" MATCH1PAT0 ",             reg_pair),
        (" MATCH1LEN ",             reg_pair),
        (" MATCH1MAX ",             reg_pair),
        (" PKTLENCFG ",             reg_pair),
        (" PKTLENOFFSET ",             reg_pair),
        (" PKTMAXLEN ",             reg_pair),
        (" PKTSTOREFLAGS ",             reg_pair),
#additional
        (" PINFUNCDCLK ",             reg_pair),
        (" PINFUNCDATA ",             reg_pair),
        (" PINFUNCANTSEL ",             reg_pair),
        (" PINFUNCPWRAMP ",             reg_pair),
        (" WAKEUPXOEARLY ",             reg_pair),
        (" FSKDMAX1 ",             reg_pair),
        (" FSKDMAX0 ",             reg_pair),
        (" FSKDMIN1 ",             reg_pair),
        (" FSKDMIN0 ",             reg_pair),
        (" PKTADDRCFG ",             reg_pair),
        (" TMGRXRSSI ",             reg_pair),
        (" RSSIABSTHR ",             reg_pair),
        (" BGNDRSSITHR ",             reg_pair),    
        (" DACVALUE1 ",             reg_pair),
        (" DACVALUE0 ",             reg_pair),
        (" DACCONFIG ",             reg_pair),   
        (" MODCFGP ",             reg_pair), 
        (" FREQB0 ",             reg_pair),
        (" FREQB1 ",             reg_pair),
        (" FREQB2 ",             reg_pair),
        (" FREQB3 ",             reg_pair),
        (" IRQMASK0 ",             reg_pair),
        (" CRCINIT3 ",             reg_pair),
        (" CRCINIT2 ",             reg_pair),
        (" CRCINIT1 ",             reg_pair),
        (" CRCINIT0 ",             reg_pair),
        (" FEC ",             reg_pair),
        (" FECSYNC ",             reg_pair),
        (" PINFUNCIRQ ",             reg_pair),
        (" PWRAMP ",             reg_pair),
        (" FIFOSTAT ",             reg_pair),
        (" FIFOTHRESH1 ",             reg_pair),
        (" FIFOTHRESH0 ",             reg_pair),
        (" PLLLOOPBOOST ",             reg_pair),
        (" PLLCPIBOOST ",             reg_pair),
        (" PLLRANGINGA ",             reg_pair),
        (" PLLRANGINGB ",             reg_pair),
        (" BGNDRSSI ",             reg_pair),
        (" DIVERSITY ",             reg_pair),
        (" WAKEUP1 ",             reg_pair),    
        (" WAKEUP0 ",             reg_pair),
        (" WAKEUPFREQ1 ",             reg_pair),
        (" WAKEUPFREQ0 ",             reg_pair),
        (" AFSKSPACE1 ",             reg_pair),
        (" AFSKSPACE0 ",             reg_pair),
        (" AFSKMARK1 ",             reg_pair),
        (" AFSKMARK0 ",             reg_pair),
        (" AFSKCTRL ",             reg_pair),
        (" FREQUENCYLEAK ",             reg_pair),
        (" AGCGAIN2 ",             reg_pair),
        (" AGCTARGET2 ",             reg_pair),
        (" AGCAHYST0 ",             reg_pair),
        (" AGCAHYST2 ",             reg_pair),    
        (" AGCMINMAX0 ",             reg_pair),
        (" AGCMINMAX2 ",             reg_pair), 
        (" TIMEGAIN2 ",             reg_pair),
        (" DRGAIN2 ",             reg_pair),
        (" PHASEGAIN2 ",             reg_pair),
        (" FREQUENCYGAINA2 ",             reg_pair),
        (" FREQUENCYGAINB2 ",             reg_pair),
        (" FREQUENCYGAINC2 ",             reg_pair),
        (" FREQUENCYGAIND2 ",             reg_pair),    
        (" AMPLITUDEGAIN2 ",             reg_pair),
        (" FREQDEV12 ",             reg_pair),
        (" FREQDEV02 ",             reg_pair),
        (" FOURFSK0 ",             reg_pair),
        (" FOURFSK2 ",             reg_pair),
        (" BBOFFSRES2 ",             reg_pair),
        (" TXPWRCOEFFA1 ",             reg_pair),
        (" TXPWRCOEFFA0 ",             reg_pair), 	
        (" TXPWRCOEFFC1 ",             reg_pair),
        (" TXPWRCOEFFC0 ",             reg_pair), 	
        (" TXPWRCOEFFD1 ",             reg_pair),
        (" TXPWRCOEFFD0 ",             reg_pair), 	
        (" TXPWRCOEFFE1 ",             reg_pair),
        (" TXPWRCOEFFE0 ",             reg_pair), 	
        (" PLLLOCKDET ",             reg_pair),
        (" PKTADDR3 ",             reg_pair),
        (" PKTADDR2 ",             reg_pair),
        (" PKTADDR1 ",             reg_pair),
        (" PKTADDR0 ",             reg_pair),
        (" PKTADDRMASK3 ",             reg_pair),
        (" PKTADDRMASK2 ",             reg_pair),
        (" PKTADDRMASK1 ",             reg_pair),
        (" PKTADDRMASK0 ",             reg_pair),
        (" MATCH0MIN ",             reg_pair),
        (" MATCH1MIN ",             reg_pair),  
        (" TMGRXPREAMBLE3 ",             reg_pair),
        (" BGNDRSSIGAIN ",             reg_pair),
        (" GPADCCTRL ",             reg_pair),
        (" GPADCPERIOD ",             reg_pair),
        (" LPOSCCONFIG ",             reg_pair),
        (" LPOSCKFILT1 ",             reg_pair),
        (" LPOSCKFILT0 ",             reg_pair),
        (" LPOSCREF1 ",             reg_pair),
        (" LPOSCREF0 ",             reg_pair),
        (" LPOSCFREQ1 ",             reg_pair),
        (" LPOSCFREQ0 ",             reg_pair), 
        (" POWCTRL1 ",             reg_pair),   
        (" TUNE_F0C ",             reg_pair),
        (" TUNE_F0D ",             reg_pair),    
        (" TUNE_F10 ",             reg_pair),
        (" TUNE_F11 ",             reg_pair),
        (" TUNE_F72 ",             reg_pair),  
    ]

#C file translation
psk125_reg_settings = radio_settings(
reg_pair(AX_REG_MODULATION, 0x04),
reg_pair(AX_REG_ENCODING, 0x02),
reg_pair(AX_REG_FRAMING, 0x06),
reg_pair(AX_REG_PINFUNCSYSCLK, 0x01),
reg_pair(AX_REG_IFFREQ1, 0x00),
reg_pair(AX_REG_IFFREQ0, 0x89),
reg_pair(AX_REG_DECIMATION, 0x3C),
reg_pair(AX_REG_RXDATARATE2, 0x00),
reg_pair(AX_REG_RXDATARATE1, 0x28),
reg_pair(AX_REG_RXDATARATE0, 0x00),
reg_pair(AX_REG_MAXDROFFSET2, 0x00),
reg_pair(AX_REG_MAXDROFFSET1, 0x00),
reg_pair(AX_REG_MAXDROFFSET0, 0x00),
reg_pair(AX_REG_MAXRFOFFSET2, 0x80),
reg_pair(AX_REG_MAXRFOFFSET1, 0x00),
reg_pair(AX_REG_MAXRFOFFSET0, 0x00),
reg_pair(AX_REG_AMPLFILTER, 0x00),
reg_pair(AX_REG_RXPARAMSETS, 0xF4),
reg_pair(AX_REG_AGCGAIN0, 0xD6),
reg_pair(AX_REG_AGCTARGET0, 0x84),
reg_pair(AX_REG_AGCGAIN2, 0xA8),
reg_pair(AX_REG_TIMEGAIN0,          0xA8),#Timing Gain
reg_pair(AX_REG_DRGAIN0,            0xA2),#Data Rate Gain
reg_pair(AX_REG_PHASEGAIN0,         0xC3),#Filter Index, Phase Gain
reg_pair(AX_REG_FREQUENCYGAINA0,	0x46),#Frequency Gain A
reg_pair(AX_REG_FREQUENCYGAINB0,	0x0A),#Frequency Gain B
reg_pair(AX_REG_FREQUENCYGAINC0,	0x1F),#Frequency Gain C
reg_pair(AX_REG_FREQUENCYGAIND0,	0x1F),#Frequency Gain D
reg_pair(AX_REG_AMPLITUDEGAIN0,     0x06),#Amplitude Gain
reg_pair(AX_REG_FREQDEV10,          0x00),#Receiver Frequency Deviation
reg_pair(AX_REG_FREQDEV00,          0x00),#Receiver Frequency Deviation
reg_pair(AX_REG_BBOFFSRES0,         0x00),#Baseband Offset Compensation Resistors
reg_pair(AX_REG_AGCGAIN1,           0xD6),#AGC Speed
reg_pair(AX_REG_AGCTARGET1,         0x84),#AGC Target
reg_pair(AX_REG_AGCAHYST1,          0x00),#AGC Digital Threshold Range
reg_pair(AX_REG_AGCMINMAX1,         0x00),#AGC Digital Minimum/Maximum Set Points
reg_pair(AX_REG_TIMEGAIN1,          0xA6),#Timing Gain
reg_pair(AX_REG_DRGAIN1,            0xA1),#Data Rate Gain
reg_pair(AX_REG_PHASEGAIN1,         0xC3),#Filter Index, Phase Gain
reg_pair(AX_REG_FREQUENCYGAINA1,    0x46),#Frequency Gain A
reg_pair(AX_REG_FREQUENCYGAINB1,	0x0A),#Frequency Gain B
reg_pair(AX_REG_FREQUENCYGAINC1,	0x1F),#Frequency Gain C
reg_pair(AX_REG_FREQUENCYGAIND1,	0x1F),#Frequency Gain D
reg_pair(AX_REG_AMPLITUDEGAIN1,	    0x06),#Amplitude Gain
reg_pair(AX_REG_FREQDEV11,	        0x00),#Rx freq deviation
reg_pair(AX_REG_FREQDEV01,	        0x00),#Rx freq deviation
reg_pair(AX_REG_BBOFFSRES1,	        0x00),#BB offset compensation resistors
reg_pair(AX_REG_AGCGAIN3,           0xFF),#AGC Speed
reg_pair(AX_REG_AGCTARGET3,         0x84),#AGC Target
reg_pair(AX_REG_AGCAHYST3,          0x00),#AGC Digital Threshold Range
reg_pair(AX_REG_AGCMINMAX3,         0x00),#AGC Digital Minimum/Maximum Set Points
reg_pair(AX_REG_TIMEGAIN3,          0xA5),#Timing Gain
reg_pair(AX_REG_DRGAIN3,            0xA0),#Data Rate Gain
reg_pair(AX_REG_PHASEGAIN3,         0xC3),#Filter Index, Phase Gain
reg_pair(AX_REG_FREQUENCYGAINA3,    0x46),#Frequency Gain A
reg_pair(AX_REG_FREQUENCYGAINB3,	0x0A),#Frequency Gain B
reg_pair(AX_REG_FREQUENCYGAINC3,	0x1F),#Frequency Gain C
reg_pair(AX_REG_FREQUENCYGAIND3,	0x1F),#Frequency Gain D
reg_pair(AX_REG_AMPLITUDEGAIN3,	    0x06),#Amplitude Gain
reg_pair(AX_REG_FREQDEV13,	        0x00),#Rx freq deviation
reg_pair(AX_REG_FREQDEV03,	        0x00),#Rx freq deviation
reg_pair(AX_REG_FOURFSK3,	        0x16),#Four FSK control
reg_pair(AX_REG_BBOFFSRES3,	        0x00),#BB offset compensation resistors
reg_pair(AX_REG_MODCFGF,	        0x00),#Freq shaping mode
reg_pair(AX_REG_FSKDEV1,	        0x00),#FSK freq deviation
reg_pair(AX_REG_FSKDEV0,	        0x00),#FSK freq deviation
reg_pair(AX_REG_MODCFGA,	        0x06),#Amplitude shaping mode
reg_pair(AX_REG_TXRATE2,	        0x00),#TX bitrate
reg_pair(AX_REG_TXRATE1,	        0x06),#TX bitrate
reg_pair(AX_REG_TXRATE0,	        0xD4),#TX bitrate
reg_pair(AX_REG_TXPWRCOEFFB1,	    0x02),#TX predistortion
reg_pair(AX_REG_TXPWRCOEFFB0,	    0x07),#TX predistortion
reg_pair(AX_REG_PLLVCOI,	        0x99),#PLL parameters
reg_pair(AX_REG_PLLRNGCLK,	        0x05),#PLL parameters
reg_pair(AX_REG_BBTUNE,	            0x0F),#Baseband tuning
reg_pair(AX_REG_BBOFFSCAP,	        0x77),#Baseband gain offset compensation
reg_pair(AX_REG_TMGTXBOOST,         0x5B),#Boost time
reg_pair(AX_REG_TMGTXSETTLE,	    0x3E),#Settling time
reg_pair(AX_REG_TMGRXBOOST,         0x5B),#Boost time
reg_pair(AX_REG_TMGRXSETTLE,	    0x3E),#Settling time
reg_pair(AX_REG_TMGRXOFFSACQ,	    0x00),#Baseband offset acq
reg_pair(AX_REG_TMGRXCOARSEAGC,	    0x9C),#Coarse AGC time
reg_pair(AX_REG_TMGRXPREAMBLE2,	    0x35),#Preamble 2 timeout
reg_pair(AX_REG_PKTCHUNKSIZE,	    0x0D),#Packet chunk size
reg_pair(AX_REG_PKTACCEPTFLAGS,	    0x1C),#Packet ctrl accept flags
reg_pair(AX_REG_REF,	            0x03),
reg_pair(AX_REG_XTALOSC,	        0x04),
reg_pair(AX_REG_XTALAMPL,	        0x00),
reg_pair(AX_REG_TUNE_F1C,	        0x07),#Tuning registers
reg_pair(AX_REG_TUNE_F21,	        0x68),#Tuning registers
reg_pair(AX_REG_TUNE_F22,	        0xFF),#Tuning registers
reg_pair(AX_REG_TUNE_F23,	        0x84),#Tuning registers
reg_pair(AX_REG_TUNE_F26,	        0x98),#Tuning registers
reg_pair(AX_REG_TUNE_F34,	        0x28),#Tuning registers
reg_pair(AX_REG_TUNE_F35,	        0x11),#Tuning registers
reg_pair(AX_REG_TUNE_F44,	        0x25),#Tuning registers
#
reg_pair(AX_REG_PLLLOOP,           0x0B),
reg_pair(AX_REG_PLLCPI,            0x10),
reg_pair(AX_REG_PLLVCODIV,         0x25),
reg_pair(AX_REG_XTALCAP,           0x00),
reg_pair(AX_REG_TUNE_F00,          0x0F),
reg_pair(AX_REG_TUNE_F18,          0x02),
#
reg_pair(AX_REG_TMGRXAGC,           0x00),#Receiver AGC settling time
reg_pair(AX_REG_TMGRXPREAMBLE1,     0x00),#Receiver preamble 1 timeout
reg_pair(AX_REG_PKTMISCFLAGS,       0x00),#Packet misc flags
#
reg_pair(AX_REG_FREQA0,	            0xAB),#Output Frequency
reg_pair(AX_REG_FREQA1,	            0xAA),#Output Frequency
reg_pair(AX_REG_FREQA2,	            0x1A),#Output Frequency
reg_pair(AX_REG_FREQA3,	            0x09),#Output Frequency
#
reg_pair(AX_REG_RSSIREFERENCE,      0x00),#RSSI offset
#
reg_pair(AX_REG_MATCH0PAT3,	        0xAA),#Pattern match
reg_pair(AX_REG_MATCH0PAT2,	        0xCC),#Pattern match
reg_pair(AX_REG_MATCH0PAT1,	        0xAA),#Pattern match
reg_pair(AX_REG_MATCH0PAT0,	        0xCC),#Pattern match
reg_pair(AX_REG_MATCH0LEN,	        0x9F),#Pattern length
reg_pair(AX_REG_MATCH0MAX,	        0x1F),#Max match
#
reg_pair(AX_REG_MATCH1PAT1,	        0x55),#Pattern match
reg_pair(AX_REG_MATCH1PAT0,	        0x55),#Pattern match
reg_pair(AX_REG_MATCH1LEN,	        0x8A),#Pattern length
reg_pair(AX_REG_MATCH1MAX,	        0x0A),#Max match
reg_pair(AX_REG_PKTLENCFG,	        0x00),#Packet length config
reg_pair(AX_REG_PKTLENOFFSET,	    0x03),#Packet length offset
reg_pair(AX_REG_PKTMAXLEN,	        0xC8),#Packet max length
reg_pair(AX_REG_PKTSTOREFLAGS,      0x14),#Packet store flags
# Additional registers
reg_pair(AX_REG_PINFUNCDCLK,        0x01),#Output 1
reg_pair(AX_REG_PINFUNCDATA,        0x01),#Output 1
reg_pair(AX_REG_PINFUNCANTSEL,      0x01),#Output 1
reg_pair(AX_REG_PINFUNCPWRAMP,      0x07),#Output Power Amp control
reg_pair(AX_REG_WAKEUPXOEARLY,      0x01),#Nb of LPOSC cycles by which the XTAL Osc is woken up before the receiver
reg_pair(AX_REG_FSKDMAX1,           0x00),#FSK-4 stuff
reg_pair(AX_REG_FSKDMAX0,           0xA6),#    ...
reg_pair(AX_REG_FSKDMIN1,           0xFF),#    ...
reg_pair(AX_REG_FSKDMIN0,           0x5A),#    ...
reg_pair(AX_REG_PKTADDRCFG,	        0x80),#Packet addr config
reg_pair(AX_REG_TMGRXRSSI,	        0x03),#RSSI settling time
reg_pair(AX_REG_RSSIABSTHR,	        0xDD),#RSSI abs. threshold
reg_pair(AX_REG_BGNDRSSITHR,        0x00),#Background RSSI rel. threshold
reg_pair(AX_REG_DACVALUE1,	        0x00),#DAC value
reg_pair(AX_REG_DACVALUE0,	        0x00),#DAC value
reg_pair(AX_REG_DACCONFIG,	        0x00),#DAC config
reg_pair(AX_REG_MODCFGP,	        0xE1),
reg_pair(AX_REG_FREQB0,	            0xAB),#Output Frequency
reg_pair(AX_REG_FREQB1,	            0xAA),#Output Frequency
reg_pair(AX_REG_FREQB2,	            0x1A),#Output Frequency
reg_pair(AX_REG_FREQB3,	            0x09),#Output Frequency
reg_pair(AX_REG_IRQMASK0,           0x00),#Enable interrupts
reg_pair(AX_REG_CRCINIT3,	        0xFF),#CRC Reset value
reg_pair(AX_REG_CRCINIT2,	        0xFF),#CRC Reset value
reg_pair(AX_REG_CRCINIT1,	        0xFF),#CRC Reset value
reg_pair(AX_REG_CRCINIT0,	        0xFF),#CRC Reset value
reg_pair(AX_REG_FEC,	            0x00),#FEC
reg_pair(AX_REG_FECSYNC,	        0x62),#Interleaver Synch Threshold
reg_pair(AX_REG_PINFUNCIRQ,	        0x03),#IRQ behaviour
reg_pair(AX_REG_PWRAMP,	            0x00),#Ext Power Amp control
reg_pair(AX_REG_FIFOSTAT,	        0x03),#FIFO information
reg_pair(AX_REG_FIFOTHRESH1,	    0x00),#FIFO Threshold
reg_pair(AX_REG_FIFOTHRESH0,	    0x00),#FIFO Threshold
reg_pair(AX_REG_PLLLOOPBOOST,     	0x0B),#PLL Loop Filter Settings
reg_pair(AX_REG_PLLCPIBOOST,  	    0xC8),#PLL Charge pump current
reg_pair(AX_REG_PLLRANGINGA,  	    0x04),#PLL Autoranging
reg_pair(AX_REG_PLLRANGINGB,  	    0x04),#PLL Autoranging
reg_pair(AX_REG_BGNDRSSI,  	        0x00),#Background RSSI
reg_pair(AX_REG_DIVERSITY,  	    0x00),#Antenna diversity enable
reg_pair(AX_REG_WAKEUP1,  	        0x00),#Wake-up Timer
reg_pair(AX_REG_WAKEUP0,  	        0x00),#Wake-up Timer
reg_pair(AX_REG_WAKEUPFREQ1,        0x00),#Wake-up Freq
reg_pair(AX_REG_WAKEUPFREQ0,        0x00),#Wake-up Freq
reg_pair(AX_REG_AFSKSPACE1,         0x00),#AFSK Space Freq
reg_pair(AX_REG_AFSKSPACE0,         0x40),#AFSK Space Freq
reg_pair(AX_REG_AFSKMARK1,          0x00),#AFSK Mark Freq
reg_pair(AX_REG_AFSKMARK0,          0x75),#AFSK Mark Freq
reg_pair(AX_REG_AFSKCTRL,           0x04),#AFSK Detector BW
reg_pair(AX_REG_FREQUENCYLEAK,      0x00),#Leakiness of BB Freq Recovery Loop
reg_pair(AX_REG_AGCGAIN2,           0xFF),#AGC Gain reduction/increase speed
reg_pair(AX_REG_AGCTARGET2,         0x84),#AGC output average magnitude
reg_pair(AX_REG_AGCAHYST0,          0x00),#Digital threshold range
reg_pair(AX_REG_AGCAHYST2,          0x00),#Digital threshold range
reg_pair(AX_REG_AGCMINMAX0,         0x00),#AGC attenuation max
reg_pair(AX_REG_AGCMINMAX2,         0x00),#AGC attenuation max
reg_pair(AX_REG_TIMEGAIN2,          0xA5),#Gain of timing recovery loop
reg_pair(AX_REG_DRGAIN2,            0xA0),#Gain of datarate recovery loop
reg_pair(AX_REG_FREQUENCYGAINA2,    0x46),#Gain of BB freq recovery loop
reg_pair(AX_REG_FREQUENCYGAINB2,    0x0A),#Gain of BB freq recovery loop
reg_pair(AX_REG_FREQUENCYGAINC2,    0x1F),#Gain of BB freq recovery loop
reg_pair(AX_REG_FREQUENCYGAIND2,    0x1F),#Gain of BB freq recovery loop
reg_pair(AX_REG_AMPLITUDEGAIN2,     0x06),#Gain of Amplitude recovery loop
reg_pair(AX_REG_FREQDEV12,          0x00),#Rx Freq deviation
reg_pair(AX_REG_FREQDEV02,          0x00),#Rx Freq deviation
reg_pair(AX_REG_FOURFSK0,           0x16),#Deviation decay
reg_pair(AX_REG_FOURFSK2,           0x16),#Deviation decay
reg_pair(AX_REG_BBOFFSRES2,         0x00),#BB Gain Block offset compensation resistors
reg_pair(AX_REG_TXPWRCOEFFA1,       0x00),#Transmit predistortion A coefficient
reg_pair(AX_REG_TXPWRCOEFFA0,       0x00),#Transmit predistortion A coefficient
reg_pair(AX_REG_TXPWRCOEFFC1,       0x00),#Transmit predistortion C coefficient
reg_pair(AX_REG_TXPWRCOEFFC0,       0x00),#Transmit predistortion C coefficient
reg_pair(AX_REG_TXPWRCOEFFD1,       0x00),#Transmit predistortion D coefficient
reg_pair(AX_REG_TXPWRCOEFFD0,       0x00),#Transmit predistortion D coefficient
reg_pair(AX_REG_TXPWRCOEFFE1,       0x00),#Transmit predistortion E coefficient
reg_pair(AX_REG_TXPWRCOEFFE0,       0x00),#Transmit predistortion E coefficient
reg_pair(AX_REG_PLLLOCKDET,         0x03),#PLL Lock detector delay
reg_pair(AX_REG_PKTADDR3,           0x00),#Packet Address
reg_pair(AX_REG_PKTADDR2,           0x00),#Packet Address
reg_pair(AX_REG_PKTADDR1,           0x34),#Packet Address
reg_pair(AX_REG_PKTADDR0,           0x33),#Packet Address
reg_pair(AX_REG_PKTADDRMASK3,       0x00),#Packet Address
reg_pair(AX_REG_PKTADDRMASK2,       0x00),#Packet Address
reg_pair(AX_REG_PKTADDRMASK1,       0x00),#Packet Address
reg_pair(AX_REG_PKTADDRMASK0,       0x00),#Packet Address
reg_pair(AX_REG_MATCH0MIN,          0x00),#Min Number of position for match signalling
reg_pair(AX_REG_MATCH1MIN,          0x00),#Min Number of position for match signalling
reg_pair(AX_REG_TMGRXPREAMBLE3,     0x00),#Receiver preamble 3 timeout
reg_pair(AX_REG_BGNDRSSIGAIN,       0x00),#Background RSSI avaeraging Time Constant
reg_pair(AX_REG_GPADCCTRL,          0x00),#General puropse ADC control
reg_pair(AX_REG_GPADCPERIOD,        0x3F),#GPADC sampling period
reg_pair(AX_REG_LPOSCCONFIG,        0x00),#Low power oscillator config
reg_pair(AX_REG_LPOSCKFILT1,        0x20),#Low power oscillator calibration filter constant
reg_pair(AX_REG_LPOSCKFILT0,        0xC4),#Low power oscillator calibration filter constant
reg_pair(AX_REG_LPOSCREF1,          0x61),#Low power oscillator Ref Freq divider
reg_pair(AX_REG_LPOSCREF0,          0xA8),#Low power oscillator Ref Freq divider
reg_pair(AX_REG_LPOSCFREQ1,         0x00),#Low power oscillator Freq tune value
reg_pair(AX_REG_LPOSCFREQ0,         0x00),#Low power oscillator Freq tune value
reg_pair(AX_REG_POWCTRL1,           0x04),#Low power oscillator Freq tune value
reg_pair(AX_REG_TUNE_F0C,	        0x00),#Tuning registers
reg_pair(AX_REG_TUNE_F0D,	        0x03),#Tuning registers
reg_pair(AX_REG_TUNE_F10,	        0x04),#Tuning registers
reg_pair(AX_REG_TUNE_F11,	        0x00),#Tuning registers
reg_pair(AX_REG_TUNE_F72,	        0x00),#Tuning registers
)

def ax5043_readAllReg():
    #get pointer to reg pair object
    #get size of reg, ie: size of the struct/size of a reg pair
    #increment through and read
    
    SettingsPointer = pointer(reg_pair())
    
    TempPointer = pointer(psk125_reg_settings())
    
    reg_size = sizeof(TempPointer)/sizeof(SettingsPointer)
    
    for i in range(0, reg_size):
        data = ax5043_readReg(SettingsPointer.addr)
        SettingsPointer = SettingsPointer + 1
    
    return

def ax5043_writeAllReg():
    
    SettingsPointer = pointer(reg_pair())
    
    TempPointer = pointer(psk125_reg_settings())
    
    reg_size = sizeof(TempPointer)/sizeof(SettingsPointer)
    
    for i in range(0, reg_size):
        ax5043_writeReg(SettingsPointer.addr, SettingsPointer.data)
        SettingsPointer = SettingsPointer + 1
    
    return

def ax5043_writeReg(addr, value):
    data = np.array([0,0])
    longData = np.array([0,0,0])
    
    if (addr < 0x70):
        data[0] = addr | 0x80
        data[1] = value
        #write SPI
    else:
        longData[0] = (addr >> 8) | 0xF0
        longData[1] = addr & 0xFF
        longData[2] = value
    return

def ax5043_readReg(addr):
    data = np.array([0,0])
    longData = np.array([0,0,0])
    
    if (addr < 0x70):
        data[0] = addr & 0x80
        data[1] = value
        
        #write SPI
        time.sleep(5)
        return data[1]
    else:
        longData[0] = (addr >> 8) | 0xF0
        longData[1] = addr & 0xFF
        longData[2] = 0
        
        #write SPI
        time.sleep(5)
        return longData[2]
        
    return

def ax5043_TX():
    
    transmitted = 0
    for k in range(0,100):
        #According to Errata for Silicon v51
        #turn off receiver
        ax5043_writeReg(AX_REG_PWRMODE, PWRMODE_STANDBY)
        time.sleep(100)
        ax5043_writeReg(AX_REG_PWRMODE, PWRMODE_FIFOON)
        time.sleep(100)
        
        #Set freqA and tune for TX
        ax5043_set_reg_tx()
        
        #Clear FIFO data and flags
        ax5043_writeReg(AX_REG_FIFOSTAT, 0x03)
        
        #FULL TX MODE
        ax5043_writeReg(AX_REG_PWRMODE, PWRMODE_FULLTX)
        time.sleep(100)
        
        #write Preamble
        ax5043_writePreamble()
        #write Packet
        ax5043_writePacket
        
        reg = 0x00
        while (reg != 0x01):
            reg = ax5043_readReg(AX_REG_XTALSTATUS)
            time.sleep()
        
        #commit FIFO
        ax5043_writeReg(AX_REG_FIFOSTAT, 0x04)
        
        #printf
        time.sleep(100)
        
        reg = 0x01
        while (reg != 0x00):
            reg = ax5043_readReg(AX_REG_RADIOSTATE)
            time.sleep(100)
        
        #printf
        ax5043_writeReg(AX_REG_PWRMODE, PWRMODE_POWERDOWN)
        time.sleep(2000000)
    
    return

def ax5043_writePreamble():
    
    #code blocks example
    ax5043_writeReg(AX_REG_FIFODATA, 0x62)
    ax5043_writeReg(AX_REG_FIFODATA, 0x38)
    ax5043_writeReg(AX_REG_FIFODATA, 0x20)
    ax5043_writeReg(AX_REG_FIFODATA, 0xAA)
    
    return

def ax5043_writePacket():
    
    #long sync
    ax5043_writePacket(AX_REG_FIFODATA, 0xA1)
    ax5043_writePacket(AX_REG_FIFODATA, 0x38)
    ax5043_writePacket(AX_REG_FIFODATA, 0x33)
    ax5043_writePacket(AX_REG_FIFODATA, 0x55)
    ax5043_writePacket(AX_REG_FIFODATA, 0x33)
    ax5043_writePacket(AX_REG_FIFODATA, 0x55)
    
    ax5043_writePacket(AX_REG_FIFODATA, 0xE1)
    ax5043_writePacket(AX_REG_FIFODATA, 0x04)
    ax5043_writePacket(AX_REG_FIFODATA, 0x13)
    
    ax5043_writePacket(AX_REG_FIFODATA, 0x31)
    ax5043_writePacket(AX_REG_FIFODATA, 0x32)
    ax5043_writePacket(AX_REG_FIFODATA, 0x33)
    
    return

def ax5043_init():
    
    #set_registers
    ax5043_writeAllReg();
    
    #Set freqA and tune for TX
    ax5043_set_reg_tx();
    
    #set datarate...
    ax5043_set_datarate();

    #Perform autoranging
    ax5043_autoranging();
    
    return

def ax5043_autoranging():
    
    ax5043_writeReg(AX_REG_PWRMODE, PWRMODE_POWERDOWN)
    time.sleep(10)
    #turn XTAL ON..power in standy-by
    ax5043_writeReg(AX_REG_PWRMODE, PWRMODE_STANDBY)
    
    #wait till Xtal is running
    reg = 0x00
    while(reg != 0x01):
        reg = ax5043_readReg(AX_REG_XTALSTATUS)
        #fprintf
        time.sleep(10)
    
    #start autoranging (set RNGSTART) w/ VCO ranging at 8 (to be tuned)
    #fprintf
    ax5043_writeReg(AX_REG_PLLRANGINGA, 0x18)
    
    reg = 0x10
    while (reg & 0x10):
        reg = ax5043_readReg(AX_REG_PLLRANGINGA)
        #fprintf
        time.sleep(10)
    
    #powerdown
    ax5043_writeReg(AX_REG_PWRMODE, PWRMODE_POWERDOWN)
    
    return

def ax5043_set_reg_tx():
    
    ax5043_writeReg(AX_REG_PLLVCOI,0x98)
    ax5043_writeReg(AX_REG_PLLLOOP,0x0B)#500kHz & Use FreqA...
    x5043_writeReg(AX_REG_PLLCPI,0x10)#0x08
    ax5043_writeReg(AX_REG_PLLVCODIV,0x24)
    ax5043_writeReg(AX_REG_XTALCAP,0x00)
    ax5043_writeReg(AX_REG_TUNE_F00,0x0F)
    ax5043_writeReg(AX_REG_TUNE_F18,0x06)
    
    return

def ax5043_set_reg_rx():
    
    ax5043_writeReg(AX_REG_PLLVCOI,0x99)
    ax5043_writeReg(AX_REG_PLLLOOP,0x0B)#500kHz; 0x09...100kHz BW for ranging
    ax5043_writeReg(AX_REG_PLLCPI,0x10)#0x08
    ax5043_writeReg(AX_REG_PLLVCODIV,0x25)#fPD = fXTAL/2
    ax5043_writeReg(AX_REG_XTALCAP,0x00)#0 - TCXO
    ax5043_writeReg(AX_REG_TUNE_F00,0x0F)
    ax5043_writeReg(AX_REG_TUNE_F18,0x02)
    
    return

def ax5043_set_datarate():
    
    ax5043_writeReg(AX_REG_IFFREQ1,0x01)
    ax5043_writeReg(AX_REG_IFFREQ0,0x11)
    ax5043_writeReg(AX_REG_DECIMATION,0x7F)
    ax5043_writeReg(AX_REG_RXDATARATE2,0x00) 
    ax5043_writeReg(AX_REG_RXDATARATE1,0xBC)
    ax5043_writeReg(AX_REG_RXDATARATE0,0xF9)
    ax5043_writeReg(AX_REG_AGCGAIN0,0xE9)
    ax5043_writeReg(AX_REG_TIMEGAIN0,0xBA)
    ax5043_writeReg(AX_REG_DRGAIN0,0xB4)
    ax5043_writeReg(AX_REG_PHASEGAIN0,0x03)
    ax5043_writeReg(AX_REG_AGCGAIN1,0xE9)
    ax5043_writeReg(AX_REG_TIMEGAIN1,0xB8)
    ax5043_writeReg(AX_REG_DRGAIN1,0xB3)
    ax5043_writeReg(AX_REG_PHASEGAIN1,0x03)
    ax5043_writeReg(AX_REG_TIMEGAIN3,0xB7)
    ax5043_writeReg(AX_REG_DRGAIN3,0xB2)
    ax5043_writeReg(AX_REG_PHASEGAIN3,0x03)
    ax5043_writeReg(AX_REG_TXRATE2,0x00)
    ax5043_writeReg(AX_REG_TXRATE1,0x00)
    ax5043_writeReg(AX_REG_TXRATE0,0x57)
    ax5043_writeReg(AX_REG_TUNE_F35,0x12)
    ax5043_writeReg(AX_REG_AGCGAIN3,0xE9)
    
    return

def ax5043_RX():
    
    received = 0
    for k in range(0,100):
        ax5043_writeReg(AX_REG_FIFOSTAT, 0x03)
        
        time.sleep(10)
        
        prev_rstat = ax5043_readReg(AX_REG_RADIOSTATE)
        prev_fstat = ax5043_readReg(AX_REG_FIFOSTAT)
        
        ax5043_writeReg(AX_REG_PWRMODE, PWRMODE_FULLRX)
        
        #printf
        rstat = prev_rstat
        fstat = prev_fstat
        
        while (rstat != 0x0F):
            rstat = ax5043_readReg(AX_REG_RADIOSTATE)
        
        time.sleep(1000000)
        
        fif0 = ax5043_readReg(AX_REG_FIFOCOUNT0)
        fif1 = ax5043_readReg(AX_REG_FIFOCOUNT1)
        FIFObytes = (fif1 << 8) | fifo
        
        received = received + 1
        #printf
        for i in range(0, FIFObytes):
            reg = ax5043_readReg(AX_REG_FIFODATA)
            #printf
        
        #printf
        ax5043_writeReg(AX_REG_PWRMODE, PWRMODE_POWERDOWN)
    
    return

def radioConfig():
    fp = open('/home/pi/AX5043/Test/AX5043_PSK/log.txt','w')
    
    #check for error
    
    status = ax5043_readReg(AX_REG_PWRMODE)
    version = ax5043_readReg(AX_REG_SILICONREVISION)
    state = ax5043_readReg(AX_REG_RADIOSTATE)
    
    #turn off receiver
    ax5043_writeReg(AX_REG_PWRMODE,PWRMODE_STANDBY)
    time.sleep(100)
    
    #release FIFO ports
    ax5043_writeReg(AX_REG_PWRMODE,PWRMODE_FIFOON)
    time.sleep(100)
    
    #Init transceiver
    ax5043_init()
    
    ax5043_RX()
    
    fp.close()
    