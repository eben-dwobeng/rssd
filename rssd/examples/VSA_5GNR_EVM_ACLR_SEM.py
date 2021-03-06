###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : 5GNR Measurements
### Creatd : mclim, 2019.12.11
###############################################################################
### User Entry
###############################################################################
instru_ip   = '192.168.1.109'
centerFreq  = 15e9    #GHz
SEMFreqmax  = 2.345e9
SEMFreqmin  = 2.900e9

###############################################################################
### Code Overhead: Import and create objects
###############################################################################
# import timeit
from rssd.VSA.NR5G_K144     import VSA
from rssd.FileIO            import FileIO

OFile = FileIO().makeFile(__file__)
FSW   = VSA().jav_Open(instru_ip,OFile)                     #Create Object

###############################################################################
### Code Start
###############################################################################
OFile.write('EVM,FreqError,ChPwr,Adj-,Adj+,SEM')            #Data Header

FSW.Set_Freq(centerFreq)
FSW.Set_SweepCont(0)

###########################
### EVM
###########################
FSW.Init_5GNR()
FSW.Init_5GNR_Meas('EVM')
FSW.Set_InitImm()
EVM = FSW.query(':FETC:CC1:ISRC:FRAM:SUMM:EVM:ALL:AVER?')
EVM = EVM + ',' + FSW.query(':FETC:CC1:ISRC:FRAM:SUMM:FERR:AVER?')

###########################
### ACLR
###########################
FSW.Init_5GNR_Meas('ACLR')
FSW.Set_InitImm()
ACLR = FSW.Get_5GNR_ACLR()

FSW.Init_5GNR_Meas('ESP')
FSW.Set_Span(SEMFreqmax+SEMFreqmin)
print(centerFreq - SEMFreqmin)
print(centerFreq + SEMFreqmax)

FSW.write(f':SENS:ESP1:RANG1:FREQ:STAR -{SEMFreqmin}')
FSW.write(f':SENS:ESP1:RANG5:FREQ:STOP {SEMFreqmax}')
FSW.Set_InitImm()
SEM  = FSW.Get_5GNR_SEM()

"""
:FETC:CC1:ISRC:FRAM:SUMM:EVM:ALL:AVER?
:FETC:CC1:ISRC:FRAM:SUMM:EVM:PCH:AVER?
:FETC:CC1:ISRC:FRAM:SUMM:EVM:PSIG:AVER?
:FETC:CC1:ISRC:FRAM:SUMM:FERR:AVER?
:FETC:CC1:ISRC:FRAM:SUMM:SERR:AVER?
:FETC:CC1:ISRC:FRAM:SUMM:IQOF:AVER?
:FETC:CC1:ISRC:FRAM:SUMM:GIMB:AVER?
:FETC:CC1:ISRC:FRAM:SUMM:QUAD:AVER?
:FETC:CC1:ISRC:FRAM:SUMM:OSTP:AVER?
:FETC:CC1:ISRC:FRAM:SUMM:POW:AVER?
:FETC:CC1:ISRC:SUMM:CRES:AVER?
"""
OFile.write (f'{EVM},{ACLR},{SEM}')

###############################################################################
### Cleanup Automation
###############################################################################
FSW.jav_Close()
