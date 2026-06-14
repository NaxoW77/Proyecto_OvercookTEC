
# --- Pantalla de inicio ---

# Aquí se muestra una pequeña introducción al juego,
# una imagen, y las instrucciones para jugar.

# Imports necesarios
from assets.classes import tk
from assets.classes import ttk
from assets.classes import StyledFrame

# Importar textos
from assets.lang import Lang
lang = Lang()

# Importar estilos
from assets.styles import Style
style = Style()

# Importar escenarios
from assets.data.escenarios import EscenarioList
escenarios = EscenarioList()


# Se define la clase del frame
class SelectFrame(StyledFrame):
    def __init__(self, parent, controller, root):
        super().__init__(parent, controller, style.colors["default"], root) # Se hereda el controlador
        
        # --- Banner ---
        
        banner = tk.Frame(
            self,
            bg=style.colors["game"],
            height=10
            )
        banner.pack(fill="x")
        
        # --- Banner ---
        
        
        
        # --- Body ---
        
        # Contenedor principal
        split_frame = tk.Frame(
            self, # Ubicación
            bg=style.colors["default"] # Color
            )
        split_frame.pack(fill="both", expand=True, pady=20)
        
        split_frame.grid_columnconfigure(0, weight=15)
        split_frame.grid_columnconfigure(1, weight=85)

        # -- Body izquierdo | ... --
        
        # Contenedor izquierdo
        left = tk.Frame(
            split_frame,
            bg=style.colors["default"]
            )
        left.grid(row=0, column=0, sticky="nsew")
        
        # Título
        self.create_title(
            left, # Ubicación
            "Configuración del juego" # Texto
            ).pack()
        
        # Descripción
        self.create_text1(
            left, # Ubicación
            "Selecciona el escenario que deseas jugar:", # Texto
            55, # Distanciado en x
            5, # Distanciado en y
            500 # Ancho máximo
            ).pack(side="top",pady=(0, 20))
        
        self.stage_combo = ttk.Combobox(
            left, # Ubicación
            values=["Escenario 1", "Escenario 2", "Escenario 3"], # Opciones
            state="readonly" # Desactivar edición
            )
        self.stage_combo.pack(side="top", padx=55)
        
        self.error_txt = tk.Label(
            left, # Ubicación
            text="", # Texto
            fg=style.colors["fail"], # Color
            bg=style.colors["default"] # Fondo
            )
        
        # -- Body izquierdo | ... --
        
        
        # -- ... | Body derecho --
 
        # Contenedor derecho
        right = tk.Frame(
            split_frame,
            bg=style.colors["default"]
            )
        right.grid(row=0, column=1, sticky="nsew")
        
        # Título
        self.title_text = self.create_title(
            right, 
            "Escenario X"
            )
        self.title_text.pack()
        
        # Instrucciones
        self.desc_text = self.create_text2(
            right, # Ubicación
            "Descripción X", # Texto
            10, # Distanciado en x
            5, # Distanciado en y
            800, # Ancho máximo
            "center" # Alineación
            )
        self.desc_text.pack()

        self.demo_img = tk.PhotoImage(
            master=left, # Ubicación
            file="assets/img/demo.png", # Ruta de la imagen
            )
        self.demo_img_label = tk.Label(
            right, # Ubicación
            image=self.demo_img, # Imagen
            bg=style.colors["default"] # Fondo
            )
        self.demo_img_label.pack()

        # -- ... | Body derecho --
        
        # --- Body ---
        
        
        
        # --- Botones ---
        
        # Contenedor
        btn_container = tk.Frame(
            self,
            bg=style.colors["default"]
            )
        btn_container.pack(side="bottom", fill="x", pady=20)
        
        # Subcontenedor
        btn_group = tk.Frame(
            btn_container,
            width=200,
            bg=style.colors["default"]
            )
        btn_group.pack(side="bottom", padx=5)
        
        # Botón de jugar
        self.create_button1(
            btn_group, # Ubicación
            "Jugar", # Texto
            lambda: iniciar() # Función
            ).pack(side="left", padx=5)
        
        # --- Botones ---
        
        def iniciar():
            selected = self.stage_combo.get()
            if selected in [escenario.name for escenario in escenarios.getEscenarios()]:
                controller.escenario = escenarios.getEscenario(selected)
            else:
                self.error_txt.config(text="Por favor, selecciona un escenario")
                self.show(self.error_txt)
                self.after(3000, lambda: self.hide(self.error_txt))
                return
            
            controller.puntaje_max = 0
            controller.pedidos_completados = 0
            controller.show_frame("GameFrame")
            self.stage_combo.config(state="disabled")
    
    def update_frame(self):
        esc = escenarios.getEscenarios()
        self.stage_combo.config(values=[escenario.name for escenario in esc])
        self.stage_combo.current(0)
        self.stage_combo.config(state="readonly")
        self.stage_combo.bind("<<ComboboxSelected>>", lambda event: self.update_img())
        self.update_img()
        
    def update_img(self):
        self.title_text.config(text=f"Escenario {self.stage_combo.get()}")
        self.desc_text.config(text=escenarios.getEscenario(self.stage_combo.get()).desc)
        
        self.demo_img = tk.PhotoImage(
            master=self, # Ubicación
            file=f"assets/img/{self.stage_combo.get()}demo.png", # Ruta de la imagen
            ).subsample(2,2)
        
        self.demo_img_label.config(image=self.demo_img)
        
        