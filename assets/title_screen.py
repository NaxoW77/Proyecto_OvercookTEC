
# --- Pantalla de inicio ---

# Aquí se muestra una pequeña introducción al juego,
# una imagen, y las instrucciones para jugar.

# Imports necesarios
from assets.classes import tk
from assets.classes import StyledFrame



# Se define la clase del frame
class IntroFrame(StyledFrame):
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
            bg="white",
            
            )
        left.grid(row=0, column=0, sticky="nsew")
        
        # Título
        self.create_title(
            left, # Ubicación
            "OvercookTEC" # Texto
            ).pack()
        
        # Descripción
        self.create_text1(
            left, # Ubicación
            "OvercookTEC es un juego basado en el juego de cocina cooperativo, Overcooked. En donde se debe trabajar en conjunto para entregar el mayor número de platos en el menor tiempo posible.", # Texto
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
            bg="#dbd339" # Fondo
            )
        self.demo_img_label.pack(side="top", padx=(0, 0), pady=0)
        
        # -- Body izquierdo | ... --
        
        
        # -- ... | Body derecho --
 
        # Contenedor derecho
        right = tk.Frame(
            split_frame,
            bg="white"
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
                    "• Primer jugador:\n- Muevete con W-A-S-D, interactua con E\n\n• Segundo jugador:\n- Muevete con I-J-K-L e interactua con U\n\n• Al iniciar el juego, tendrán un tiempo limitado establecido para preparar y entregar pedidos.\n\n• Tomen ingredientes de las cajas, procésenlos en las estaciones y entreguenlos a los platos. \n\n• Cada pedido puntúa según el tiempo de entrega.\n\n• Si no se entrega un pedido a tiempo se restarán puntos.\n\n• El juego termina cuando se termine el tiempo, o se resten muchos puntos.\n\n\n¿Serás capaz de preparar suficientes pedidos? \n\n¡Disfruta!", # Texto
            10, # Distanciado en x
            5, # Distanciado en y
            600, # Ancho máximo
            "left" # Alineación
            ).pack()

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
            lambda: controller.show_frame("SelectFrame") # Función
            ).pack(side="left", padx=5)
        
        # --- Botones ---
        
        
        