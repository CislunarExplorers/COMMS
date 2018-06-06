#include "timing.h"

///////////////////////////////////////////////////////////////////////////////
void calibrate_oscillators(uint8_t flags)
{
    if ((flags & CALIBRATE_LPOSC) || (flags & CALIBRATE_FRCOSC)) {
        AX5043_PINFUNCPWRAMP = 0x07; // output TCXO enable on PWRAMP pin
        AX5043_PWRMODE = AX5043_PWRSTATE_XTAL_ON;
        AX5043_PINFUNCSYSCLK = 0x06; // fXTAL/4
#pragma save
#pragma disable_warning 126 // disable 'unreachable code' warnings in SDCC
        // change frequency here when using an oscillator != 48MHz!
        setup_osc_calibration_const(12000000UL, CLKSRC_RSYSCLK);
#pragma restore
        LPOSCKFILT = 0x0800;

        OSCCALIB = 0;
        if (flags & CALIBRATE_FRCOSC)
            OSCCALIB |= 0x01; // enable calibration interrupts
        if (flags & CALIBRATE_LPOSC)
            OSCCALIB |= 0x02; // enable calibration interrupts
    }

    // calibrate internal oscillators to the radio clock (which is tied to an XTAL/TCXO)
    // ?TODO: is this true?
    if ((flags & CALIBRATE_LPOSC) || (flags & CALIBRATE_FRCOSC)) {
        // wait for a couple of calibration cycles to get close to the desired frequency
        uint8_t frc = 0, lpc = 0;

        if (flags & CALIBRATE_FRCOSC)
            frc = 32;

        if (flags & CALIBRATE_LPOSC)
            lpc = 32;

        for (;;) {
            uint8_t oc = OSCCALIB;
            if (oc & 0x40) {
                FRCOSCFREQ1;
                switch (frc) {
                case 29:
                case 26:
                case 23:
                case 20:
                case 17:
                case 14:
                    FRCOSCKFILT >>= 1;

                // fall through
                default:
                    --frc;
                    break;

                case 0:
                    break;
                }
                if (!frc && !lpc)
                    break;
            }
            if (oc & 0x80) {
                LPOSCFREQ1;
                switch (lpc) {
                case 29:
                case 26:
                case 23:
                case 20:
                case 17:
                case 14:
                    LPOSCKFILT >>= 1;

                // fall through
                default:
                    --lpc;
                    break;

                case 0:
                    break;
                }
                if (!frc && !lpc)
                    break;
            }
            oc = IE & 0x80;
            EA = 0;
            IE_5 = 1; // clock management interrupt
            enter_standby();
            IE_5 = 0;
            IE |= oc;
        }

        OSCCALIB = 0x00;
        LPOSCCONFIG = 0x01;
        FRCOSCCONFIG = 0x00;

        if (flags & CALIBRATE_FRCOSC)
            LOG(STR("FRC Oscillator Calibration: 0x"), HEX8(FRCOSCFREQ1), HEX8(FRCOSCFREQ0), NL());

        if (flags & CALIBRATE_LPOSC)
            LOG(STR("LP Oscillator Calibration: 0x"), HEX8(LPOSCFREQ1), HEX8(LPOSCFREQ0), NL());
    }
}
///////////////////////////////////////////////////////////////////////////////
