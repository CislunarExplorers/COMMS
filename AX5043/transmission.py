import _ax5043
import time
from registers import Register

usleep = lambda x: time.sleep(x/1000000.0)

class AX5043():

	def __init__(self):
		self.transmitted = 0
		self.received = 0

		print("Initializing the Antenna")

		_ax5043.setup_SPI("./log.txt")

		status = _ax5043.read_reg(Register.AX_REG_PWRMODE.value)
		print("Power mode : {}".format(status))

		version = _ax5043.read_reg(Register.AX_REG_SILICONREVISION.value)
		print("Silicon Revision : {}".format(version))

		state = _ax5043.read_reg(Register.AX_REG_RADIOSTATE.value)
		print("Radio State : {}".format(state))

		# turn off receiver
		_ax5043.write_reg(Register.AX_REG_PWRMODE.value,Register.PWRMODE_STANDBY.value)
		usleep(100)

		# release FIFO ports
		_ax5043.write_reg(Register.AX_REG_PWRMODE.value,Register.PWRMODE_FIFOON.value)
		usleep(100)

		# Init Transceiver
		_ax5043.init()

	def transmit(self, data):
		print("Mode changed to Tranmitting")
		# According to ERRATA for Silicon v51 
		# turn off receiver
		_ax5043.write_reg(Register.AX_REG_PWRMODE.value,Register.PWRMODE_STANDBY.value)
		usleep(100)
		# release FIFO ports
		_ax5043.write_reg(Register.AX_REG_PWRMODE.value,Register.PWRMODE_FIFOON.value)
		usleep(100)

		# Set freqA and tune for TX
		self.set_reg_tx()

		# Clear FIFO data and flags
		_ax5043.write_reg(Register.AX_REG_FIFOSTAT.value,0x03)

		# FULL TX Mode
		_ax5043.write_reg(Register.AX_REG_PWRMODE.value,Register.PWRMODE_FULLTX.value)
		usleep(100)

		#_ax5043.write_preamble();
		self.write_preamble()

		# Start Writing 
		self.write_packets(data)

		# Wait till Xtal is running
		reg = _ax5043.read_reg(Register.AX_REG_XTALSTATUS.value)
		usleep(10)
		while (reg != Register.AX_REG_XTALSTATUS_MASK.value):
			reg = _ax5043.read_reg(Register.AX_REG_XTALSTATUS.value)
			usleep(10)
		
		# Commit FIFO
		_ax5043.write_reg(Register.AX_REG_FIFOSTAT.value,0x04)

		print("Transmiting...")
		self.transmitted += 1
		usleep(10)

		# Wait till TX is done
		reg = _ax5043.read_reg(Register.AX_REG_RADIOSTATE.value)
		usleep(10)
		while (reg != 0x00):
			reg = _ax5043.read_reg(Register.AX_REG_RADIOSTATE.value)
			usleep(10)
		
		print("TX done...Packet No : {}".format(self.transmitted))
		
		# Powerdown
		_ax5043.write_reg(Register.AX_REG_PWRMODE.value,Register.PWRMODE_POWERDOWN.value)
		usleep(5000000)

	def receive(self):
		print("Mode changed to Receiving")

		self.set_reg_rx()
		# Clear FIFO data and flags
		_ax5043.write_reg(Register.AX_REG_FIFOSTAT.value,0x03)

		# Set power mode to FULLRX
		_ax5043.write_reg(Register.AX_REG_PWRMODE.value,Register.PWRMODE_FULLRX.value)

		print("Receiving...\n")
		rstat = 0
		while (rstat != Register.AX_REG_RADIOSTATE_RX_MASK.value):
			rstat = _ax5043.read_reg(Register.AX_REG_RADIOSTATE.value)
		
		while (rstat == Register.AX_REG_RADIOSTATE_RX_MASK.value):
			rstat = _ax5043.read_reg(Register.AX_REG_RADIOSTATE.value)
			usleep(100)
		

		fif0 = _ax5043.read_reg(Register.AX_REG_FIFOCOUNT0.value)
		fif1 = _ax5043.read_reg(Register.AX_REG_FIFOCOUNT1.value) 
		FIFObytes = (fif1 << 8) | fif0

		self.received += 1
		print("Received DATA :")
		received_data = self.read_packets(FIFObytes)
		print(received_data)
		
		print(" ... Packet No : {}".format(self.received))
		# Set power mode to POWERDOWN
		_ax5043.write_reg(Register.AX_REG_PWRMODE.value,Register.PWRMODE_POWERDOWN.value)
		return received_data 

	def write_preamble(self):
		_ax5043.write_reg(Register.AX_REG_FIFOSTAT.value,0x62)
		_ax5043.write_reg(Register.AX_REG_FIFOSTAT.value,0x38)
		_ax5043.write_reg(Register.AX_REG_FIFOSTAT.value,0x21)
		_ax5043.write_reg(Register.AX_REG_FIFOSTAT.value,0xAA)

	def set_reg_tx(self):
		_ax5043.write_reg(Register.AX_REG_PLLLOOP.value,0x0B);
		_ax5043.write_reg(Register.AX_REG_PLLCPI.value,0x10);
		_ax5043.write_reg(Register.AX_REG_PLLVCODIV.value,0x24);
		_ax5043.write_reg(Register.AX_REG_XTALCAP.value,0x00);
		_ax5043.write_reg(Register.AX_REG_TUNE_F00.value,0x0F);
		_ax5043.write_reg(Register.AX_REG_TUNE_F18.value,0x06);

	def set_reg_rx(self):
		_ax5043.write_reg(Register.AX_REG_PLLLOOP.value,0x0B);
		_ax5043.write_reg(Register.AX_REG_PLLCPI.value,0x10);
		_ax5043.write_reg(Register.AX_REG_PLLVCODIV.value,0x25);
		_ax5043.write_reg(Register.AX_REG_XTALCAP.value,0x00);
		_ax5043.write_reg(Register.AX_REG_TUNE_F00.value,0x0F);
		_ax5043.write_reg(Register.AX_REG_TUNE_F18.value,0x02);;

	def write_packets(self, data):
		for byte in data:
			hex_byte = ord(byte)
			# print(hex_byte)
			_ax5043.write(hex_byte)

	def read_packets(self, FIFObytes):
		data = ""
		for i in range(FIFObytes):
			reg = _ax5043.read_reg(Register.AX_REG_FIFODATA.value)	
			# print(reg)
			data += chr(reg)
		return data



if __name__ == "__main__":
	radio = AX5043()
	radio.receive()
