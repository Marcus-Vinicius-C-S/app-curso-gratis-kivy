from kivy.core.window import Window
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase

# Definição das janelas de tela

class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            ProfileSelectionWindow.current = self.email.text
            self.reset()
            sm.current = "profile_selection"
        else:
            invalidLogin()

    def reset(self):
        self.email.text = ""
        self.password.text = ""

class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)
                self.reset()
                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""

class ProfileSelectionWindow(Screen):
    current = ""

    def select_student(self):
        MainWindow.current = self.current
        sm.current = "main"

    def select_institution(self):
        MainWindow.current = self.current
        sm.current = "main"

class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.n.text = "Nome da conta: " + name
        self.email.text = "Email: " + self.current
        self.created.text = "Criado em: " + created

class WindowManager(ScreenManager):
    pass

def invalidLogin():
    pop = Popup(title='Login Inválido',
                content=Label(text='Usuário ou senha inválidos.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()

def invalidForm():
    pop = Popup(title='Formulário Inválido', content=Label(
        text='Por favor, preencha todos os campos com informações válidas!.'),
        size_hint=(None, None), size=(400, 400))
    pop.open()

kv = Builder.load_file("my.kv")
sm = WindowManager()
db = DataBase("users.txt")
screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), ProfileSelectionWindow(name="profile_selection"), MainWindow(name="main")]

for screen in screens:
    sm.add_widget(screen)

sm.current = "login"

class MyMainApp(App):
    def build(self):
        Window.size = (360, 640)
        Window.position = 'auto'
        return sm

if __name__ == "__main__":
    MyMainApp().run()
