// Copyright (c) 2014 AXSEM AG
// All rights reserved.
//
// CONFIDENTIAL
//
// Redistribution  and use in source and binary forms (either in whole or in parts),
// with or without modification, are not permitted.
//
// Use of this source code and its binary form shall only be run on AX8052F143
// chips.
//
// THIS SOFTWARE IS PROVIDED BY AXSEM AG AND CONTRIBUTORS ``AS IS'' AND ANY
// EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
// WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
// DISCLAIMED. IN NO EVENT SHALL AXSEM AG AND CONTRIBUTORS BE LIABLE FOR ANY
// DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
// (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
// LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
// ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
// SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


#ifndef ATCOMMAND_INTERFACE_H_INCLUDED
#define ATCOMMAND_INTERFACE_H_INCLUDED

#include <libmftypes.h>
#include <string.h>

#include "common/easyax_defines.h"
#include "uart.h"
#include "code/wmbus.h"
#include "code/wmbus_receiver.h"
#include "code/wmbus_sender.h"

void atcmd_init();

void atcmd_parse();

//void atcmd_response_error_cmd(uint8_t error_code); // TODO: want enum here. Probably need to expand this anyway, as error code/message might depend on actual command

/*
 * to add a new command:
 * 1. add new entry to enum atcmd_packet_type below
 * 2. implement functionality in commands.c::atcmd_exec_cmd()
 * 3. implement the command in the text-protocol in protocol_text.c:
 *      1. add command to command_lookup_table in protocol_text.c
 *      2. add command to help-command in atcmd_text_parse_command_line()
 *      3. parse command line in atcmd_text_parse_command_line()
 *         (simply parse tokens into binary command)
 */

typedef enum {

    ATCMD_INVALID               = 0,

    // GENERAL COMMANDS

    ATCMD_PING                  = 1,
    ATCMD_GET_INFO              = 2,

    ATCMD_SET_MODE              = 3,

    ATCMD_SET_LINK_LAYER_ADDRESS        = 4,
    ATCMD_SET_APPLICATION_LAYER_ADDRESS = 5,
    ATCMD_SET_AES_KEY                   = 6,

    // TODO
    ATCMD_WRITE_CONFIG          ,//= 4, // TODO
    ATCMD_SET_POWER_MODE        ,//= 5,

    // RECEIVER COMMANDS
    ATCMD_ENABLE_RECEIVER               = 0x20,
    ATCMD_EVENT_DECODED_PACKET_RECEIVED = 0x21, // not a command! sent by module
    ATCMD_EVENT_RAW_PACKET_RECEIVED     = 0x22, // not a command! sent by module

    // TRANSMITTER COMMANDS
    ATCMD_SET_TXPWR             = 0x40,

    ATCMD_BUILD_PACKET_SET_HEADER       = 0x50,
    ATCMD_BUILD_PACKET_SET_COMMAND      = 0x51,
    ATCMD_BUILD_PACKET_SET_ACC_RX       = 0x52,
    ATCMD_BUILD_PACKET_APPEND_DATA      = 0x53,
    ATCMD_BUILD_PACKET_CLEAR_DATA       = 0x54,
    ATCMD_TRANSMIT_PACKET               = 0x55,
    ATCMD_RETRANSMIT_PACKET             = 0x56,
    ATCMD_TRANSMIT_RAW                  = 0x57,

    // TEST COMMANDS
    ATCMD_TRANSMIT_TEST                 = 0x60,

    /*
    ATCMD_GET_MODE              = 3,
    ATCMD_INSERT_HEADER         = 6,
    ATCMD_SET_ACC               = 7,
    ATCMD_SET_COMMAND           = 8,
    ATCMD_APPEND_DATA           = 9,
    ATCMD_CLEAR_DATA            = 10,
    ATCMD_SEND_PACKET           = 11,
    ATCMD_REPEAT_PACKET         = 12,
    ATCMD_SEND_RAW              = 13,
    ATCMD_RECEIVE               = 14,
    ATCMD_GET_RAW_LEN           = 16,
    ATCMD_GET_RAW               = 17,
    ATCMD_GET_LL_INFO           = 24,
    ATCMD_GET_AL_INFO           = 25,
    ATCMD_GET_DIF               = 32,
    ATCMD_GET_VIF               = 33,
    ATCMD_GET_LVAR              = 34,
    ATCMD_GET_DATA              = 35,
    ATCMD_GET_LEN               = 36,
    ATCMD_GET_DATA_COUNT        = 37,
    ATCMD_GET_CI                = 38,
    ATCMD_SET_PWRMODE           = 40,
    ATCMD_SEND_CW               = 43,
    ATCMD_SEND_1010             = 44,
    ATCMD_SEND_PATTERN          = 45,
    ATCMD_SEND_CB               = 46,
    ATCMD_SEND_TEST_FRAME       = 47
    */

    ATCMD_USE_PROTOCOL_BINARY           = 0x70,
    ATCMD_USE_PROTOCOL_TEXT             = 0x71,

    ATCMD_DEBUG_READ_REGISTER           = 0x80,
    ATCMD_DEBUG_WRITE_REGISTER          = 0x81,

    // TEXT PROTOCOL ONLY COMMANDS
    // they don't actually need specific command codes ;)
    ATCMD_TEXT_HELP                     = 0xE0,
    ATCMD_TEXT_CLEAR_SCREEN             = 0xE1,
    ATCMD_TEXT_HISTORY                  = 0xE2,




    ATCMD_RESPONSE_OK                   = 0xF0, // no error, command was executed successfully

    // execution error
    ATCMD_RESPONSE_ERR_CMD              = 0xF1, // command error, see specific error code

    // syntax/semantic errors
    ATCMD_RESPONSE_ERR_UNKNOWN_CMD      = 0xF2, // command not implemented
    ATCMD_RESPONSE_ERR_MALFORMED_CMD    = 0xF3, // not enough / too many parameters, wrong CRC, etc.
    ATCMD_RESPONSE_ERR_INVALID_VALUE    = 0xF4  // command parameter not allowed
} atcmd_packet_type;

typedef struct {
    void (*parse)(void);

    void (*respond)(atcmd_packet_type); // send OK, or simple ERROR etc.
    void (*respond_err_cmd)(uint8_t);         // send command execution error

    void (*build_response)(atcmd_packet_type); // start new response consisting of a few more fields
    void (*show_text)    (__code const char *); // output in text mode, ignore in binary mode
    void (*append_uint8) (const uint8_t);
    void (*append_uint16)(const uint16_t);
    void (*append_uint32)(const uint32_t);
    void (*append_str)   (__code const char *); // append string (pad/cut it to fixed length of 32 bytes)
    void (*append_char)  (const char);

    void (*send_response)(void); // transmit packet built with append_*() functions

    void (*init)(void);

    // handle an incoming radio packet
    void (*rx_radio_raw)(void);
    void (*rx_radio_decoded)(void);
} atcmd_protocol;

extern __xdata atcmd_protocol protocol;

void atcmd_set_protocol_binary();
void atcmd_set_protocol_text();

extern void atcmd_exec_cmd(__xdata uint8_t * cmd);

#endif /* end of include guard: ATCOMMAND_INTERFACE_H_INCLUDED */


