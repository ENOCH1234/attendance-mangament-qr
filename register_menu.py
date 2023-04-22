from kivy.uix.screenmanager import Screen
from kivy.storage.jsonstore import JsonStore
import os
import pyqrcode
import random

class RegisterMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.store = JsonStore('Studentdata.json')
        self.qr_folder = 'qrcodes'
        random.seed()

        # Create the QR code folder if it doesn't exist
        if not os.path.exists(self.qr_folder):
            os.mkdir(self.qr_folder)

    def save_data(self):
        first_name = self.ids.first_name_input.text
        last_name = self.ids.last_name_input.text
        matric_number = self.ids.matric_number_input.text
        lab_number = int(self.ids.lab_number_input.text)
    
    # Get a list of all available labs
        available_labs = [i+1 for i in range(lab_number)]
    
    # Get the list of labs already assigned to students
        labs_assigned = [self.store.get(key)['Lab'] for key in self.store.keys()]
    
    # Remove labs already assigned to students from available labs
        available_labs = list(set(available_labs) - set(labs_assigned))
    
    # If there are no available labs, assign a random lab
        if not available_labs:
            nlab = random.randint(1, lab_number)
        else:
        # Shuffle the list of available labs
            random.shuffle(available_labs)
        
        # Assign the first available lab to the student
            nlab = available_labs[0]
    
    # Save the data to the JSON store
        self.store.put(matric_number, first_name=first_name, last_name=last_name, Lab=nlab)

    # Generate the QR code and save it to a file
        qr = pyqrcode.create(matric_number)
        qr.png(os.path.join(self.qr_folder, matric_number + '.png'), scale=8)

    # Clear the input fields
        self.ids.first_name_input.text = ''
        self.ids.last_name_input.text = ''
        self.ids.matric_number_input.text = ''
        self.ids.lab_number_input.text = ''

