from __future__ import division     #int div to float
########################################################################
# Title: Rohde & Schwarz Simple ATE example GUI
# Description:
#
#
########################################################################
# User Input Settings
########################################################################
btnWid = 12
textWindWid = 90
WaveWindWid = 55
maxCol = 6
btnRow = 20
ColorBG = "black"  #gray30
ColorFG = "green"
ColorCurs = "White"

########################################################################
### Code Start
########################################################################
#from Tkinter import *
import Tkinter as Tk
import ttk
import tkMessageBox
import tkFileDialog
END = Tk.END

#Code specific libraries
import csv
import copy
from os.path   import split
from yaVISA    import jaVisa

########################################################################
### Functions
########################################################################
class GUIData():
   def __init__(self):
      GUIData.K2_IP = "192.168.1.109"
      GUIData.K2_SCPI = "*IDN?"
      GUIData.FreqArry = ""
      GUIData.WvArry = ""
      GUIData.PwrArry = ""
      
def mnu_Out2WindLoad_Files():
   lstOutp2.delete(0,END)
   filez = tkFileDialog.askopenfilenames()
   fileList = list(filez)
   for i in fileList:
      lstOutp2.insert(END,i)
   lstOutp2.see(END)

def mnu_Out2WindLoad_Read():
   lstOutp2.delete(0,END)
   filez = tkFileDialog.askopenfilename()
   fprintf(filez)
#   for i in fileList:
#      lstOutp2.insert(END,i)
   lstOutp2.see(END)
 
def mnu_Out2WindClear():
   posi = lstOutp2.curselection()
   lstOutp2.delete(0,END)

def mnu_SaveCond():
   RSVar.K2_IP = Entry1.get()
   RSVar.K2_SCPI = Entry2.get()
   RSVar.WvArry = list(lstOutp2.get(0,END))
   RSVar.FreqArry = Entry3.get()
   RSVar.PwrArry  = Entry4.get()
   dataSave(RSVar)

def btn_Clear():
   posi = lstOutpt.curselection()
   lstOutpt.delete(0,END)
   
def btn_IDN():
   fprintf("--> *IDN?")
   K2 = jaVisa()
   K2.VISA_Open(Entry1.get())
   readStr = K2.query("*IDN?")
   fprintf("<-- " + readStr)
   K2.VISA_Close()
   
def btn_Query():
   fprintf("--> " + Entry2.get())
   K2 = jaVisa()
   K2.VISA_Open(Entry1.get())
   readStr = K2.query(Entry2.get())
   fprintf("<-- " + readStr)
   K2.VISA_Close()
   
def btn_Scan():
   K2 = jaVisa()
   InstrList = K2.jav_ResList()
   for i in InstrList:
      fprintf("   " + i)
   fprintf("[Resource List]")
   K2.VISA_Close()

def btn_SCPIList():
   K2 = jaVisa()
   K2.VISA_Open(Entry1.get())
   OutList = K2.jav_Super(['*IDN?','*IDN?','DISP:TRAC:Y:RLEV -30'])
   K2.VISA_Close()
   for Ostr in OutList:
      fprintf("   " + Ostr)
   fprintf("[SCPI LIST]")
   
def btn_Write():
   fprintf("-->" + Entry2.get())
   K2 = jaVisa()
   K2.VISA_Open(Entry1.get())
   K2.write(Entry2.get())
   K2.VISA_Close()
   
def menu_Open():
   asdf = tkFileDialog.askopenfilename()
   print(asdf)
   
def menu_Exit():
   global GUI
   #btn_SaveCond()
   GUI.quit()
   GUI.destroy()
   print("Program End")

def menu_Save():
   dataSave(RSVar)

def ArrayInput(stringIn):
   OutputList = []
   InputList = stringIn.split(",")
   for i in InputList:
      i = i.strip()
      OutputList.append(i)
   return OutputList
   
def fprintf(inStr):
   #print(inStr)
   try:
      #lstOutpt.insert(END,inStr)
      lstOutpt.insert(0,inStr)
      #lstOutpt.see(END)
      GUI.update()
   except:
      pass

def dataSave(data):
   f = open("yaVISA_GUI.dat","wb")
   f.write("HelloWorld")
   fprintf("DataSave: File Saved")

def dataLoad():
   data = 1
   try:
      f = open("yaVISA_GUI.dat","wb")
      data = f.read()
      fprintf("DataLoad: OK")
   except:
      data = GUIData()
      fprintf("DataLoad: Default")

   return data
                 
########################################################################
# Define GUI Widgets
RSVar = copy.copy(dataLoad())
GUI = Tk.Tk()                                 #Create GUI object
GUI.title("Rohde&Schwarz VISA Utility")            #GUI Title
Lbl1 = Tk.Label(GUI, text="Instrument IP")    #Create Label
Entry1 = Tk.Entry(GUI,bg=ColorBG, fg=ColorFG,insertbackground=ColorCurs) #Create Entry background
Entry1.insert(END, RSVar.K2_IP)                    #Default Value
Lbl2 = Tk.Label(GUI, text="SCPI String")      #Create Label
Entry2 = Tk.Entry(GUI,bg=ColorBG, fg=ColorFG,insertbackground=ColorCurs) #Entry Background
Entry2.insert(END, RSVar.K2_SCPI)                  #Default Value
Lbl3 = Tk.Label(GUI, text="Freq Array")       #Create Label
Entry3 = Tk.Entry(GUI,bg=ColorBG, fg=ColorFG,insertbackground=ColorCurs) #Entry Background
Entry3.insert(END, RSVar.FreqArry)                 #Default Value
Lbl4 = Tk.Label(GUI, text="Power Array")      #Create Label
Entry4 = Tk.Entry(GUI,bg=ColorBG, fg=ColorFG,insertbackground=ColorCurs) #Entry Background
Entry4.insert(END, RSVar.PwrArry)                  #Default Value
btnWaveF = Tk.Button(GUI, width=btnWid, text = "VISA Scan", command = btn_Scan)
btnWaveC = Tk.Button(GUI, width=btnWid, text = "SCPI List", command = btn_SCPIList)
btnSaveC = Tk.Button(GUI, width=btnWid, text = "*IDN?", command = btn_IDN)
btnClear = Tk.Button(GUI, width=btnWid, text = "Query", command = btn_Query)
btnRunIt = Tk.Button(GUI, width=btnWid, text = "Write", command = btn_Write)
btnQuit  = Tk.Button(GUI, width=btnWid, text = "Quit", command = menu_Exit)

########################################################################
### List Boxes
lstOutpt = Tk.Listbox(GUI, width=textWindWid,bg=ColorBG, fg=ColorFG)
srlOutpt = ttk.Scrollbar(GUI, orient=Tk.VERTICAL, command=lstOutpt.yview) #Create scrollbar S
lstOutpt.config(yscrollcommand=srlOutpt.set)        #Link scroll to lstOutpt
lstOutpt.insert(0,"Output Window")

lstOutp2 = Tk.Listbox(GUI,bg=ColorBG, fg=ColorFG,width=WaveWindWid)
srlOutp2 = ttk.Scrollbar(GUI, orient=Tk.VERTICAL, command=lstOutp2.yview) #Create scrollbar S
lstOutp2.insert(0,"SCPI Window")
for item in RSVar.WvArry:
    lstOutp2.insert(END, item)
lstOutp2.config(yscrollcommand=srlOutp2.set)        #Link scroll to lstOutp2

########################################################################
### Draw Widgets w/ Grid
Lbl1.grid(row=0,column=0,sticky=Tk.E,columnspan=1)
Lbl2.grid(row=1,column=0,sticky=Tk.E,columnspan=1)
#Lbl3.grid(row=2,column=0,sticky=Tk.E,columnspan=1)
#Lbl4.grid(row=3,column=0,sticky=Tk.E,columnspan=1)
Entry1.grid(row=0,column=1,columnspan=1)
Entry2.grid(row=1,column=1,columnspan=1)
#Entry3.grid(row=2,column=1,columnspan=1)
#Entry4.grid(row=3,column=1,columnspan=1)
btnWaveF.grid(row=btnRow,column=0)
btnWaveC.grid(row=btnRow,column=1)
btnSaveC.grid(row=btnRow,column=2)
btnClear.grid(row=btnRow,column=3)
btnRunIt.grid(row=btnRow,column=4)
btnQuit.grid(row=btnRow,column=5)

lstOutp2.grid(row=0,column=2,columnspan=4,rowspan=2, sticky=(Tk.E))
srlOutp2.grid(column=maxCol,row=0,rowspan=2,sticky=(Tk.W,Tk.N,Tk.S))     
lstOutpt.grid(row=btnRow-1,column=0,columnspan=maxCol)
srlOutpt.grid(column=maxCol,row=btnRow-1, sticky=(Tk.W,Tk.N,Tk.S))     

# *****************************************************************
# Define menu
# *****************************************************************
menu = Tk.Menu(GUI)                        #create dropdown in GUI
GUI.config(menu=menu)

fileMenu = Tk.Menu(menu)                   #create dropdown in menu
fileMenu.add_command(label="Open",command=menu_Open)
fileMenu.add_command(label="Save",command=menu_Save)
fileMenu.add_separator()
fileMenu.add_command(label="SCPI Load", command=mnu_Out2WindLoad_Read)
fileMenu.add_command(label="SCPI Clear",command=mnu_Out2WindClear)
fileMenu.add_separator()
fileMenu.add_command(label="Exit",command=menu_Exit)

editMenu = Tk.Menu(menu)                   #create dropdown in menu
editMenu.add_command(label="Edit",command=menu_Open)

menu.add_cascade(label="File",menu=fileMenu)    #add dropdown menu
menu.add_cascade(label="Edit",menu=editMenu)    #add dropdown menu

# *****************************************************************
# Start Program
# *****************************************************************
GUI.mainloop()       #Display window