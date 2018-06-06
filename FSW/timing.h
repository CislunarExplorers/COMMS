#ifndef TIMING_H_INCLUDED
#define TIMING_H_INCLUDED

#include <libmftypes.h>
#include <ax8052f143.h>
#include <libmfosc.h>

#include "axradio5043.h" // why?
#include "dbghelpers.h"

///////////////////////////////////////////////////////////////////////////////

#define WTIMER0_CLKSRC          CLKSRC_LPOSC    // 640 Hz
#define WTIMER0_PRESCALER       0x01            //  x1 = 640 Hz

#define WTIMER1_CLKSRC          CLKSRC_FRCOSC   //  20 MHz
#define WTIMER1_PRESCALER       0x07            // /64 = 312.5 KHz

///////////////////////////////////////////////////////////////////////////////
// use floats here! otherwise we cannot use something like MS(1.23)

#define WTIMER0_CYCLES_PER_US   0.000640
#define WTIMER0_CYCLES_PER_MS   0.640
#define WTIMER0_CYCLES_PER_S    640.0

#define WTIMER1_CYCLES_PER_US   0.312500
#define WTIMER1_CYCLES_PER_MS   312.5
#define WTIMER1_CYCLES_PER_S    312500.0

///////////////////////////////////////////////////////////////////////////////
// TIME CONVERSIONS

// usage e.g.:
// WTIMER1_UNITS(MS(100))

#define _WTIMER0_UNITS(unit, time)          ((uint32_t) ((time) * WTIMER0_CYCLES_PER_##unit + 0.5))
#define WTIMER0_UNITS(...)                  _WTIMER0_UNITS(__VA_ARGS__)

#define _WTIMER1_UNITS(unit, time)          ((uint32_t) ((time) * WTIMER1_CYCLES_PER_##unit + 0.5))
#define WTIMER1_UNITS(...)                  _WTIMER1_UNITS(__VA_ARGS__)

// force compiler to use floats for calculating times. this way, we can use MS(1.23) etc.
#define US(time)                            US, (time)
#define MS(time)                            MS, (time)
#define SEC(time)                            S, (time)

///////////////////////////////////////////////////////////////////////////////
#define CALIBRATE_FRCOSC                0x01
#define CALIBRATE_LPOSC                 0x02

void calibrate_oscillators(uint8_t flags);
///////////////////////////////////////////////////////////////////////////////

#endif /* end of include guard: TIMING_H_INCLUDED */
