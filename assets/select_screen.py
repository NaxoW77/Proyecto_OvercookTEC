
# --- Pantalla de selección ---

# Aquí se presentan los diferentes niveles
# y se pide seleccionar uno para continuar.

# Imports necesarios
from assets.classes import tk
from assets.classes import ttk
from assets.classes import StyledFrame

# Importar escenarios
from assets.classes import EscenarioList
escenarios = EscenarioList()



# Se define la clase del frame
class SelectFrame(StyledFrame):
    def __init__(self, parent, controller, root):
        super().__init__(parent, controller, "white", root) # Se hereda el controlador
        
        # --- Banner ---
        
        banner = tk.Frame(
            self,
            bg="#db9a39",
            height=10
            )
        banner.pack(fill="x")
        
        # --- Banner ---
        
        
        
        # --- Body ---
        
        # Contenedor principal
        split_frame = tk.Frame(
            self, # Ubicación
            bg="white" # Color
            )
        split_frame.pack(fill="both", expand=True, pady=20)
        
        split_frame.grid_columnconfigure(0, weight=15)
        split_frame.grid_columnconfigure(1, weight=85)

        # -- Body izquierdo | ... --
        
        # Contenedor izquierdo
        left = tk.Frame(
            split_frame,
            bg="white"
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
        
        # Selector de escenario
        self.stage_combo = ttk.Combobox(
            left, # Ubicación
            values=["Escenario 1", "Escenario 2", "Escenario 3"], # Opciones
            state="readonly" # Desactivar edición
            )
        self.stage_combo.pack(side="top", padx=55)
        
        # Texto de error
        self.error_txt = tk.Label(
            left, # Ubicación
            text="", # Texto
            fg="#db3939", # Color
            bg="white" # Fondo
            )
        
        # -- Body izquierdo | ... --
        
        
        # -- ... | Body derecho --
 
        # Contenedor derecho
        right = tk.Frame(
            split_frame,
            bg="white"
            )
        right.grid(row=0, column=1, sticky="nsew")
        
        # Título
        self.title_text = self.create_title(
            right, 
            "Escenario X"
            )
        self.title_text.pack()
        
        # Descripción
        self.desc_text = self.create_text2(
            right, # Ubicación
            "Descripción X", # Texto
            10, # Distanciado en x
            5, # Distanciado en y
            800, # Ancho máximo
            "center" # Alineación
            )
        self.desc_text.pack()

        # Imagen del escenario
        self.esc_img = tk.PhotoImage(
            master=left, # Ubicación
            file="assets/img/demo.png", # Ruta de la imagen
            )
        self.esc_img_label = tk.Label(
            right, # Ubicación
            image=self.esc_img, # Imagen
            bg="white" # Fondo
            )
        self.esc_img_label.pack()

        # -- ... | Body derecho --
        
        # --- Body ---
        
        
        
        # --- Botones ---
        
        # Contenedor
        btn_container = tk.Frame(
            self,
            bg="white"
            )
        btn_container.pack(side="bottom", fill="x", pady=20)
        
        # Subcontenedor
        btn_group = tk.Frame(
            btn_container,
            width=200,
            bg="white"
            )
        btn_group.pack(side="bottom", padx=5)
        
        # Botón de jugar
        self.create_button1(
            btn_group, # Ubicación
            "Jugar", # Texto
            lambda: iniciar() # Función para iniciar el juego
            ).pack(side="left", padx=5)
        
        # --- Botones ---
        
        # Función para iniciar el juego
        def iniciar():
            # Obtener el escenario seleccionado
            selected = self.stage_combo.get()
            if selected in [escenario.name for escenario in escenarios.getEscenarios()]:
                # Asignar el escenario al controlador
                controller.escenario = escenarios.getEscenario(selected)
            else:
                # Mostrar mensaje de error
                self.error_txt.config(text="Por favor, selecciona un escenario")
                self.show(self.error_txt)
                self.after(3000, lambda: self.hide(self.error_txt))
                return
            
            # Asignar el puntaje y los pedidos completados al controlador
            controller.puntaje_max = 0
            controller.pedidos_completados = 0
            
            # Mostrar la siguiente sección y bloquear el selector
            controller.show_frame("GameFrame")
            self.stage_combo.config(state="disabled")
    
    # Función para actualizar el frame
    def update_frame(self):
        # Lista de escenarios disponibles
        esc = escenarios.getEscenarios()
        self.stage_combo.config(values=[escenario.name for escenario in esc])
        self.stage_combo.current(0)
        self.stage_combo.config(state="readonly")
        
        # Función para detectar el escenario seleccionado
        self.stage_combo.bind("<<ComboboxSelected>>", lambda event: self.update_img())
        self.update_img()
        
    # Función para actualizar la imagen del escenario seleccionado
    def update_img(self):
        self.title_text.config(text=f"Escenario {self.stage_combo.get()}")
        self.desc_text.config(text=escenarios.getEscenario(self.stage_combo.get()).desc)
        
        self.esc_img = tk.PhotoImage(
            master=self, # Ubicación
            file=f"assets/img/{self.stage_combo.get()}demo.png", # Ruta de la imagen
            ).subsample(2,2)
        
        self.esc_img_label.config(image=self.esc_img)
        
        