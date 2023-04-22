import os
import json
from datetime import datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.camera import Camera
import cv2

Builder.load_file('attend_menu.kv')

class AttendMenu(Screen):
    date_input = ObjectProperty(None)
    result_label = ObjectProperty(None)

    def scan_qr_code(self):

        # check if date input is empty
        if not self.date_input.text:
            self.result_label.text = 'Please enter a date'
            return
        
        # create folder for lecture if it doesn't exist
        lecture_folder = 'lectures/{}'.format(self.date_input.text)
        if not os.path.exists(lecture_folder):
            os.makedirs(lecture_folder)
        
        # create json store if it doesn't exist
        attendance_file = '{}/attendance.json'.format(lecture_folder)
        json_store = JsonStore(attendance_file) 
        
        # request camera and storage permissions
        from android.permissions import request_permissions, Permission
        request_permissions([
            Permission.CAMERA,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.READ_EXTERNAL_STORAGE
        ])
        # capture image from camera
        cam = Camera(play=False, index=1)
        cam.play = True
        cam.texture_update()
        texture = cam.texture
        texture_size = list(texture.size)
        image_size = texture_size[::-1]
        frame = texture.pixels
        cam.play = False
        
        # check if image capture fails
        if not frame:
            self.result_label.text = 'Failed to capture image'
            return
        
        # convert texture to OpenCV image format
        frame = frame.reshape(texture_size[1], texture_size[0], 4)
        frame = frame[:,:,::-1]
        
        # initialize OpenCV QR Code detector
        detector = cv2.QRCodeDetector()
        
        # decode QR code using OpenCV QR Code detector
        data, bbox, _ = detector.detectAndDecode(frame)
        
        # get result from detector
        if bbox is not None:
            result = data.decode()
            
            # check if student has already been marked present
            if result in json_store:
                self.result_label.text = 'Student already marked present'
            else:
                # add student to attendance json file
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                json_store.put(result, timestamp=timestamp)
                self.result_label.text = 'Attendance marked for {}'.format(result)
        else:
            self.result_label.text = 'QR code not found'