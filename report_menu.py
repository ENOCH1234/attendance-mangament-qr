from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.storage.jsonstore import JsonStore
import os
import pandas as pd


class ReportMenu(Screen):
    def __init__(self, **kwargs):
        super(ReportMenu, self).__init__(**kwargs)
        self.total_attendance = 0
        self.store = JsonStore('Studentdata.json')

    def count_folders(self):
        lectures_path = 'lectures/'
        folders = [f for f in os.listdir(lectures_path) if os.path.isdir(os.path.join(lectures_path, f))]
        return len(folders)


    def export_attendance_to_excel(self, date):
        lecture_folder = f'lectures/{date}'
        if not os.path.isdir(lecture_folder):
            return 'no laboratory session was held on that date'
        attendance = JsonStore(f'{lecture_folder}/attendance.json')
        if attendance.exists('attendance'):
            matric_numbers = attendance.get('attendance')['matric_numbers']
            total_attendance = len(matric_numbers)

    # Save the data to an Excel file
            df = pd.DataFrame(matric_numbers, columns=['Matric Numbers'])
            excel_filename = f"{os.path.basename(lecture_folder)}.xlsx"
            df.to_excel(excel_filename, index=False) 
            self.ids.result_label.text =  f"Attendance data for lectures held on {os.path.basename(lecture_folder)} has been exported to {excel_filename}"       
            return 
        else:
            self.ids.result_label.text = "No attendance was taken on this day."   
            return  

    
    def export_data(self):
        try:
            data = []
        # Iterate through all the registered students
            for key in self.store:
                student_data = self.store.get(key)
            # Extract the relevant fields
                row = [key, student_data['first_name'], student_data['last_name'], student_data['Lab']]
                data.append(row)

        # Create a pandas DataFrame from the data
            df = pd.DataFrame(data, columns=['Matric Number', 'First Name', 'Last Name', 'Lab'])

        # Export the DataFrame to an excel file
            filename = 'registered_students.xlsx'
            df.to_excel(filename, index=False)
            self.ids.result_label.text = "Data exported successfully as registered_students.xlsx!"
            return 

        except Exception as e:
            self.ids.result_label.text = f"Error exporting data: {str(e)}"
            return 



