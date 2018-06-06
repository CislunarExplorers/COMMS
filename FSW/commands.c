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

#include "commands.h"

///////////////////////////////////////////////////////////////////////////////

void atcmd_check_retval(uint8_t retval)
{
    if (retval == SUCCESS) {
        protocol.respond(ATCMD_RESPONSE_OK);
    } else {
        protocol.respond_err_cmd(retval);
    }
}

///////////////////////////////////////////////////////////////////////////////

// TODO: change everything to little endian? Then a simple cast would be enough
// reads an 32bit unsigend integer from a 4 byte array (MSB first, i.e. big endian)
uint32_t atcmd_decode_uint32(__xdata uint8_t * data)
{
    uint32_t
    v  = data[0]; v <<= 8;
    v |= data[1]; v <<= 8;
    v |= data[2]; v <<= 8;
    v |= data[3];
    return v;
}

uint16_t atcmd_decode_uint16(__xdata uint8_t * data)
{
    uint16_t
    v  = data[0]; v <<= 8;
    v |= data[1];
    return v;
}


///////////////////////////////////////////////////////////////////////////////
/*!
 * FORMAT:
 *  cmd[0]      command code
 *  cmd[1]      length of parameter section (in bytes)
 *  cmd[2...]   parameters for command
 *
 *
 *  To implement a new command, create a code for it in atcmd_packet_type enum
 *  in atcommand_interface.h, then implement it here (nothing more is required
 *  for the binary protocol) and in
 *  protocol_text.c:atcmd_text_parse_command_line().
 *
 */

void atcmd_exec_cmd(__xdata uint8_t * cmd)
{
    uint8_t __xdata packet_raw[] = {0x44, 0xAE, 0x0C, 0x78, 0x56, 0x34, 0x12, 0x01, 0x07, 0x78, 0x0B, 0x13, 0x43, 0x65, 0x87};

    #define LENGTH()    cmd[1]
    #define DATA(i)     cmd[2+(i)]

    #define atcmd_assert_data_length_atleast(l) do { \
        if (LENGTH() < l) { \
            protocol.respond(ATCMD_RESPONSE_ERR_MALFORMED_CMD); \
            return; \
        } \
    } while (0)

    switch (cmd[0]) {

        // GENERAL COMMANDS
        ///////////////////////////////////////////////////////////////////////

        case ATCMD_PING:
            // allow any number of parameters
            protocol.respond(ATCMD_RESPONSE_OK);
            break;

        case ATCMD_GET_INFO:
            {
                uint8_t field = 0xFF; // all information
                if (LENGTH() > 0) {
                    field = DATA(0);
                }

                protocol.build_response(ATCMD_RESPONSE_OK);
                switch (field) {
                    case 0xFF:
                    case  0: protocol.show_text("Software Name:            "); protocol.append_str("AX-WMBUS-AT " VERSION_STRING);        if (field != 0xFF) break;
                    case  1: protocol.show_text("Contact Details:          "); protocol.append_str("support@axsem.com");                  if (field != 0xFF) break;
                    case  2: protocol.show_text("Silicon Revision (lower): "); protocol.append_uint8(axwm_get_siliconrev());              if (field != 0xFF) break;
                    case  3: protocol.show_text("Silicon Revision (upper): "); protocol.append_uint8(axwm_get_ax5043_siliconrev());       if (field != 0xFF) break;
                    case  4: protocol.show_text("Major Firmware Version:   "); protocol.append_uint8(axwm_get_major_version());           if (field != 0xFF) break;
                    case  5: protocol.show_text("Minor Firmware Version:   "); protocol.append_uint8(axwm_get_minor_version());           if (field != 0xFF) break;
                    case  6: protocol.show_text("Wireless M-Bus Mode:      "); protocol.append_char(axwm_get_mode());                     if (field != 0xFF) break;
                    case  7: protocol.show_text("Device ID:                "); protocol.append_uint32(axwm_get_id());                                        break;

                    case 190: protocol.show_text("Firmware Revision:        "); protocol.append_str(STRINGIFY(VERSION_REVISION)); break;
                    case 192: protocol.show_text("PLLRANGINGA:              "); protocol.append_uint8(AX5043_PLLRANGINGA); break;
                    case 193: protocol.show_text("PLLVCOI:                  "); protocol.append_uint8(AX5043_PLLVCOI); break;
                    case 194: protocol.show_text("PLLCPI:                   "); protocol.append_uint8(AX5043_PLLCPI); break;
                    case 195: protocol.show_text("axradio_get_mode():       "); protocol.append_uint8(axradio_get_mode()); break;
                    default:
                              protocol.respond(ATCMD_RESPONSE_ERR_INVALID_VALUE); //("invalid information line selected");
                              return; // repsond() already outputs crlf
                }
            }
            protocol.send_response();
            break;

        case ATCMD_SET_MODE:
            atcmd_assert_data_length_atleast(1);
            atcmd_check_retval(axwm_set_mode(DATA(0)));
            break;

        case ATCMD_SET_LINK_LAYER_ADDRESS:
            atcmd_assert_data_length_atleast(8);
            axwm_user_cfg.link.serial  = atcmd_decode_uint32(&DATA(0));
            axwm_user_cfg.link.ID      = atcmd_decode_uint16(&DATA(4));
            axwm_user_cfg.link.version = DATA(6);
            axwm_user_cfg.link.type    = DATA(7);
            axwm_init_tx_buffers();
            protocol.respond(ATCMD_RESPONSE_OK);

            LOG(STR("raw data:"), ARR(&DATA(0), 8), NL());
            LOG(STR("serial:  "), ARR(&axwm_user_cfg.link.serial, 4), NL());
            LOG(STR("ID:      "), ARR(&axwm_user_cfg.link.ID, 2), NL());
            LOG(STR("version: "), HEX8(axwm_user_cfg.link.version), NL());
            LOG(STR("type:    "), HEX8(axwm_user_cfg.link.type), NL());
            break;

        case ATCMD_SET_APPLICATION_LAYER_ADDRESS:
            atcmd_assert_data_length_atleast(8);
            axwm_user_cfg.app.serial  = atcmd_decode_uint32(&DATA(0));
            axwm_user_cfg.app.ID      = atcmd_decode_uint16(&DATA(4));
            axwm_user_cfg.app.version = DATA(6);
            axwm_user_cfg.app.type    = DATA(7);
            axwm_init_tx_buffers();
            protocol.respond(ATCMD_RESPONSE_OK);
            break;

        case ATCMD_SET_AES_KEY:
            atcmd_assert_data_length_atleast(16);
            // copy key from serial buffer into user config
            memcpy(axwm_user_cfg.AES_key, &DATA(0), 16);
            axwm_init_tx_buffers(); // not really necessary if only key has changed
            protocol.respond(ATCMD_RESPONSE_OK);
            break;

        /*
        // TODO!
        case ATCMD_WRITE_CONFIG:
            break;

        // TODO!
        case ATCMD_SET_POWER_MODE:
            atcmd_assert_data_length_atleast(1);
            switch (DATA(1)) {
                case 0: // reset
                    protocol.respond(ATCMD_RESPONSE_OK);
                    // wait until all data has been written
                    uart0_wait_txdone();
                    LOG(WAIT_DONE());

                    for (;;) { PCON |= 1<<4; } // software reset
                    break;

                case 1: // sleep
                    // allow mcu to sleep until next UART or GPIO interrupt
                    // only go to sleep in mainloop when nothing else to do
                    atcmd_check_retval(atcmd_enter_sleep());
                    break;

                case 2: // OFF
                    protocol.respond(ATCMD_RESPONSE_OK); // enter_deepsleep() doesn't return
                    uart0_wait_txdone();
                    atcmd_enter_deepsleep();
                    break;

                default:
                    protocol.respond(ATCMD_RESPONSE_ERR_INVALID_VALUE);
                    break;
            }
            break;
        */


        // RECEIVER COMMANDS
        ///////////////////////////////////////////////////////////////////////

        case ATCMD_ENABLE_RECEIVER:
            atcmd_assert_data_length_atleast(1);
            if (!!DATA(0)) {
                atcmd_check_retval(axwm_start_receive(0)); // decode = false
            } else {
                atcmd_check_retval(axwm_stop_receive());
            }
            break;



        // TRANSMITTER COMMANDS
        ///////////////////////////////////////////////////////////////////////

        case ATCMD_SET_TXPWR:
            atcmd_assert_data_length_atleast(1);
            axwm_set_tx_pwr(DATA(0));
            protocol.respond(ATCMD_RESPONSE_OK);
            break;


        case ATCMD_BUILD_PACKET_SET_HEADER:
            atcmd_assert_data_length_atleast(3);
            atcmd_check_retval(axwm_insert_header(DATA(0), DATA(1), DATA(2)));
            break;


        case ATCMD_BUILD_PACKET_SET_COMMAND:
            atcmd_assert_data_length_atleast(1);
            if (LENGTH() > 1) {
                // optional bit parameter
                atcmd_check_retval(axwm_set_command(DATA(0), !!DATA(1)));
            } else {
                atcmd_check_retval(axwm_set_command(DATA(0), 0)); // default, don't listen for a response
            }
            break;


        case ATCMD_BUILD_PACKET_SET_ACC_RX:
            atcmd_assert_data_length_atleast(1);
            atcmd_check_retval(axwm_set_acc_received(DATA(0)));
            break;


        case ATCMD_BUILD_PACKET_APPEND_DATA:
            atcmd_assert_data_length_atleast(2);
            {
                // TODO: parse that stuff manually and assert that not buffer overrun occurs

                //uint8_t dif = DATA(0);
                uint8_t dif_size = axwm_calc_extended_field_length(&DATA(0)); // counts DIF itself too!

                //uint8_t vif = DATA(dif_size+1);
                uint8_t vif_size = axwm_calc_extended_field_length(&DATA(dif_size)); // counts VIF itself too!

                //LOG(STR("appending data: dif size = "), NUM8(dif_size), STR(", vif size = "), NUM8(vif_size), NL());
                //LOG(STR("raw data: "), ARR(&DATA(0), LENGTH()), NL());

                atcmd_check_retval(axwm_append_data(
                            DATA(0),        &DATA(1), // VIF, VIFE
                            DATA(dif_size), &DATA(dif_size+1), // DIF, DIFE
                            &DATA(dif_size+vif_size)));
            }
            break;


        case ATCMD_BUILD_PACKET_CLEAR_DATA:
            axwm_clear_data();
            protocol.respond(ATCMD_RESPONSE_OK);
            break;


        case ATCMD_TRANSMIT_PACKET:
            atcmd_check_retval(axwm_send_packet());
            break;


        case ATCMD_RETRANSMIT_PACKET:
            atcmd_check_retval(axwm_repeat_packet());
            break;

        case ATCMD_TRANSMIT_RAW:
            atcmd_check_retval(axwm_send_raw(&DATA(0), LENGTH()));
            break;


        // TEST COMMANDS
        ///////////////////////////////////////////////////////////////////////

        case ATCMD_TRANSMIT_TEST:

            atcmd_assert_data_length_atleast(1);
            switch (DATA(0)) {
                case 0:
                    // stop transmission
                    axwm_stop_test_transmission();
                    protocol.respond(ATCMD_RESPONSE_OK);
                    break;

                case 1:
                    // send unmodulated carrier wave
                    axwm_set_cw();
                    protocol.respond(ATCMD_RESPONSE_OK);
                    break;

                case 2:
                    // send 1010 pattern
                    axwm_set_tx1010();
                    protocol.respond(ATCMD_RESPONSE_OK);
                    break;

                case 3:
                    // send random bits
                    axwm_set_cb();
                    protocol.respond(ATCMD_RESPONSE_OK);
                    break;

                // send custom pattern?

                case 4:
                    atcmd_check_retval(axwm_send_raw(packet_raw, sizeof(packet_raw)));
                    break;

                default:
                    protocol.respond(ATCMD_RESPONSE_ERR_INVALID_VALUE);
                    break;
            }
            break;

        ///////////////////////////////////////////////////////////////////////

        case ATCMD_USE_PROTOCOL_BINARY:
            protocol.respond(ATCMD_RESPONSE_OK);
            atcmd_set_protocol_binary();
            break;

        case ATCMD_USE_PROTOCOL_TEXT:
            protocol.respond(ATCMD_RESPONSE_OK);
            atcmd_set_protocol_text();
            break;

        // DEBUG COMMANDs
        ///////////////////////////////////////////////////////////////////////

        case ATCMD_DEBUG_READ_REGISTER:
            atcmd_assert_data_length_atleast(2);
            {
                __xdata const uint8_t * const ptr =
                    (const __xdata uint8_t* const) atcmd_decode_uint16(&DATA(0));
                LOG(STR("reading from address "), HEX16(ptr), NL());
                protocol.build_response(ATCMD_RESPONSE_OK);
                protocol.append_uint8(*ptr); // read memory
                protocol.send_response();
            }
            break;

        case ATCMD_DEBUG_WRITE_REGISTER:
            atcmd_assert_data_length_atleast(3);
            {
                const uint16_t ptr = atcmd_decode_uint16(&DATA(0));
                LOG(STR("writing to address "), HEX16(ptr), NL());
                *((__xdata uint8_t *) ptr) = DATA(2); // write memory
            }
            protocol.respond(ATCMD_RESPONSE_OK);
            break;

        ///////////////////////////////////////////////////////////////////////////////

        default:
            //atcmd_write_error("unknown command");
            protocol.respond(ATCMD_RESPONSE_ERR_UNKNOWN_CMD);
            break;
    }
}
///////////////////////////////////////////////////////////////////////////////
