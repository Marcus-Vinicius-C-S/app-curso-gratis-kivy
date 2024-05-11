from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
from kivy.core.window import Window

# Definição das janelas de tela

class CreateAccountWindow(Screen):
    # Definição de propriedades de objetos para os elementos de interface do usuário
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    
    def submit(self):
        # Método para lidar com a submissão do formulário de criação de conta
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
        # Método para navegar de volta para a tela de login
        self.reset()
        sm.current = "login"
        
    def reset(self):
        # Método para redefinir os campos do formulário
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""
        
        
class LoginWindow(Screen):
    # Definição de propriedades de objetos para os elementos de interface do usuário
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def createBtn(self):
        # Método para navegar para a tela de criação de conta
        self.reset()
        sm.current = "create"
    
    def loginBtn(self):
        # Método para lidar com o evento de clique no botão de login
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()
        
    def reset(self):
        # Método para redefinir os campos do formulário
        self.email.text = ""
        self.password.text = ""
        
        
class MainWindow(Screen):
    # Definição de propriedades de objetos para os elementos de interface do usuário
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""
    
    def logOut(self):
        # Método para fazer logout e navegar de volta para a tela de login
        sm.current = "login"
        
    def on_enter(self, *args):
        # Método chamado quando a tela principal é exibida
        password, name, created = db.get_user(self.current)
        self.n.text = "Nome da conta: " + name
        self.email.text = "Email: " + self.current
        self.created.text = "Criado em: " + created
            
class WindowManager(ScreenManager):
    # Gerenciador de tela
    
    pass

# Funções para exibir pop-ups de erro

def invalidLogin():
    pop = Popup(title='Login Inválido',
    content=Label(text='Usuário ou senha inválidos.'),
    size_hint=(None, None), size=(400, 400))
    pop.open()
    
def invalidForm():
    pop = Popup(title='Formulário Inválido', content=Label(text='Por favor, preencha todos os campos com informações válidas!.'), size_hint=(None, None), size=(400, 400))
    pop.open()
    
# Carregamento do arquivo KV e instanciamento do gerenciador de tela e banco de dados

kv = Builder.load_file("my.kv")
sm = WindowManager()
db = DataBase("users.txt")
screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), MainWindow(name="main")]

# Adição das telas ao gerenciador de tela

for screen in screens:
    sm.add_widget(screen)
    sm.current = "login"
        
# Definição da classe principal do aplicativo Kivy

class MyMainApp(App):
    def build(self):
        # Define o tamanho da janela para corresponder ao tamanho de um smartphone
        Window.size = (360, 640)  
        
        return sm
    
# Verificação se o script está sendo executado diretamente e inicialização do aplicativo

if __name__ == "__main__":
    MyMainApp().run()
