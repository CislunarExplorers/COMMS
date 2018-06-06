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


#include "uart.h"

///////////////////////////////////////////////////////////////////////////////
void axwm_uart_init()
{
	PALTB  |= (1<<4); // B4 enable U0TX
	DIRB   |= (1<<4); // B4 is output
	DIRB   &= (uint8_t)~(1<<5); // B5 is input (U0RX)
	PINSEL &= (uint8_t)~(1<<0); // U0RX is B5

	// enable interrupt on BREAK
	// will be overwritten by uart0_init!
	// U0CTRL |= (1<<5);

	EIP |= (1<<4); // UART0 has priority

	uart_timer1_baud(CLKSRC_FRCOSC, ATCOMMAND_SERIAL_BAUD, 20000000UL);
	uart0_init(1, ATCOMMAND_SERIAL_WORDLENGTH, ATCOMMAND_SERIAL_STOP_BITS);
}
///////////////////////////////////////////////////////////////////////////////
