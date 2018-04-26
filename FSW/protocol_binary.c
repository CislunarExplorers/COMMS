#include "protocol_binary.h"

///////////////////////////////////////////////////////////////////////////////

#define PACKET_SOF_MARKER   0x16 // ASCII SYN and one of the least likely symbols to received when sending random data at random baudrate
//#define PACKET_EOF_MARKER   0xAA // TODO: we don't really need this, do we?


#define BYTE_TIMEOUT        US(100)

///////////////////////////////////////////////////////////////////////////////

__bit rx_packet_in_progress = 0;

///////////////////////////////////////////////////////////////////////////////

struct wtimer_desc __xdata byte_timeout_timer;

void atcmd_binary_byte_timeout_cb(struct wtimer_desc __xdata *desc)
{
    desc;

    // abort packet reception
    rx_packet_in_progress = 0;

    //LOG(STR("[ATB] timeout\n"));
}

///////////////////////////////////////////////////////////////////////////////

void atcmd_binary_init(void)
{
    rx_buffer_len = 0;
    rx_packet_in_progress = 0;

    byte_timeout_timer.handler = atcmd_binary_byte_timeout_cb;

    uart0_rxadvance(uart0_rxcount());

    //LOG(STR("[ATB] clearing buffers\n"));
}

///////////////////////////////////////////////////////////////////////////////

void atcmd_binary_parse(void)
{
    if (uart0_rxcount() == rx_buffer_len)
        return; // no new data :(

    while (uart0_rxcount() > rx_buffer_len) {

        if (rx_packet_in_progress == 0) {
            // wait for SOF marker
            if (uart0_rxpeek(0) == PACKET_SOF_MARKER) {
                // begin a new packet
                rx_packet_in_progress = 1;

                rx_buffer_len = 0;

                //LOG(STR("[ATB] found SOF, starting packet\n"));
            } else {
                //LOG(STR("[ATB] invalid SOF: "), HEX8(uart0_rxpeek(0)), NL());
            }

            uart0_rxadvance(1); // drop byte (we don't need either valid nor invalid SOF marker byte)
        } else {
            // receiving a packet
            // copy data to local buffer
            rx_buffer[rx_buffer_len] = uart0_rxpeek(rx_buffer_len);

            ++rx_buffer_len;

            // we've got data, stop (and potentially restart) byte timeout timer
            wtimer0_remove(&byte_timeout_timer);
            wtimer_remove_callback((struct wtimer_callback*) &byte_timeout_timer);

            if (rx_buffer_len >= 3) {
                // we've already got the length byte and maybe the CRC

                if (rx_buffer[1] > RX_BUFFER_SIZE-3) {
                    // drop packet, not enough space in local buffer
                    // wait for next packet
                    rx_packet_in_progress = 0;
                    rx_buffer_len = 0;
                    // don't rxadvance() anything, just check next byte (which we though was the CMD field) as a possible SOF marker
                    LOG(STR("[ATB] dropping packet, too big\n"));
                } else if (rx_buffer[1] == rx_buffer_len-2-1) { // don't count CMD and length fields at the beginning or CRC at end
                    // packet is complete!
                    // check if CRC matches (CRC over CMD, length, data)
                    // TODO: init with 0 okay?
                    uint8_t expected_crc = crc_crc8ccitt_msb(&rx_buffer[0], rx_buffer_len-1, 0);
                    if (expected_crc == rx_buffer[rx_buffer_len-1]) {

                        // make space for the next packet
                        uart0_rxadvance(rx_buffer_len);

                        // we've got a valid packet, process it
                        atcmd_exec_cmd(rx_buffer);
                    } else {
                        // CRC fail, flush local buffer, and restart at the next byte
                        //uart0_rxadvance(1); don't flush anything, check if CMD is a valid SOF marker
                        LOG(STR("[ATB] invalid CRC: "), HEX8(rx_buffer[rx_buffer_len-1]),
                                    STR(" expected: "), HEX8(expected_crc), NL());
                    }

                    rx_packet_in_progress = 0;
                    rx_buffer_len = 0;
                }
            }
        }
    }

    if (rx_packet_in_progress) { // this check isn't really necessary, but prevents unnecessary timeouts after a complete packet
        // packet isn't complete yet, start timeout
        byte_timeout_timer.time = WTIMER1_UNITS(BYTE_TIMEOUT);
        wtimer0_addrelative(&byte_timeout_timer);
    }
}

///////////////////////////////////////////////////////////////////////////////

void atcmd_binary_respond(atcmd_packet_type response_code)
{
    atcmd_binary_build_response(response_code);
    atcmd_binary_send_response();
}

///////////////////////////////////////////////////////////////////////////////

void atcmd_binary_respond_err_cmd(uint8_t err)
{
    atcmd_binary_build_response(ATCMD_RESPONSE_ERR_CMD);
    atcmd_binary_append_uint8(err);
    atcmd_binary_send_response();
}

///////////////////////////////////////////////////////////////////////////////

void atcmd_binary_build_response(atcmd_packet_type response_code)
{
    tx_buffer[0] = response_code;
    tx_buffer[1] = 0; // length
    tx_buffer_len = 2;
}

///////////////////////////////////////////////////////////////////////////////

void atcmd_binary_show_text    (__code const char * str)
{
    UNUSED(str);

    // ignore, this is just for the text-based protocol
}

///////////////////////////////////////////////////////////////////////////////

void atcmd_binary_append_uint8(const uint8_t val)
{
    if (tx_buffer_len >= TX_BUFFER_SIZE) {
        // TODO: handle error
        // -> send ATCMD_RESPONSE_ERR_TX_BUFFER_OVERFLOW or so
        // -> set current packet to 'invalid' or something
        LOG(STR("[ATB] ERROR: cannot append uint8_t, tx_buffer full\n"));
        return;
    }

    tx_buffer[tx_buffer_len++] = val;
}

///////////////////////////////////////////////////////////////////////////////

void atcmd_binary_append_uint16(const uint16_t val)
{
    if (tx_buffer_len >= TX_BUFFER_SIZE-1) {
        // TODO: handle error
        LOG(STR("[ATB] ERROR: cannot append uint16_t, tx_buffer full\n"));
        return;
    }

    // send value as big endian
    atcmd_binary_append_uint8( (val>>8) & 0x00FF );
    atcmd_binary_append_uint8(  val     & 0x00FF );
}

///////////////////////////////////////////////////////////////////////////////

void atcmd_binary_append_uint32(const uint32_t val)
{
    if (tx_buffer_len >= TX_BUFFER_SIZE-3) {
        // TODO: handle error
        LOG(STR("[ATB] ERROR: cannot append uint32_t, tx_buffer full\n"));
        return;
    }

    // send value as big endian
    atcmd_binary_append_uint8( (val>>24) & 0x000000FF );
    atcmd_binary_append_uint8( (val>>16) & 0x000000FF );
    atcmd_binary_append_uint8( (val>> 8) & 0x000000FF );
    atcmd_binary_append_uint8(  val      & 0x000000FF );
}

///////////////////////////////////////////////////////////////////////////////

void atcmd_binary_append_array(const uint8_t * data, uint8_t len)
{
    if (tx_buffer_len >= TX_BUFFER_SIZE-len+1) {
        // TODO: handle error
        LOG(STR("[ATB] ERROR: cannot append array["), NUM8(len) ,STR("], tx_buffer full\n"));
        return;
    }

    while (len-- > 0) {
        tx_buffer[tx_buffer_len++] = *data++;
    }
}

///////////////////////////////////////////////////////////////////////////////

void atcmd_binary_append_str(__code const char * str)
{
    uint8_t field_length = 32;

    // copy string
    // TODO: pass length of string buffer str
    while (*str != '\0' && field_length > 1) { // 'field_length > 1' => ensure last byte will be 0

        if (tx_buffer_len >= TX_BUFFER_SIZE) {
            // TODO: handle error
            LOG(STR("[ATB] ERROR: cannot append string, tx_buffer full\n"));
            return;
        }

        tx_buffer[tx_buffer_len++] = *str;
        --field_length;
        ++str;
    }

    // pad remaining bytes with zeroes
    while(field_length > 0) {

        if (tx_buffer_len >= TX_BUFFER_SIZE) {
            // TODO: handle error
            LOG(STR("[ATB] ERROR: cannot pad string, tx_buffer full\n"));
            return;
        }

        tx_buffer[tx_buffer_len++] = '\0';
        --field_length;
    }
}

///////////////////////////////////////////////////////////////////////////////

void atcmd_binary_append_char(const char val)
{
    atcmd_binary_append_uint8((uint8_t) val);
}

///////////////////////////////////////////////////////////////////////////////

void atcmd_binary_send_response(void)
{
    if (tx_buffer_len < 2) {
        // TODO: handle error
        // assertion fail! invalid packet built
        LOG(STR("[ATB] invalid response packet built, length < 2!\n"));
        return;
    }

    if (tx_buffer_len > TX_BUFFER_SIZE) {
        // TODO: handle error
        // assertion fail! invalid packet built
        LOG(STR("[ATB] invalid response packet built, length > TX_BUFFER_SIZE!\n"));
        return;
    }

    // set length field
    tx_buffer[1] = tx_buffer_len-2; // don't count CMD and length field towards length

    // actually transmit this packet
    uart0_tx(PACKET_SOF_MARKER); // mark start of packet
    {
        uint8_t i = 0;
        for (; i < tx_buffer_len; i++) {
            uart0_tx(tx_buffer[i]);
        }
    }

    // append CRC
    uart0_tx(crc_crc8ccitt_msb(&tx_buffer[0], tx_buffer_len, 0));

    // clear transmit buffer
    tx_buffer_len = 0;
}

///////////////////////////////////////////////////////////////////////////////

void atcmd_binary_rx_radio_raw(void)
{
    LOG(STR("[ATB] got raw radio packet ("), NUM8(axwm_get_raw_len()), STR(" bytes)\n"));

    atcmd_binary_build_response(ATCMD_EVENT_RAW_PACKET_RECEIVED);

    // RSSI (8bit should be enough ;)
    atcmd_binary_append_uint8((int8_t) axwm_get_RSSI());

    atcmd_binary_append_array(axwm_get_raw(), axwm_get_raw_len());

    atcmd_binary_send_response();
}

///////////////////////////////////////////////////////////////////////////////
// this only works for standard packets, as soon as manufacturer specific stuff comes into play we're screwed
void atcmd_binary_rx_radio_decoded(void)
{
    uint8_t data_cnt = 0, data_idx = 0;

    atcmd_binary_build_response(ATCMD_EVENT_DECODED_PACKET_RECEIVED);

    // RSSI (8bit should be enough ;)
    atcmd_binary_append_uint8((int8_t) axwm_get_RSSI());

    // Control
    atcmd_binary_append_uint8(axwm_get_c());
    atcmd_binary_append_uint8(axwm_get_ci());

    // Link Layer
    atcmd_binary_append_uint8 (axwm_get_type());
    atcmd_binary_append_uint16(axwm_get_manufacturer());
    atcmd_binary_append_uint8 (axwm_get_version());
    atcmd_binary_append_array (axwm_get_serialnumber(), 4);
    atcmd_binary_append_uint8 (axwm_get_status());
    atcmd_binary_append_uint8 (axwm_get_acc());
    atcmd_binary_append_uint8 (axwm_get_conf());

    // Application Layer
    atcmd_binary_append_uint8 (axwm_get_al_type());
    atcmd_binary_append_uint16(axwm_get_al_manufacturer());
    atcmd_binary_append_uint8 (axwm_get_al_version());
    atcmd_binary_append_array (axwm_get_al_serialnumber(), 4);
    atcmd_binary_append_uint8 (axwm_get_al_status());
    atcmd_binary_append_uint8 (axwm_get_al_acc());
    atcmd_binary_append_uint8 (axwm_get_al_conf());

    // Data
    data_cnt = axwm_get_data_count();
    atcmd_binary_append_uint8(data_cnt);

    for (; data_idx < data_cnt; data_idx++) {

        uint8_t dif_length  = axwm_get_dif_length(data_idx);
        uint8_t vif_length  = axwm_get_vif_length(data_idx);
        uint8_t data_length = axwm_get_len(data_idx);
        uint8_t i = 0;

        // length of this data segment
        atcmd_binary_append_uint8(dif_length + vif_length + data_length);

        atcmd_binary_append_array(axwm_get_dif(data_idx),  dif_length);
        atcmd_binary_append_array(axwm_get_vif(data_idx),  vif_length);
        atcmd_binary_append_array(axwm_get_data(data_idx), data_length);
    }


    //atcmd_binary_append_uint8(axwm_get_);
    //atcmd_binary_append_
    //
    // 16   00  1A   C4  00 00    FF    24  23   FF        FF FF 07 87     00 00 00 
    // syn  CMD len rssi c  ci    type  manuf    version   serial          status acc conf  
    //
    // 00 00 00       00    00 00 00  00   00 00 00           03       78
    // t manuf        vers  serial         status acc conf    datacnt  CRC


    atcmd_binary_send_response();
}

///////////////////////////////////////////////////////////////////////////////
