#
#Lynx Fundus Camera software. 
#Copyright WWW.OICO.CO.UK 2016. 
#
#
#The software uses the following libraries:
#Tkinter for the GUI.
#Pylon 5 for image preview and capture
#use python pexpect to interact with the C++ pylon program
#
#arduino virtual gpio for LED and button control
#img2dcm library to generate the DICOM images
#pydicom to add attributes to DICOM file
# 
#use ttk.notebook function to add tabs. 
# This version of the software is for use on ubuntu and UVC camera with arduino nano v3
#camera trigger via bluetooth button with dual volume up and volume down function. 
#XF86AudioLowerVolume and XF86AudioRaiseVolume on keycode 122 and 123 . find the keycode using xev application.
#desktop icon for fundus camera is called "fundus camera" and can be copied to desktop for ease of access


import Tkinter
from Tkinter import *
import ttk 
from ttk import *
import tkFileDialog
import time, threading
from time import sleep
import datetime
import sys, subprocess, os
import cPickle as pickle
#for controlling arduino
import virtGPIO as GPIO
#import the pydicom library to edit the DICOM file elements
import dicom
#import pexpect to interact with C++ camera application
import pexpect


#using the arduino. 
#connect the LED in the following fashion:
#white LED - ground/resistor to GND and positive to D6 and D7
#IR LED - ground / resistor to GND and positive to D5
ir=5
white1=6
white2=7
white3=8
GPIO.setup(ir,GPIO.OUT) #IR Led
GPIO.setup(white1,GPIO.OUT) #White1 Led
GPIO.setup(white2,GPIO.OUT) #White2 Led
GPIO.setup(white3,GPIO.OUT) #White3 Led

#turn off autorepeat to remove duplicate images
os.system('xset r off')


#starting the main user interface
root = Tk()
#for large HD screen use below
root.geometry('400x420+900+1')

root.title("OICO Fundus Camera")
root.wm_iconbitmap('@'+'logo-1.xbm')
#make the GUI always in foreground
root.lift()

#The three tabs of the user interface
note=ttk.Notebook(root)
tab1=ttk.Frame(note);
tab1.columnconfigure(0, weight=1)
tab1.rowconfigure(0, weight=1)
tab1.grid(column=3, row=20, sticky=(N,W,E,S))
tab2=ttk.Frame(note);
tab2.grid(column=5, row=20, sticky=(N,W,E,S))
tab3=ttk.Frame(note);
tab3.grid(column=3, row=20, sticky=(N,W,E,S))
tab4=ttk.Frame(note);
tab4.grid(column=3, row=20, sticky=(N,W,E,S))
tab5=ttk.Frame(note);
tab5.grid(column=3, row=20, sticky=(N,W,E,S))
note.add(tab1, text='Patient Details')
note.add(tab2, text='Camera')
note.add(tab3, text='Setup')
note.add(tab4, text='Help')
note.add(tab5, text='About')
note.pack()


#tab1 The Patient details

#Name
forenameval = StringVar()
ttkforenameval = ttk.Entry(tab1, textvariable=forenameval).grid(column=1, row=0)
forenameLabel=ttk.Label(tab1, text="Forename").grid(column=0, row=0)
surnameval = Tkinter.StringVar()
ttksurnameval = ttk.Entry(tab1, textvariable=surnameval).grid(column=1, row=1)
surnameLabel=ttk.Label(tab1, text="Surname").grid(column=0, row=1)
s1=ttk.Separator(tab1, orient=HORIZONTAL).grid(row=2, columnspan=3, stick="ew", pady=5, padx=5)

#gender details
genderlabel=ttk.Label(tab1, text="Gender").grid(column=0, row=3)
genderval=StringVar()
genderMale=ttk.Radiobutton(tab1, text='Male', variable=genderval, value='M').grid(column=1,row=3)
genderFemale=ttk.Radiobutton(tab1, text='Female', variable=genderval, value='F').grid(column=2,row=3)
s2=ttk.Separator(tab1, orient=HORIZONTAL).grid(row=4, columnspan=3, stick="ew", pady=5, padx=5)

dateofbirthlabel=ttk.Label(tab1, text="Date of Birth").grid(column=0, row=5)
dateofbirthlabelD=ttk.Label(tab1, text="Day").grid(column=0, row=6)
dateofbirthD=StringVar()
ttkdateofbirthD = Spinbox(tab1,from_=1.0, to=31, textvariable=dateofbirthD).grid(column=1, row=6)
dateofbirthlabelM=ttk.Label(tab1, text="Month").grid(column=0, row=7)
dateofbirthM=StringVar()
ttkdateofbirthM = Spinbox(tab1,from_=1.0, to=12, textvariable=dateofbirthM).grid(column=1, row=7)
dateofbirthlabelY=ttk.Label(tab1, text="Year").grid(column=0, row=8)
dateofbirthY=StringVar()
ttkdateofbirthY = Spinbox(tab1,from_=1900.0, to=2050.00, textvariable=dateofbirthY).grid(column=1, row=8)
#ttk.Label(tab1, textvariable=dateofbirth).grid(column=1,row=9)
s3=ttk.Separator(tab1, orient=HORIZONTAL).grid(row=10, columnspan=3, stick="ew", pady=5, padx=5)

#Patient Number
patientID = StringVar()
ttkpatientID = ttk.Entry(tab1, textvariable=patientID).grid(column=1, row=11)
patientIDLabel=ttk.Label(tab1, text="Patient ID").grid(column=0, row=11)

#Series number
seriesNumber = StringVar()
ttkSeriesNumber = ttk.Entry(tab1, textvariable=seriesNumber).grid(column=1, row=12)
seriesNumberLabel=ttk.Label(tab1, text="Series Number").grid(column=0, row=12)

#Study ID
StudyID = StringVar()
ttkStudyID = ttk.Entry(tab1, textvariable=StudyID).grid(column=1, row=13)
StudyIDLabel=ttk.Label(tab1, text="Study ID").grid(column=0, row=13)

#Patient Comments
PatientComments = StringVar()
ttkPatientComments = ttk.Entry(tab1, textvariable=PatientComments).grid(column=1, row=14)
PatientCommentsLabel=ttk.Label(tab1, text="Patient Comments").grid(column=0, row=14)



#Selecting the eye
eyeLabel=ttk.Label(tab2, text="Select eye").grid(column=0, row=0)
eyeLR=StringVar()
rEye=ttk.Radiobutton(tab2, text='Right Eye', variable=eyeLR, value='RightEye').grid(column=0, row=1)
lEye=ttk.Radiobutton(tab2, text='Left Eye', variable=eyeLR, value='LeftEye').grid(column=2, row=1)


#tab2 camera operation
def camera_start():
	GPIO.output(ir,1)  #start infrared 
	GPIO.output(white1,0) #stop white1
	GPIO.output(white2,0) #stop white2
	GPIO.output(white3,0) #stop white3
#	subprocess.call(["rm", "1.png","2.png"])
	cam=pexpect.spawn('sudo ./Grab', timeout=400)
	cam.expect('XXXXXX')
	GPIO.output(ir,0)  #stop infrared 
	GPIO.output(white1,1) #start white1
	GPIO.output(white2,1) #start white2
	GPIO.output(white3,1) #start white3
	sleep(0.4)
	GPIO.output(white1,0)   #stop white1
	GPIO.output(white2,0)   #stop white2
	GPIO.output(white3,0)   #stop white3
	sleep(2)
	#now take the generated images and combine them.
	process_images()

#start camera start button
camera_start_button = ttk.Button(tab2, text='Camera Start', command=camera_start).grid(column=4, row=3)
s20=ttk.Separator(tab2, orient=HORIZONTAL).grid(row=4, columnspan=5, stick="ew", pady=5, padx=5)

def camera_setup():
#	setup=pexpect.run('/opt/pylon5/bin/PylonViewerApp')
	subprocess.call(["/opt/pylon5/bin/PylonViewerApp"])

# camera setup button
camera_setup_button = ttk.Button(tab2, text='Camera Setup', command=camera_setup).grid(column=2, row=3)
s20=ttk.Separator(tab2, orient=HORIZONTAL).grid(row=4, columnspan=5, stick="ew", pady=5, padx=5)


#tab2 toggle LED illumination
def led_illumination_on():
	if led_illumination_string.get() == 'IR':
                print "IR" 
                GPIO.output(ir,1)  #start infrared 
		GPIO.output(white1,0) #stop white1
		GPIO.output(white2,0) #stop white2
		GPIO.output(white3,0) #stop white3
        elif led_illumination_string.get() == 'WHITE':
                print "WHITE"
                GPIO.output(ir,0)  #stop infrared 
		GPIO.output(white1,1)   #start white1
		GPIO.output(white2,1)   #start white2
		GPIO.output(white3,1)   #start white3
	else :
		print "OFF"
                GPIO.output(ir,0)  #stop infrared 
		GPIO.output(white1,0)   #stop white
		GPIO.output(white2,0)   #stop white
		GPIO.output(white3,0)   #stop white

#Illumination LED control buttons
illuminationLabel=ttk.Label(tab2, text='LED illumination').grid(column=0, row=11, columnspan=2)
led_illumination_string=StringVar()
led_illumination_on_btn =ttk.Radiobutton(tab2, text='IR', variable=led_illumination_string, value='IR', command=led_illumination_on).grid(column=2, row=11)
led_illumination_on_btn =ttk.Radiobutton(tab2, text='White', variable=led_illumination_string, value='WHITE', command=led_illumination_on).grid(column=3, row=11)
led_illumination_on_btn =ttk.Radiobutton(tab2, text='OFF', variable=led_illumination_string, value='OFF', command=led_illumination_on).grid(column=4, row=11)
s23=ttk.Separator(tab2, orient=HORIZONTAL).grid(row=12, columnspan=5, stick="ew", pady=5, padx=5)


#function to exit from program
def quit():
	os.system('xset r on')
	print "OICO Fundus Camera program exiting. goodbye"
	sys.exit(0)

#button to end program
camera_settings_button = ttk.Button(tab2, text='Quit', command=quit).grid(column=2, row=13)


#Sequence for picture capture set variables
tempIDjpg = StringVar()
tempIDdcm = StringVar()
tempIDdt = StringVar()

#get current home folder and set image folder
homeFolder=os.path.expanduser('~') + '/images/'



#function for capturing images
def process_images():
	tempIDdt.set(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))
	tempID= surnameval.get() + '_' + forenameval.get() + '_' + dateofbirthD.get() + dateofbirthM.get() + dateofbirthY.get() + '_' + patientID.get() + '_' + eyeLR.get() + '_' + genderval.get() + '_' + tempIDdt.get()
	sleep(10)
	#if combining two greyscale images
#	subprocess.call(["convert", "1.png","2.png","3.png", "-channel", "RGB", "-combine", homeFolder + tempID +'.jpg'])
	#if combining two colour images
	subprocess.call(["enfuse", "1.png","2.png","3.png","4.png","-o", homeFolder + tempID +'.jpg'])
	#Sequence for saving dicom file
	tempIDjpg.set(homeFolder + tempID + '.jpg')
	tempIDdcm.set(homeFolder + tempID + '.dcm')
	if imageVersion.get() == 'JD':
		dicomout()
	elif imageVersion.get() == 'D':
		dicomout()
		time.sleep(2)
		subprocess.call(["rm", tempIDjpg.get()])


#method for generating the dicom file
def dicomout():
	subprocess.call(["img2dcm", tempIDjpg.get(), tempIDdcm.get()])
	ds=dicom.read_file(tempIDdcm.get())
	#generating initial DICOM file with the SOP Class UID for ophthalmic photos and OICO unique ROOT ID. 
	ds.SOPClassUID="1.2.840.10008.5.1.4.1.1.77.1.5.1"
	ds.SOPInstanceUID="1.2.840.10008.5.1.4.1.1.77.1.5.1"+tempIDdt.get()
	ds.StudyDate=datetime.datetime.now().strftime("%Y-%m-%d")
	ds.StudyTime=datetime.datetime.now().strftime("%H:%M:%S")
	ds.PatientsName=forenameval.get() + " " + surnameval.get()
	ds.UID="1.2.826.0.1.3680043.9.3918"
	ds.PatientBirthDate=dateofbirthY.get() + dateofbirthM.get() + dateofbirthD.get()
	ds.PatientSex=genderval.get()
	ds.PatientComments=PatientComments.get()
	ds.StudyID=StudyID.get()
	ds.SeriesNumber= seriesNumber.get()
	ds.ReferringPhysiciansName= PhysicianName.get()
	ds.OperatorsName=OperatorName.get()
	ds.InstitutionName=InstitutionName.get()
	ds.InstitutionAddress=InstitutionAddress.get()
	ds.save_as(tempIDdcm.get())


#Taking picture sequence APS including flash button
#picCaptureLabel=ttk.Label(tab2, text='Capture Picture').grid(column=0, row=13, columnspan=3)
#picCapture_button = ttk.Button(tab2, text='Capture', command=picCapture_start).grid(column=4, row=13)


#Tab 3 setup
#Selecting image output versions
imageVersion=StringVar()
InstitutionName = StringVar()
InstitutionAddress = StringVar()
OperatorName = StringVar()
PhysicianName = StringVar()
#loading from pickled saved settings
pkl_file=open('settings.pkl', 'rb')
SAVED_SETTING=pickle.load(pkl_file)
pkl_file.close()
imageVersion.set(SAVED_SETTING[0])
InstitutionName.set(SAVED_SETTING[1])
InstitutionAddress.set(SAVED_SETTING[2])
OperatorName.set(SAVED_SETTING[3])
PhysicianName.set(SAVED_SETTING[4])

imageversionLabel=ttk.Label(tab3, text="Select image output").grid(column=0, row=0)
jpeganddicom=ttk.Radiobutton(tab3, text='JPEG & DICOM', variable=imageVersion, value='JD').grid(column=1, row=0, stick="nesw")
jpegonly=ttk.Radiobutton(tab3, text='JPEG Only', variable=imageVersion, value='J').grid(column=1, row=1, stick="nesw")
dicomonly=ttk.Radiobutton(tab3, text='DICOM Only', variable=imageVersion, value='D').grid(column=1, row=2, stick="nesw")

#Institution and operator details
institutionlabel=ttk.Label(tab3, text='Institution and Operator details').grid(column=0, row=4)
ttkInstitutionName= ttk.Entry(tab3, textvariable=InstitutionName).grid(column=1, row=5)
InstitutionNameLabel=ttk.Label(tab3, text="Institution Name").grid(column=0, row=5)

ttkInstitutionAddress= ttk.Entry(tab3, textvariable=InstitutionAddress).grid(column=1, row=6)
InstitutionAddressLabel=ttk.Label(tab3, text="Institution Address").grid(column=0, row=6)

ttkOperatorName= ttk.Entry(tab3, textvariable=OperatorName).grid(column=1, row=7)
OperatorNameLabel=ttk.Label(tab3, text="Operator Name").grid(column=0, row=7)

ttkPhysicianName= ttk.Entry(tab3, textvariable=PhysicianName).grid(column=1, row=8)
PhysicianNameLabel = ttk.Label(tab3, text="Physician Name").grid(column=0, row=8)

def saveSettings():
	SAVED_SETTINGS = [imageVersion.get(), InstitutionName.get(), InstitutionAddress.get(), OperatorName.get(), PhysicianName.get()]
	output = open('settings.pkl', 'wb')
	pickle.dump(SAVED_SETTINGS, output)
	output.close()

#saving settings for tab3 using pickle
savesettings_button = ttk.Button(tab3, text='Save Settings', command=saveSettings).grid(column=1, row=10)


#tab4 with help
helpLabel=ttk.Label(tab4, text='Operating Instructions for illumination and optics\n').grid(column=0, row=0, stick="nesw")
helpText=ttk.Label(tab4, text='The operator sequence is as follows.\n 1- Verify that settings are correct.\n 2-Enter the patient details\n3-Go to camera tab and click on preview button twice\n4-Use the focus to focus the patient eye\n5-Take an image by clicking the capture button or clicking the \nphysical trigger\n6-The images are saved automatically under the images folder\n7-Note that JPEG images do NOT save patient and other\n information DICOM is recommended').grid(column=0, row=1, stick="nesw")

#tab5 about
aboutLabel=ttk.Label(tab5, text='This fundus camera was developed and produced by\n\n Ophthalmic Instrument Company (c) 2015\n London, United Kingdom\n\n\n\n Contact Details for customer support can be found on\n www.oico.co.uk').grid(column=0, row=0)
logoimage=PhotoImage(file='logo-1.ppm')
helpImageLabel=ttk.Label(tab5, image=logoimage).grid(column=0, row=1, stick="s")

#looping the main Tkinter user interface
root.mainloop()
