from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.toolbar.toolbar import MDToolbar
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout

# Create the screen
class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create the toolbar
        self.toolbar = MDToolbar(title="Attendance App", pos_hint={"top": 1})
        self.add_widget(self.toolbar)

        # Create the menu
        menu_items = [
            {"text": "Register Students"},
            {"text": "Attendance"},
            {"text": "Report Menu"},
            {"text": "Exit"},
        ]
        self.menu = MDDropdownMenu(
            caller=self.toolbar.right_action_items[0],
            items=menu_items,
            width_mult=4,
        )
        self.toolbar.right_action_items = [
            ["dots-vertical", lambda x: self.menu.open()],
        ]

        # Create the content
        content = MDBoxLayout(orientation="vertical")
        content.add_widget(MDFlatButton(text="Scan QR Code"))
        content.add_widget(MDFlatButton(text="Manually enter code"))

        self.add_widget(content)

# Create the screen manager
class ScreenManager(ScreenManager):
    pass

# Create the app
class AttendanceApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.primary_hue = "700"
        screen_manager = ScreenManager()
        screen_manager.add_widget(MainMenuScreen(name="main_menu"))
        return screen_manager

if __name__ == "__main__":
    AttendanceApp().run()
