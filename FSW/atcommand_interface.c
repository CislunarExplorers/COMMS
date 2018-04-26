#include "atcommand_interface.h"

///////////////////////////////////////////////////////////////////////////////

__xdata atcmd_protocol protocol;

///////////////////////////////////////////////////////////////////////////////

void atcmd_init()
{
    // initialize uart
    axwm_uart_init();

#if 0
    // use binary protocol by default
    atcmd_set_protocol_binary();
#else
    atcmd_set_protocol_text();
#endif

    protocol.init();
}

///////////////////////////////////////////////////////////////////////////////

void atcmd_parse()
{
    protocol.parse();
}

///////////////////////////////////////////////////////////////////////////////

void axwm_receive_callback(struct axradio_status __xdata *st)
{
    // try to decode packet
    uint8_t err = axwm_decode_data(st);

    if (err == SUCCESS) {
        protocol.rx_radio_decoded();
    } else {
        LOG(STR("ERROR: failed to decode packet, error code "), NUM8(err), NL());

        // copy raw data and forward it without decoding
        err = axwm_process_packet(st);
        if (err == SUCCESS) {
            protocol.rx_radio_raw();
        } else {
            // this cannot happen :P
            LOG(STR("ERROR: failed to process packet, error code "), NUM8(err), NL());
        }
    }
}

///////////////////////////////////////////////////////////////////////////////

#include "protocol_binary.h"

void atcmd_set_protocol_binary()
{
    protocol.parse              = atcmd_binary_parse;

    protocol.respond            = atcmd_binary_respond;
    protocol.respond_err_cmd    = atcmd_binary_respond_err_cmd;

    protocol.build_response     = atcmd_binary_build_response;
    protocol.show_text          = atcmd_binary_show_text;
    protocol.append_uint8       = atcmd_binary_append_uint8;
    protocol.append_uint16      = atcmd_binary_append_uint16;
    protocol.append_uint32      = atcmd_binary_append_uint32;
    protocol.append_str         = atcmd_binary_append_str;
    protocol.append_char        = atcmd_binary_append_char;

    protocol.send_response      = atcmd_binary_send_response;

    protocol.init               = atcmd_binary_init;

    protocol.rx_radio_decoded   = atcmd_binary_rx_radio_decoded;
    protocol.rx_radio_raw       = atcmd_binary_rx_radio_raw;
}

///////////////////////////////////////////////////////////////////////////////

#include "protocol_text.h"

void atcmd_set_protocol_text()
{
    protocol.parse              = atcmd_text_terminal;

    protocol.respond            = atcmd_text_respond;
    protocol.respond_err_cmd    = atcmd_text_respond_err_cmd;

    protocol.build_response     = atcmd_text_build_response;
    protocol.show_text          = atcmd_text_show_text;
    protocol.append_uint8       = atcmd_text_append_uint8;
    protocol.append_uint16      = atcmd_text_append_uint16;
    protocol.append_uint32      = atcmd_text_append_uint32;
    protocol.append_str         = atcmd_text_append_str;
    protocol.append_char        = atcmd_text_append_char;

    protocol.send_response      = atcmd_text_send_response;

    protocol.init               = atcmd_text_init;

    protocol.rx_radio_decoded   = atcmd_text_rx_radio_decoded;
    protocol.rx_radio_raw       = atcmd_text_rx_radio_raw;
}

///////////////////////////////////////////////////////////////////////////////
