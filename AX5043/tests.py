import transmission

DEVICE = 0

radio = AX5043()


######### Test 1 : Marco Polo System ######

#Send Marco
if DEVICE == 0:
	radio.transmit("Marco")
	data = radio.receive()
	while len(data < 0):
		data = radio.receive()
	print(data)

# Read Marco and Send Polo
else:
	data = radio.receive()
	while len(data < 0):
		data = radio.receive()

	print(data)
	if(data == "Marco")
		radio.transmit("Marco")


######### Test 2 : Scheduled Commands ######
