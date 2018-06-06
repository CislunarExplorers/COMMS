#ifndef SERIAL_BUFFER_H_INCLUDED
#define SERIAL_BUFFER_H_INCLUDED

#include <libmftypes.h>

#define RX_BUFFER_SIZE 100
#define TX_BUFFER_SIZE 100

extern __xdata uint8_t rx_buffer[RX_BUFFER_SIZE];
extern __xdata uint8_t rx_buffer_len;

extern __xdata uint8_t tx_buffer[TX_BUFFER_SIZE];
extern __xdata uint8_t tx_buffer_len;

#endif /* end of include guard: SERIAL_BUFFER_H_INCLUDED */
