from kivy.uix.screenmanager import Screen
from kivy.storage.jsonstore import JsonStore


class LabMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.store = JsonStore('Labdata.json')

    def save_data(self):
        max_students = self.ids.max_students_input.text
        num_labs = self.ids.num_labs_input.text

        # Save the data to the JSON store
        self.store.put('lab_info', max_students=max_students, num_labs=num_labs)

        # Clear the input fields
        self.ids.max_students_input.text = ''
        self.ids.num_labs_input.text = ''
