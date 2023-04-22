from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

# Import the screen classes from their respective files
from home_screen import HomeScreen
from lab_menu import LabMenu
from register_menu import RegisterMenu
from report_menu import ReportMenu
from register_success import RegisterSuccess
from attend_menu import AttendMenu


class MyScreenManager(ScreenManager):
    pass


class MainApp(App):
    kv_file = './main.kv'

    def build(self):
        sm = MyScreenManager()

        # Create instances of each screen and add them to the ScreenManager
        home_screen = HomeScreen(name='Home')
        lab_menu = LabMenu(name='labmenu')
        register_menu = RegisterMenu(name='register')
        report_menu = ReportMenu(name='report')
        register_success = RegisterSuccess(name='Successful')
        Attend_menu = AttendMenu(name='Attendance')

        sm.add_widget(home_screen)
        sm.add_widget(lab_menu)
        sm.add_widget(register_menu)
        sm.add_widget(report_menu)
        sm.add_widget(register_success)
        sm.add_widget(Attend_menu)

        return sm


if __name__ == '__main__':
    MainApp().run()