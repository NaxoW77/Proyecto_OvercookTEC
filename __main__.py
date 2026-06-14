
# --- Código principal ---

# Este es el código encargado de llamar a todas
# las secciones, definir clases y modelos,
# y empezar el juego.

# Imports necesarios
from assets.classes import tk

# Importar secciones
from assets.title_screen import IntroFrame
from assets.game_screen import GameFrame
from assets.results_screen import ResultsFrame
from assets.select_screen import SelectFrame

# Importar modelo del jugador
from assets.classes import Player


# Se define la clase principal
class Main:
    def __init__(self, root):
        
        # Se instancian y configuran los jugadores
        self.chef1 = Player("Chef1", "assets/img/chef1.png", ["w", "s", "a", "d", "e"])
        self.chef2 = Player("Chef2", "assets/img/chef2.png", ["i", "k", "j", "l", "u"])
        
        # Variables globales
        self.escenario = None
        self.puntaje_max = 0
        self.pedidos_completados = 0
        
        # Configuración general de la ventana
        self.root = root
        self.root.title("OvercookTEC")
        width = 800
        height = 600
        self.root.geometry(f"{width}x{height}+{int(self.root.winfo_screenwidth()/2-width/2)}+{int(self.root.winfo_screenheight()/2-height/2)}")
        self.root.attributes("-fullscreen", True)
        self.root.resizable(False, False)
        self.root.configure(bg="white")

        # --- Header ---
        
        # Base del header
        self.main_header = tk.Frame(
            root,
            bg="#dbd339",
            height=60
            )
        self.main_header.pack(fill="x")
        
        # Logo
        self.header_logo = tk.PhotoImage(
            master=self.main_header,
            file="assets/img/hamburguesa.png",
            width=250,
            height=250
            ).subsample(4,4)
        
        self.header_img = tk.Label(
            self.main_header,
            image=self.header_logo,
            bg="#dbd339"
            )
        self.header_img.pack(side="left", padx=(20, 0), pady=0)
        
        # Título
        self.header_label = tk.Label(
            self.main_header,
            text="OvercookTEC",
            bg="#dbd339",
            fg="white",
            font=("Arial", 24, "bold")
            )
        self.header_label.pack(
            side="left",
            padx=10,
            pady=20
            )

        # Botón de salir
        btn_exit = tk.Button(
            self.main_header,
            text="X",
            bg="#ff0000",
            fg="white",
            font=("Arial", 18, "bold"),
            padx=12,
            pady=5,
            relief="groove",
            cursor="hand2", 
            command=lambda: self.root.destroy() # Función para detener el programa
            )
        btn_exit.pack(
            side="right", 
            pady=20, 
            padx=20
            )
        
        # --- Header ---
        
        
        
        # --- Body ---
        
        # Base principal
        self.container = tk.Frame(
            root,
            bg="white"
            )
        self.container.pack(
            fill="both",
            expand=True
            )

        # Llamada a todos los frames
        self.screens = {}
        for screen in (IntroFrame, SelectFrame, GameFrame, ResultsFrame):
            page_name = screen.__name__ # Se les coloca el nombre de la clase
            
            screenFrame = screen(parent=self.container, controller=self, root=self.root) # Se pasa el controlador principal a cada frame
            
            self.screens[page_name] = screenFrame # Se guardan los frames en una lista de fácil acceso
            screenFrame.grid(row=0, column=0, sticky="nsew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Se muestra el primer frame
        self.show_frame("IntroFrame")
    
        # --- Body ---
        
        
            
        # --- Footer ---
        
        # Base del footer
        self.main_footer = tk.Frame(root, bg="#dbd339", height=60)
        self.main_footer.pack(fill="x")
        
        self.main_footer_banner = tk.Frame(self.main_footer, bg="#db9a39",height=10)
        self.main_footer_banner.pack(fill="x")
        
        # Copyright
        self.footer_copyright = tk.Label(
            self.main_footer,
            text="Copyright © 2026 Ignacio Apuy, Jordanny Hernandez.",
            bg="#dbd339",
            fg="white",
            font=("Arial", 12)
            )
        self.footer_copyright.pack(
            side="top",
            pady=15)
        
        # --- Footer ---
        
        
        
    # Función para cambiar de frame
    def show_frame(self, page_name):
        frame = self.screens[page_name] # Se busca el frame en la lista
        frame.tkraise() # Función para mostrar el frame como tal
        
        # Se actualizan los datos en el frame, si es necesario
        if hasattr(frame, 'update_frame'):
            frame.update_frame() # Método interno

# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()