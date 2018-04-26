#include "serial_buffer.h"

#define PACKET_SOF_MARKER   0x16 // ASCII SYN and one of the least likely symbols to received when sending random data at random baudrate
//#define PACKET_EOF_MARKER   0xAA // TODO: we don't really need this, do we?

__xdata uint8_t rx_buffer[RX_BUFFER_SIZE];
__xdata uint8_t rx_buffer_len = 0;

__xdata uint8_t tx_buffer[TX_BUFFER_SIZE];
__xdata uint8_t tx_buffer_len = 0;
