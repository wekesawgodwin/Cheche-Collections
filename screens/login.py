# screens/login.py
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.snackbar import MDSnackbarText
import database

KV_LOGIN = '''
<LoginScreen>:
    MDCard:
        size_hint: None, None
        size: "320dp", "400dp"
        pos_hint: {"center_x": .5, "center_y": .5}
        elevation: 4
        padding: 25
        spacing: 25
        orientation: 'vertical'

        MDLabel:
            text: "Boutique POS"
            theme_text_color: "Primary"
            font_style: "HeadlineMedium"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15

        MDTextField:
            id: username_field
            mode: "outlined"
            MDTextFieldHintText:
                text: "Username"
            MDTextFieldIconLeading:
                icon: "account"

        MDTextField:
            id: password_field
            mode: "outlined"
            password: True
            MDTextFieldHintText:
                text: "Password"
            MDTextFieldIconLeading:
                icon: "key-variant"

        MDFillRoundFlatButton:
            text: "LOGIN"
            pos_hint: {"center_x": .5}
            on_release: root.do_login()

        Widget:
            size_hint_y: None
            height: "10dp"
'''
Builder.load_string(KV_LOGIN)

class LoginScreen(MDScreen):
    def do_login(self):
        username = self.ids.username_field.text.strip()
        password = self.ids.password_field.text.strip()

        if not username or not password:
            self.show_error("Please enter username and password")
            return

        user = database.authenticate_user(username, password)
        if user:
            # Clear fields
            self.ids.password_field.text = ""
            
            # Switch to main dashboard
            app = self.manager.parent_app
            app.current_user = user
            self.manager.current = "dashboard"
        else:
            self.show_error("Invalid credentials")

    def show_error(self, message):
        MDSnackbar(
            MDSnackbarText(text=message),
            y="24dp",
            pos_hint={"center_x": 0.5},
            size_hint_x=0.8
        ).open()