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

#ifndef ATCOMMAND_COMMANDS_H_INCLUDED
#define ATCOMMAND_COMMANDS_H_INCLUDED

#include <string.h>

#include "code/wmbus_sender.h"
#include "code/wmbus_receiver.h"
#include "code/errorcodes.h"
#include "code/config.h"
#include "code/testmodes.h"

#include "atcommand_interface.h"

///////////////////////////////////////////////////////////////////////////////
// This file implements the actual actions.
// atcmd_exec_cmd() is called by the parser whenever it encounters a valid command.
///////////////////////////////////////////////////////////////////////////////

// cmd[0] = command, cmd[1] = length of following data (0 if none)
// multi-bytes values are encoded in big endian, i.e. data[0] is MSB, data[3] LSB for 32bit int!
void atcmd_exec_cmd(__xdata uint8_t * cmd);

///////////////////////////////////////////////////////////////////////////////

#endif /* end of include guard: ATCOMMAND_COMMANDS_H_INCLUDED */

