// filename - query.c
// Rev.A
// MS-DOS
#include <conio.h>
#include <dos.h>
#include <stdio.h>
#include <string.h>
#include "decl.h"

#define HIWORD(l) ((unsigned int)((((unsigned long)(l)) >> 16) & 0xFFFF))
#define LOWORD(l) ((unsigned int)(unsigned long)(l))

// example commands
char cQueryCmd[] = "@\x51\r\n";
char cUnitsCmd[] = "@\x27\r\n";

// misc vars
char cGPIBBuffer[32];
int nBoardID;
int nDeviceID;
union _REGS callregs, returnregs;

// misc funcs
void pause(int);
void Status(char *);
void main(int argc, char *argv[])
{
    // locate & initialize the GPIB board
    nBoardID = ibfind("GPIB0");
    Status("Get board ID...");

    ibsic(nBoardID);
    Status("Make board CIC...");

    // locate & initialize the GPIB device
    nDeviceID = ibfind("DEV4");
    Status("Get device ID...");

    ibclr(nDeviceID);
    Status("Reset device & bus...");
    // loop until the key is pressed
    while (!kbhit())
    {

        if (!(ibsta & ERR))
        {
            ibwrt(nDeviceID, (char *)cQueryCmd, strlen(cQueryCmd));
            pause(25);
            Status("Querying...");

            if (!(ibsta & ERR))
            {
                ibrd(nDeviceID, cGPIBBuffer, 23);
                Status("Reading...");
                printf(cGPIBBuffer);
            }
        }
        if (!(ibsta & ERR))
        {
            ibwrt(nDeviceID, (char *)cUnitsCmd,
                  strlen(cUnitsCmd));
            pause(25);
            Status("Changing units...");
        }
        if (ibsta & ERR)
        {
            ibclr(nDeviceID);
            pause(25);
        }
    }
}
// reports gpib status & err
void Status(char *message)
{
    strcat(message, '\0');
    printf("%s\nIBSTA=0x%04X <", message, ibsta);
    if (ibsta & ERR)
        printf(" ERR");
    if (ibsta & TIMO)
        printf(" TIMO");
    if (ibsta & END)
        printf(" END");
    if (ibsta & SRQI)
        printf(" SRQI");
    if (ibsta & RQS)
        printf(" RQS");
    if (ibsta & CMPL)
        printf(" CMPL");
    if (ibsta & LOK)
        printf(" LOK");
    if (ibsta & REM)
        printf(" REM");
    if (ibsta & CIC)
        printf(" CIC");
    if (ibsta & ATN)
        printf(" ATN");
    if (ibsta & TACS)
        printf(" TACS");
    if (ibsta & LACS)
        printf(" LACS");
    if (ibsta & DTAS)
        printf(" DTAS");
    if (ibsta & DCAS)
        printf(" DCAS");
    printf(" > ");
    if (ibsta & ERR)
    {
        printf("IBERR=0x%04X", iberr);
        if (iberr == EDVR)
            printf(" EDVR <DOS Error>");
        if (iberr == ECIC)
            printf(" ECIC <Not CIC>");
        if (iberr == ENOL)
            printf(" ENOL <No Listener>");
        if (iberr == EADR)
            printf(" EADR <Address error>");
        if (iberr == EARG)
            printf(" EARG <Invalid argument>");
        if (iberr == ESAC)
            printf(" ESAC <Not Sys Ctrlr>");
        if (iberr == EABO)
            printf(" EABO <Op. aborted>");
        if (iberr == ENEB)
            printf(" ENEB <No GPIB board>");
        if (iberr == EOIP)
            printf(" EOIP <Async I/O in prg>");
        if (iberr == ECAP)
            printf(" ECAP <No capability>");
        if (iberr == EFSO)
            printf(" EFSO <File sys. error>");
        if (iberr == EBUS)
            printf(" EBUS <Command error>");
        if (iberr == ESTB)
            printf(" ESTB <Status byte lost>");
        if (iberr == ESRQ)
            printf(" ESRQ <SRQ stuck on>");
        if (iberr == ETAB)
            printf(" ETAB <Table Overflow>");
    }
    printf("\n");
}
//suspend processes for howmany milliseconds
void pause(int howmany)
{
    callregs.h.ah = 0x86;
    callregs.x.cx = HIWORD(1000 * (long)howmany);
    callregs.x.dx = LOWORD(1000 * (long)howmany);
    _int86(0x15, &callregs, &returnregs);
}