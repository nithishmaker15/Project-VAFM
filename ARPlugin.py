"""
 <AR Plugin used for Fiducial Markers>
Copyright (C) 2023  Nithish Murugavenkatesh

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

import cv2
import numpy as np
from ffpyplayer.player import MediaPlayer
import serial
from pygrabber.dshow_graph import FilterGraph
import PySimpleGUI as sg
import time
cv2.setUseOptimized(True)
# Import of Required Models
sg.theme('Dark Purple 4')
graph = FilterGraph()
#s = serial.Serial("COM3",9600,timeout = .1)
liframe = [
    [sg.Text('Frames Per Second', font='Any 20'), sg.Text('0', font='Any 20', key = 'fps')],
    
    [sg.Text('Type of ArUCo Marker. ', font='Any 20'), sg.Text('4 x 4 with 250 Pixels', font='Any 20', key = 'f')],
    
    ]
rframe = [
    [sg.Image(r'', key = 'img')],
    [sg.Text('Webcam Input', font='Any 20')],
    [sg.Frame('Statistics', layout = liframe)]
    
    
    ]
R  = [
    [sg.Frame('Augmentation', layout = rframe)]
    
            ]
layout = [
    [sg.Column(R, element_justification = 'c'),sg.VSeparator()
    ]
    ]


def Augment(bbox, img, imgAug, drawId = True, d=0):

# The Augmentation of the ARUCO markers 
    if imgAug is not None and bbox is not None:
        v1 = bbox[0][0][0], bbox[0][0][1]
        v2 = bbox[0][1][0], bbox[0][1][1]
        xv1 = bbox[0][2][0], bbox[0][2][1]
        xv2 = bbox[0][3][0], bbox[0][3][1]
        h, w, c = imgAug.shape
        xArray = np.array([v1, v2, xv1, xv2])
        yArray = np.float32([[d,d], [w,d], [w,h], [d,h]])
        matrix, stateIO = cv2.findHomography(yArray, xArray)
        imgout = cv2.warpPerspective(imgAug, matrix, (img.shape[1], img.shape[0]))
        cv2.fillConvexPoly(img, xArray.astype(int), (0, 0, 0))
        imgout = img + imgout
        return imgout
    else:
        return img
# Main Wrapper Class of ARPlugin
class ARPlugin:
    def __init__(self, mtx, dist ):
        
        self.dic = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_250)
        self.parameters =  cv2.aruco.DetectorParameters_create()
        
        self.mtx = mtx
        self.dist = dist
        
        

    def createCameraObj(self):
        def select_camera(last_index):
            number = 0
            hint = "Select a camera (0 to " + str(last_index) + "): "
            try:
                number = int(input(hint))
        
            except Exception :
                print("It's not a number!")
                number=0

            if number > last_index:
                print("Invalid number! Retry!")
                number=0

            return number
        device_list = graph.get_input_devices()
        index = 0

        for name in device_list:
           print(str(index) + ': ' + name)
           index += 1
           last_index = index - 1

        if last_index < 0:
           print("No device is connected")
           exit()

        self.cameranum = select_camera(last_index)
        self.cam = cv2.VideoCapture(self.cameranum)
    def RunPlugin_BLOCKING(self, path, DEBUG, TWODAUGMENT):
        window = sg.Window('Project VAFM - Nithish Murugavenkatesh',
                       layout, location=(0, 0),no_titlebar=False,margins=(0,0),grab_anywhere=True, finalize=True)
        self.path = path
        self.aug = cv2.VideoCapture(self.path)
        if TWODAUGMENT == True:
            self.player = MediaPlayer(self.path)
            self.player.set_pause(True)
        
        while True:
            
            self.dump, self.frame = self.cam.read()
            
        
            
            
            
            self.augments = self.frame.copy()
            
            self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            self.corners, self.ids, self.rejects= cv2.aruco.detectMarkers(self.gray, self.dic, parameters=self.parameters)
            if len(self.corners)!=0 :
                #s.write(bytes("1",'utf-8'))
                print(self.ids[0])
                
                
                
                
                for self.i in range(0, len(self.ids)):
                    self.rvec, self.tvec, self.pts= cv2.aruco.estimatePoseSingleMarkers(self.corners[self.i], 0.02, self.mtx,self.dist)
                    
                    (self.rvec - self.tvec).any()
                    cv2.aruco.drawDetectedMarkers(self.frame, self.corners)
                    if self.i == 0:
                        self.dump2, self.overlay = self.aug.read()
                        
                        if TWODAUGMENT == True:
                            self.augments = Augment(self.corners[self.i],self.augments, self.overlay)
                            self.player.set_pause(False)

                    
                        
                    cv2.drawFrameAxes(self.frame, self.mtx, self.dist, self.rvec, self.tvec, 0.01)

            

            if DEBUG == True:
                #cv2.imshow('DODO SYSTEM - OPERATIONAL', self.frame)
                pass
            #cv2.imshow('DODO SYSTEM - OPERATIONAL (AUGMENTS)', self.augments)
            
        
            
            imgbytes = cv2.imencode('.png', self.augments)[1].tobytes()
            window["img"].update(data=imgbytes)
            window.refresh()
            cv2.waitKey(1)
            
            


        self.cam.release()
        cv2.destroyAllWindows()




            
                    
                    
                

        
        
        
        
