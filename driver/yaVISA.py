#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Yet Another VISA wrapper
### Author:  Martin C Lim
### Date:    2017.09.01
### Requird: python -m pip install pyvisa
import visa
import time

class RSVisa:    
   ### Rohde & Schwarz VISA Class
   ### Instrument Common functions. 
   def __init__(self):
      self.dataIDN = ""
      self.dLastErr = " "
      pass
      
   def VISA_Clear(self):
      self.K2.clear()

   def VISA_Close(self):
      try:
         self.VISA_ClrErr()
         self.K2.close()
      except:
         pass

   def VISA_ClrErr(self):
      while True:
         RdStr = self.query("SYST:ERR?").strip()
         #print("VISA_ClrErr  :"+RdStr)
         RdStrSplit = RdStr.split(',')
         if RdStrSplit[0] == "0":
            break
         else:
            self.dLastErr = RdStr
            print("VISA_ClrErr  : %s ERR:%s"%(self.K2,RdStr))
         
   def VISA_IDN(self):
      self.dataIDN = self.query("*IDN?").strip()
      return self.dataIDN
            
   def VISA_OPC_Wait(self, InCMD):
      start_time = time.time()
      self.write("*ESE 1")		            #Event Status Enable
      self.write("*SRE 32")		         #ServiceReqEnable-Bit5:Std Event
      self.write(InCMD + ";*OPC")	      #Initiate Read.  *OPC will trigger ESR
      #print ('   OPC Wait: ' +InCMD)
      read = "0"
      while (int(read) & 1) != 1:            #Loop until done
         try:
            read = self.query("*ESR?").strip()	   #Poll EventStatReg-Bit0:Op Complete		
         except:
            print("VISA_OPC_Wait:*ESR? Error")
         time.sleep(0.5)
         delta = (time.time() - start_time)
         if delta > 300:
            print("VISA_OPC_Wait: timeout")
            break
      print('VISA_OPC_Wait: %0.2fsec'%(delta))
      
   def VISA_Open(self, IPAddr, file='none.txt'):
      #*****************************************************************
      #*** Open VISA Connection
      #*****************************************************************
      #  VISA: 'TCPIP0::'+IP_Address+'::INSTR'
      #  VISA: 'TCPIP0::'+IP_Address+'::inst0'
      #  VISA: 'TCPIP0::'+IP_Address+'::hislip0'
      #  VISA: 'TCPIP0::'+IP_Address+'::hislip0::INSTR'
      rm = visa.ResourceManager()      #Create Resource Manager
      rmList = rm.list_resources()     #List VISA Resources
      try:
         self.K2 = rm.open_resource('TCPIP::'+IPAddr+'::inst0::INSTR')   #Create Visa Obj
         self.K2.timeout = 10000                  #Timeout, millisec
         self.VISA_IDN()
         print (self.dataIDN)
         try:
            file.write(self.dataIDN + "\n")
         except:
            pass
         self.VISA_ClrErr()
      except:
         print ('VISA: Can not open:' + IPAddr)
         self.K2 = 'NoVISA'
      return self.K2

   def VISA_Reset(self):
      self.write("*RST;*CLS;*WAI")

   def query(self,cmd):
      return self.K2.query(cmd).strip()
      
   def write(self,cmd):
      self.K2.write(cmd)


if __name__ == "__main__":
   M2 = RSVisa()
   M2.VISA_Open("192.168.1.109")
   #M2.VISA_Reset()
   #M2.K2.write(":SOUR1:FREQ:CW 15GHZ")
   M2.VISA_IDN()
   M2.write(":FREQ:CENT 12GHZ")
   M2.write("INIT:CONT OFF")
   print(M2.query("Freq:CENT?"))
   M2.VISA_OPC_Wait("INIT:IMM")
   M2.VISA_Close()
   print(M2.dLastErr)

