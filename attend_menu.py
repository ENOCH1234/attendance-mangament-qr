from datetime import datetime
import os
import cv2
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy_garden.zbarcam import ZBarCam

Builder.load_file('attend_menu.kv')


class CameraWidget(FloatLayout):
    play = ObjectProperty(None)
    stop = ObjectProperty(None)
    image = ObjectProperty(None)


class AttendMenu(Screen):
    date_input = ObjectProperty(None)
    result_label = ObjectProperty(None)
    camera = ObjectProperty(None)

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

        # initialize OpenCV QR Code detector
        detector = cv2.QRCodeDetector()

        # create new instance of camera
        self.camera = CameraWidget()
        self.camera.play = True

        # # :import ZBarCam kivy_garden.zbarcam.ZBarCam
        # BoxLayout:
        #     orientation: 'vertical'
        #     ZBarCam:
        #         id: zbarcam
        #         # optional, by default checks all types
        #         code_types: 'QRCODE', 'EAN13'
        #     Label:
        #         size_hint: None, None
        #         size: self.texture_size[0], 50
        #         text: ', '.join([str(symbol.data)
        #                         for symbol in zbarcam.symbols])

        # decode QR code using OpenCV QR Code detector
        while True:
            # check if camera image is not None
            if self.camera.image is not None:
                ret, frame = self.camera.image.read()
            else:
                self.result_label.text = 'Failed to capture image'
                return

            # decode QR code using OpenCV QR Code detector
            data, bbox, _ = detector.detectAndDecode(frame)

            # get result from detector
            if bbox is not None:
                result = data
                self.result_label.text = result
                matric_number = result.strip()

                # check if matric number already exists in json store
                if self.date_input.text in json_store:
                    if matric_number not in json_store[self.date_input.text]['students']:
                        json_store[self.date_input.text]['students'].append(
                            matric_number)
                else:
                    json_store[self.date_input.text] = {'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                        'students': [matric_number]}
                break
            else:
                self.result_label.text = 'No QR code found'

        # cleanup
        self.camera.image.release()
        cv2.destroyAllWindows()
        self.camera.play = False
