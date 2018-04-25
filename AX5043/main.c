//
//  main.c
//  SPI test
//
//  Created by Filipe Pereira on 6/1/16.
//
//

#include "AX5043_SPI.h"

int main(int argc, const char * argv[]) {
    char status, version , state;
    int fd ,i;
    
    fp = fopen("/home/pi/AX5043/DEMO_TX/log.txt","w+");
    
    fd = wiringPiSPISetup(SPI_DEVICE, SPI_SPEED);
    if(fd < 0){
		fprintf(stderr, "Unable to open SPI device\n\r");
	} else {
		fprintf(fp,"SPI Initialization successful : %i\n",fd) ;
    }
    
    status = ax5043_readReg(AX_REG_PWRMODE);
    fprintf(fp,"Power mode : %02x\n",status);
    version = ax5043_readReg(AX_REG_SILICONREVISION);
    
    fprintf(fp,"silicon revision : %02x\n",version);
    
    state = ax5043_readReg(AX_REG_RADIOSTATE);
    fprintf(fp,"Radio State : %01x\n", state);
    
	//turn off receiver
	ax5043_writeReg(AX_REG_PWRMODE,PWRMODE_STANDBY);
	usleep(100);
	
	//release FIFO ports
	ax5043_writeReg(AX_REG_PWRMODE,PWRMODE_FIFOON);
	usleep(100);

	//Init Transceiver
	ax5043_init();
	
	ax5043_TX();

	//ax5043_RX();
	
	fclose(fp);
	
    return 0;
}
