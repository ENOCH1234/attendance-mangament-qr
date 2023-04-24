import os
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy_garden.zbarcam import ZBarCam
from pyzbar.pyzbar import ZBarSymbol

# ...

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
        rjson_store = JsonStore('Studentdata.json')
        json_store = JsonStore(attendance_file)

    # request camera and storage permissions
        from android.permissions import request_permissions, Permission
        request_permissions([
        Permission.CAMERA,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE
    ])

    # start the camera and enable QR code detection
        cam = ZBarCam(
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            code_types=[ZBarSymbol.QRCODE, ZBarSymbol.EAN13],
            symbol_color=(1, 1, 1, 1),
            border_color=(1, 0, 0, 1),
            border_width=2,
            fps=30,
            resolution=(640, 480),
            play=True,
            orientation='landscape',
    )

    # wait for QR code detection
        while True:
            symbols = cam.symbols
            if symbols:
            # get result from detector
                result = symbols[0].data.decode()

            # check if student has already been marked present (this block doesn't run for the first time')
                if result in json_store:
                    self.result_label.text = 'Student already marked present'
                else:
                # add student to attendance json file (check if student matric no is in registered students json file)
                    if result not in rjson_store:
                        self.result_label.text = 'Student not registered yet'
                    else:
                        json_store.put(result)
                        self.result_label.text = 'Attendance marked for {}'.format(result)

            # stop the camera
                cam.play = False
                break