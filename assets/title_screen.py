
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


# Se define la clase del frame
class IntroFrame(StyledFrame):
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
            lang.title # Texto
            ).pack()
        
        # Descripción
        self.create_text1(
            left, # Ubicación
            "OvercookTEC es un juego basado en...", # Texto
            55, # Distanciado en x
            5, # Distanciado en y
            500 # Ancho máximo
            ).pack(side="top",pady=(0, 20))
        
        # Imagen del juego real
        self.demo_img = tk.PhotoImage(
            master=left, # Ubicación
            file="assets/img/demo.png", # Ruta de la imagen
            )
        
        self.demo_img_label = tk.Label(
            left, # Ubicación
            image=self.demo_img, # Imagen
            bg=style.colors["main"] # Fondo
            )
        self.demo_img_label.pack(side="top", padx=(0, 0), pady=0)
        
        # -- Body izquierdo | ... --
        
        
        # -- ... | Body derecho --
 
        # Contenedor derecho
        right = tk.Frame(
            split_frame,
            bg=style.colors["default"]
            )
        right.grid(row=0, column=1, sticky="nsew")
        
        # Título
        self.create_title(
            right, 
            "Instrucciones:"
            ).pack()
        
        # Instrucciones
        self.create_text2(
            right, # Ubicación
            # Favor utilizar \n para saltos de línea
            "... Las teclas son WASD+E y IJKL+U...\n...Las recetas van en los platos...", # Texto
            10, # Distanciado en x
            5, # Distanciado en y
            800, # Ancho máximo
            "center" # Alineación
            ).pack()

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
            lambda: controller.show_frame("SelectFrame") # Función
            ).pack(side="left", padx=5)
        
        # --- Botones ---
        
        
        