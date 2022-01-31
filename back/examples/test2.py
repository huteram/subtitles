from tkinter import *

class AndorCameraSDK():
    def __init__(self, master):
        print('SDK Init') # Show that AndorCameraSDK.__init__ runs
        self.master = master         # Save reference to master

    def LiveAcquisition(self):
        print('SDK LiveAcquisition') # Show that AndorCameraSDK.LiveAcquisition runs
        pBuf = 'Some data'       # Dummy data
        self.master.LivePlot() # Call instance of AndorCameraGUI.LivePlot

class AndorCameraGUI():
    def __init__(self):
        print('GUI Init') # Show that AndorCameraGUI.__init__ runs

    def LiveImageGUI(self):
        print('GUI LiveImageGUI') # Show that AndorCameraGUI.LiveImageGUI runs
        self.camera = AndorCameraSDK(self) # Create instance of AndorCameraSDK
        self.camera.LiveAcquisition() # Call AndorCameraSDK.LiveAcquisition

    def LivePlot(self):
        print('GUI LivePlot') # Show that AndorCameraGUI.LivePlot runs

app = AndorCameraGUI()
app.LiveImageGUI()  # Instead of pressing a button
