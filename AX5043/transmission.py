import _AX5043 as _ax5043
import time

usleep = lambda x: time.sleep(x/1000000.0)

class AX5043():

	def init(self):
		self.transmitted = 0
		self.received = 0

		print("Initializing the Antenna")

		status = _ax5043.read_reg(AX_REG_PWRMODE)
		print("Power mode : {}".format(status))

		version = _ax5043.read_reg(AX_REG_SILICONREVISION)
		print("Silicon Revision : {}".format(version))

		state = _ax5043.read_reg(AX_REG_RADIOSTATE)
		print("Radio State : {}".format(state))

		# turn off receiver
		_ax5043.write_reg(AX_REG_PWRMODE,PWRMODE_STANDBY)
		usleep(100)

		# release FIFO ports
		_ax5043.write_reg(AX_REG_PWRMODE,PWRMODE_FIFOON)
		usleep(100)

		# Init Transceiver
		_ax5043.init()

	def transmit(self, data):
		print("Mode changed to Tranmitting")
		# According to ERRATA for Silicon v51 
		# turn off receiver
		_ax5043.write_reg(AX_REG_PWRMODE,PWRMODE_STANDBY)
		usleep(100)
		# release FIFO ports
		_ax5043.write_reg(AX_REG_PWRMODE,PWRMODE_FIFOON)
		usleep(100)

		# Set freqA and tune for TX
		_ax5043.set_reg_tx()

		# Clear FIFO data and flags
		_ax5043.write_reg(AX_REG_FIFOSTAT,0x03)

		# FULL TX Mode
		_ax5043.write_reg(AX_REG_PWRMODE,PWRMODE_FULLTX)
		usleep(100)

		_ax5043.write_preamble();

		# Start Writing 
		self.write_packets(data)

		# Wait till Xtal is running
		reg = _ax5043.read_reg(AX_REG_XTALSTATUS)
		usleep(10)
		while (reg != AX_REG_XTALSTATUS_MASK):
			reg = _ax5043.read_reg(AX_REG_XTALSTATUS)
			usleep(10)
		
		# Commit FIFO
		_ax5043.write_reg(AX_REG_FIFOSTAT,0x04)

		print("Transmiting...")
		self.transmitted += 1
		usleep(10)

		# Wait till TX is done
		reg = _ax5043.read_reg(AX_REG_RADIOSTATE)
		usleep(10)
		while (reg != 0x00):
			reg = _ax5043.read_reg(AX_REG_RADIOSTATE)
			usleep(10)
		
		print("TX done...Packet No : {}".format(self.transmitted))
		
		# Powerdown
		_ax5043.write_reg(AX_REG_PWRMODE,PWRMODE_POWERDOWN)
		usleep(5000000)

	def receive(self):
		print("Mode changed to Receiving")
		# Clear FIFO data and flags
		_ax5043.write_reg(AX_REG_FIFOSTAT,0x03)

		# Set power mode to FULLRX
		_ax5043.write_reg(AX_REG_PWRMODE,PWRMODE_FULLRX)

		print("Receiving...\n")
		while (rstat != AX_REG_RADIOSTATE_RX_MASK):
			rstat = _ax5043.read_reg(AX_REG_RADIOSTATE)
		
		while (rstat == AX_REG_RADIOSTATE_RX_MASK):
			rstat = _ax5043.read_reg(AX_REG_RADIOSTATE)
			usleep(100)
		

		fif0 = _ax5043.read_reg(AX_REG_FIFOCOUNT0)
		fif1 = _ax5043.read_reg(AX_REG_FIFOCOUNT1) 
		FIFObytes = (fif1 << 8) | fif0

		self.received += 1
		print("Received DATA :")
		received_data = self.read_packets(FIFObytes)
		print(received_data)
		
		print(" ... Packet No : {}".format(self.received))
		# Set power mode to POWERDOWN
		_ax5043.write_reg(AX_REG_PWRMODE,PWRMODE_POWERDOWN)
		return received_data 

	def write_packets(self, data):
		data_byte = bytearray(data)
		for byte in data_byte:
			hex_byte = hex(byte)
			# print(hex_byte)
			_ax5043.write(hex_byte)

	def read_packets(self, FIFObytes):
		data = ""
		for i in range(FIFObytes):
			reg = _ax5043.read_reg(AX_REG_FIFODATA)	
			# print(reg)
			data += chr(reg)
		return data



if __name__ == "__main__":
	radio = AX5043()
	radio.transmit("HelloWorld")
