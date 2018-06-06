// Copyright (c) 2007,2008,2009,2010,2011,2012,2013 AXSEM AG
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
//     1.Redistributions of source code must retain the above copyright
//       notice, this list of conditions and the following disclaimer.
//     2.Redistributions in binary form must reproduce the above copyright
//       notice, this list of conditions and the following disclaimer in the
//       documentation and/or other materials provided with the distribution.
//     3.Neither the name of AXSEM AG, Duebendorf nor the
//       names of its contributors may be used to endorse or promote products
//       derived from this software without specific prior written permission.
//     4.All advertising materials mentioning features or use of this software
//       must display the following acknowledgement:
//       This product includes software developed by AXSEM AG and its contributors.
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

#include <ax8052.h>
#include <libmftypes.h>
#include <libmfwtimer.h>
#include <libaxlcd2.h>

#include "misc.h"
#include "axradio5043.h"

///////////////////////////////////////////////////////////////////////////////
uint8_t array_equal(uint8_t __xdata const * a, uint8_t __xdata const * b, uint8_t length)
{
    while (length-- > 0) {
        if ((*a++) != (*b++))
            return 0;
    }

    return 1;
}
///////////////////////////////////////////////////////////////////////////////
static struct wtimer_desc __xdata delaymstimer;

static void delayms_callback(struct wtimer_desc __xdata *desc)
{
    desc;
    delaymstimer.handler = 0;
}
///////////////////////////////////////////////////////////////////////////////
__reentrantb void delay_ms(uint16_t ms) __reentrant
{
    // scaling: 20e6/64/1e3=312.5=2^8+2^6-2^3+2^-1
    uint32_t x;
    wtimer_remove(&delaymstimer);
    x = ms;
    delaymstimer.time = ms >> 1;
    x <<= 3;
    delaymstimer.time -= x;
    x <<= 3;
    delaymstimer.time += x;
    x <<= 2;
    delaymstimer.time += x;
    delaymstimer.handler = delayms_callback;
    wtimer1_addrelative(&delaymstimer);

    do {
        wtimer_runcallbacks();
        if (!delaymstimer.handler)
            break;
        wtimer_idle(WTFLAG_CANSTANDBY); // no sleep (otherwise clock wouldn't run and we wouldn't return here)
    } while (delaymstimer.handler);
}
///////////////////////////////////////////////////////////////////////////////
__reentrantb void delay_ms_timer0(uint16_t ms) __reentrant
{
    wtimer_remove(&delaymstimer);
    delaymstimer.time = WTIMER0_UNITS(MS(ms));
    delaymstimer.handler = delayms_callback;

    wtimer0_addrelative(&delaymstimer);

    do {
        wtimer_runcallbacks();
        if (!delaymstimer.handler)
            break;
        wtimer_idle(WTFLAG_CANSTANDBY); // no sleep (LPOSC is still running, but we wouldn't return here)
    } while (delaymstimer.handler);
}
///////////////////////////////////////////////////////////////////////////////
void delay_nop(uint8_t ticks)
{
    while(--ticks) { nop(); }
}
///////////////////////////////////////////////////////////////////////////////
void delay_nop2(uint8_t ticks)
{
    while(--ticks) {
        uint8_t t = 255;
        while(--t) {
            nop();
        }
    }
}
///////////////////////////////////////////////////////////////////////////////
void shift_half_byte(uint8_t __xdata * data, uint8_t len)
{
    while (len > 0) {

        data[len-1] &= 0xF0; // clear lower nibble
        data[len-1] |= data[len-1] >> 4; // copy higher nibble to lower
        data[len-1] &= 0x0F; // clear higher nibble

        if (len > 1) {
            // copy lower nibble of previous to byte to higher nibble of current byte
            data[len-1] |= data[len-2] << 4;
        }

        len--;
    }
}
///////////////////////////////////////////////////////////////////////////////
void reverse_nibbles(uint8_t __xdata * data, uint8_t len)
{
    while (len-->0) {
        data[len-1] = ((data[len-1] >> 4) & 0x0F) | ((data[len-1] << 4) & 0xF0);
    }
}
///////////////////////////////////////////////////////////////////////////////
// source: http://www.dsprelated.com/showmessage/62049/3.php (30.9.13)
__xdata static uint16_t seed = 0;

void quick_prng_set_seed(uint16_t s)
{
    seed = s;
}

uint8_t quick_prng()
{
    if (seed == 0)
        seed = T0CNT0 | ((uint16_t) T0CNT1) << 8; // counter of timer 0 (LPOSC, 640Hz)

    seed = (seed << 7) - seed + 251;
    return (uint8_t) (seed + (seed>>8));
}
///////////////////////////////////////////////////////////////////////////////
uint8_t quick_prng_no_extrema()
{
    // this function at least attemts to stay uniform

    uint8_t r;

    do {
        r = quick_prng();
    } while (r == 0 || r == 0xFF);

    return r;
}
///////////////////////////////////////////////////////////////////////////////
uint8_t quick_prng_range(uint8_t min, uint8_t max)
{
    // this is even less uniformly random if max-min+1 is not an integer part of 256 (or so)
    return min + (quick_prng() % (max-min+1));
}
///////////////////////////////////////////////////////////////////////////////
uint16_t quick_prng16()
{
    uint16_t r  = quick_prng();
    r <<= 8; r |= quick_prng();

    return r;
}
///////////////////////////////////////////////////////////////////////////////
__reentrantb uint32_t quick_prng32(uint32_t max) __reentrant
{
    uint32_t r  = quick_prng();
    r <<= 8; r |= quick_prng();
    r <<= 8; r |= quick_prng();
    r <<= 8; r |= quick_prng();

    r %= max;

    return r;
}
///////////////////////////////////////////////////////////////////////////////
