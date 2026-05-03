# main.py
import os
# Ensure Kivy doesn't try to use X11/desktop providers on Android
os.environ['KIVY_NO_ARGS'] = '1'

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
import database

# Import Screens
from screens.login import LoginScreen
# We will create these in the next parts
# from screens.dashboard import DashboardScreen 
# from screens.inventory import InventoryScreen
# from screens.checkout import CheckoutScreen

class WindowManager(ScreenManager):
    pass

class BoutiquePOSApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user = None  # Holds logged-in user data
        
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        
        # Initialize SQLite database
        database.init_db()

        # Setup Screen Manager
        sm = WindowManager()
        self.parent_app = self # Reference to access app variables from screens
        sm.parent_app = self
        
        # Add Screens
        sm.add_widget(LoginScreen(name="login"))
        
        # Placeholder for next parts
        # sm.add_widget(DashboardScreen(name="dashboard"))
        # sm.add_widget(InventoryScreen(name="inventory"))
        # sm.add_widget(CheckoutScreen(name="checkout"))

        return sm

if __name__ == "__main__":
    BoutiquePOSApp().run()