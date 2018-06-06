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


#ifndef MISC_H_INCLUDED
#define MISC_H_INCLUDED

#include <libmftypes.h>
#include "version.h"
#include "timing.h"

#ifdef USE_DBGLINK
#include <libmfdbglink.h>
#endif // USE_DBGLINK

///////////////////////////////////////////////////////////////////////////////

// X-Macro
// define F(x), then 'call' REP_n(0), undef F

#define REP_5(x)  F(x), F((x)+1), F((x)+2), F((x)+3), F((x)+4)
#define REP_20(x) REP_5(x), REP_5((x)+5), REP_5((x)+10), REP_5((x)+15)
#define REP_40(x) REP_20(x), REP_20((x)+20)

///////////////////////////////////////////////////////////////////////////////

// Nice macro which evaluates parameters only once. Unfortunately it is GCC-only.
/*
#define MAX(a, b)   ({ __typeof__(a) _a = (a); \
                       __typeof__(b) _b = (b); \
                       _a > _b ? _a : _b; })
                       */

#define MIN(a, b) (((a)<(b)?(a):(b)))
#define MAX(a, b) (((a)>(b)?(a):(b)))

///////////////////////////////////////////////////////////////////////////////

// swaps the order of MSB and LSB (e.g. 0xABCD -> 0xCDAB)
#define BYTE_SWAP16(x) do { \
    uint8_t lsb = (uint8_t) ((x) & 0x00FF); \
    (x) >>= 8; \
    (x) |= ((uint16_t) lsb) << 8; \
} while(0)

///////////////////////////////////////////////////////////////////////////////

#define UNUSED(x)   ((void) x)

///////////////////////////////////////////////////////////////////////////////

#define BIT(x)	((uint8_t) (1<<(x)))

#define BIT_CONST(a,b,c,d,e,f,g,h) ( \
		  ( (a) ? (BIT(7)) : 0 ) \
		| ( (b) ? (BIT(6)) : 0 ) \
		| ( (c) ? (BIT(5)) : 0 ) \
		| ( (d) ? (BIT(4)) : 0 ) \
		| ( (e) ? (BIT(3)) : 0 ) \
		| ( (f) ? (BIT(2)) : 0 ) \
		| ( (g) ? (BIT(1)) : 0 ) \
		| ( (h) ? (BIT(0)) : 0 ) \
	)

#define BYTE(x, num) (*((uint8_t*)(&(x)) + (num)))

///////////////////////////////////////////////////////////////////////////////

#define _STRINGIFY(x) #x
#define  STRINGIFY(x) _STRINGIFY(x)

///////////////////////////////////////////////////////////////////////////////

uint8_t array_equal(uint8_t __xdata const * a, uint8_t __xdata const * b, uint8_t length);

///////////////////////////////////////////////////////////////////////////////

void calibrate_lposc(void);

__reentrantb void delay_ms(uint16_t ms) __reentrant;
__reentrantb void delay_ms_timer0(uint16_t ms) __reentrant;

void delay_nop(uint8_t ticks);
void delay_nop2(uint8_t ticks);

///////////////////////////////////////////////////////////////////////////////

//! shifts everything in 'data' by 4 bits in a MSB-first way, overwrites last nibble!
//! eg. [ 0xAB CD EF ] --> [ 0x0A BC DE ]
void shift_half_byte(uint8_t __xdata * data, uint8_t len);

//! reverses lower with upper half of a byte
void reverse_nibbles(uint8_t __xdata * data, uint8_t len);

///////////////////////////////////////////////////////////////////////////////

//! quick and dirty, do NOT use for anything cryptographical or otherwise security relevant!
extern uint8_t quick_prng();
extern void quick_prng_set_seed(uint16_t s);

//! same as quick_prng(), but does not return 0x00 or 0xFF
extern uint8_t quick_prng_no_extrema();

//! same as quick_prng(), but returns only values in range [min, max]
extern uint8_t quick_prng_range(uint8_t min, uint8_t max);

//! calls quick_prng() twice
extern uint16_t quick_prng16();

//! calls quick_prng() four times for a 32 bit random value
//! returns value which is less than max
__reentrantb extern uint32_t quick_prng32(uint32_t max) __reentrant;

///////////////////////////////////////////////////////////////////////////////

#define XOR_SWAP(a, b) do { \
    (a) ^= (b); \
    (b) ^= (a); \
    (a) ^= (b); \
} while(0)

///////////////////////////////////////////////////////////////////////////////

// helper type to access single bytes of a 32bit int
typedef union {

    struct {
        uint32_t value;
    } u32;

    struct {
        uint16_t value0_LSB;
        uint16_t value1_MSB;
    } u16;

    struct {
        uint8_t value0_LSB;
        uint8_t value1;
        uint8_t value2;
        uint8_t value3_MSB;
    } u8;

    struct {
        uint16_t value[2];
    } u16arr;

    struct {
        uint8_t value[4];
    } u8arr;

} array32;

// helper type to access single bytes of a 16bit int
// #TODO: make these properly byte order independent
typedef union {

    struct {
        uint16_t value;
    } u16;

    struct {
        uint8_t value0_LSB;
        uint8_t value1_MSB;
    } u8;

    struct {
        uint8_t value[2];
    } u8arr;

} array16;

///////////////////////////////////////////////////////////////////////////////

#endif // MISC_H_INCLUDED
