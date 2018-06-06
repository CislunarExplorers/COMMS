#ifndef PROTOCOL_BINARY_H_INCLUDED
#define PROTOCOL_BINARY_H_INCLUDED

#include <libmfcrc.h>
#include <libmfwtimer.h>

#include "common/misc.h"
#include "common/dbghelpers.h"
#include "code/wmbus.h"

#include "atcommand_interface.h"
#include "serial_buffer.h"

void atcmd_binary_parse(void);

void atcmd_binary_respond(atcmd_packet_type response_code); // send OK, or simple ERROR etc.
void atcmd_binary_respond_err_cmd(uint8_t err);         // send command execution error

void atcmd_binary_build_response(atcmd_packet_type response_code);
void atcmd_binary_show_text    (__code const char * str);
void atcmd_binary_append_uint8 (const uint8_t val);
void atcmd_binary_append_uint16(const uint16_t val);
void atcmd_binary_append_uint32(const uint32_t val);
void atcmd_binary_append_array (const uint8_t * data, uint8_t len);
void atcmd_binary_append_str   (__code const char * str);
void atcmd_binary_append_char  (const char val);

void atcmd_binary_send_response(void); // transmit packet built with append_*() functions

void atcmd_binary_init(void);

void atcmd_binary_rx_radio_decoded(void);
void atcmd_binary_rx_radio_raw(void);

#endif /* end of include guard: PROTOCOL_BINARY_H_INCLUDED */
