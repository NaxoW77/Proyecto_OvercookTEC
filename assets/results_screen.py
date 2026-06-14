
# --- Pantalla de resultados ---

# Aquí termina el juego y se muestra
# el puntaje máximo obtenido.

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
class ResultsFrame(StyledFrame):
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
        body = tk.Frame(
            self,
            bg=style.colors["default"]
            )
        body.pack(pady=20, padx=20)
        
        # Título
        self.create_title(
            body,
            "Resultados"
        ).pack()
        
        # Texto
        self.create_text1(
            body,
            "Resultados de la partida:"
        ).pack()
        
        # Puntaje
        self.puntaje_text = self.create_text1(
            body,
            f"Puntaje: X"
        )
        self.puntaje_text.pack()
        
        # Pedidos entregados
        self.pedidos_text = self.create_text1(
            body,
            f"Pedidos entregados: X"
        )
        self.pedidos_text.pack()
        
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
        
        # Botón de volver a jugar
        self.create_button1(
            btn_group, # Ubicación
            "Volver a jugar", # Texto
            lambda: controller.show_frame("SelectFrame") # Función para volver a jugar
            ).pack(side="left", padx=5)
        
        # --- Botones ---
    
    # Función para actualizar el frame
    def update_frame(self):
        self.puntaje_text.config(text=f"Puntaje: {self.controller.puntaje_max}")
        self.pedidos_text.config(text=f"Pedidos entregados: {self.controller.pedidos_completados}")
        
        