
# --- Pantalla de juego ---

# ...

# Imports necesarios
from assets.classes import tk
from assets.classes import ttk
from assets.classes import StyledFrame

# Importar textos
from assets.lang import Lang
lang = Lang().titleScreen # Se necesita únicamente el diccionario de este frame

# Importar estilos
from assets.styles import Style
style = Style()

# Importar escenarios
from assets.data import escenarios
escenarios = escenarios.EscenarioList()

# Importar recetas
from assets.data import recetas
recetas = recetas.RecetaList()

# Se define la clase del frame
class GameFrame(StyledFrame):
    def __init__(self, parent, controller, root):
        super().__init__(parent, controller, style.colors["default"], root) # Se hereda el controlador
        
        # --- Banner ---
        
        banner = tk.Frame(
            self,
            bg=style.colors["main"],
            height=10
            )
        banner.pack(fill="x")
        
        # --- Banner ---
        
        
        
        # --- Body ---
        
        # Contenedor principal
        main_frame = tk.Frame(
            self, # Ubicación
            bg=style.colors["default"] # Color
        )
        main_frame.pack(fill="both", expand=True, pady=20)
        
        center = tk.Frame(main_frame, bg=style.colors["default"])
        center.pack(fill="both", expand=True)
        
        escenario = escenarios.getEscenario("E1")
        rows = len(escenario.layout)
        cols = len(escenario.layout[0])
        size = escenario.tamaño

        # Creamos un Canvas
        canvas = tk.Canvas(center, width=cols*size, height=rows*size, bg="white")
        canvas.pack(expand=True)

        # Dibujar el Grid en el Canvas
        for r in range(0, len(escenario.layout)):
            for c in range(0, len(escenario.layout[r])):
                x1 = c * size
                y1 = r * size
                x2 = x1 + size
                y2 = y1 + size
                
                tipo = "black" # Esto se debe reemplazar por la imagen del objeto
                obj = escenario.layout[r][c]
                if obj == 1:
                    tipo = "red"
                elif obj == 2:
                    tipo = "green"
                elif obj == 3 or obj == 4 or obj == 5:
                    tipo = "cyan"
                elif obj == 6 or obj == 7:
                    tipo = "yellow"
                    
                canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=tipo)

        # Dibujar los jugadores
        
        # Jugador 1
        controller.chef1.posX = escenario.posChef1[0] * size
        controller.chef1.posY = escenario.posChef1[1] * size
        controller.chef1.size = size
        
        chef1_pos = canvas.create_rectangle(
            controller.chef1.posX,
            controller.chef1.posY,
            controller.chef1.posX +
            size,
            controller.chef1.posY + size,
            fill="blue")
        
        chef1_cursor = canvas.create_rectangle(
            controller.chef1.posX+size/2-size/8,
            controller.chef1.posY+size/2-size/8,
            controller.chef1.posX + size /2 + size/8, 
            controller.chef1.posY + size/2 + size/8,
            fill="red")
        
        # Jugador 2
        controller.chef2.posX = escenario.posChef2[0] * size
        controller.chef2.posY = escenario.posChef2[1] * size
        controller.chef2.size = size
        
        chef2_pos = canvas.create_rectangle(controller.chef2.posX, controller.chef2.posY, controller.chef2.posX + size, controller.chef2.posY + size, fill="purple")
        
        chef2_cursor = canvas.create_rectangle(
            controller.chef2.posX+size/2-size/8,
            controller.chef2.posY+size/2-size/8,
            controller.chef2.posX + size /2 + size/8, 
            controller.chef2.posY + size/2 + size/8,
            fill="red")

        def mover(event):
            key = event.keysym
            print(key)
            
            
            if key in controller.chef1.keySet:
                chef = controller.chef1
                chef_pos = chef1_pos
                chef_cursor = chef1_cursor
            
            elif key in controller.chef2.keySet:
                chef = controller.chef2
                chef_pos = chef2_pos
                chef_cursor = chef2_cursor
            
            else:
                return
            
            if key in chef.keySet[:-1]:
                movement = chef.keyEvent(key, canvas)
                if movement != [0,0]:
                    canvas.move(chef_pos, movement[0], movement[1])
                    
                canvas.coords (chef_cursor,
                                chef.posX+size/2-size/8,chef.posY+size/2-size/8, chef.posX + size /2 + size/8, chef.posY + size/2 + size/8)
                
                if chef.direction == "left":
                    canvas.move(chef_cursor, - size/2 + size/8, 0)
                elif chef.direction == "right":
                    canvas.move(chef_cursor, size/2 - size/8, 0)
                elif chef.direction == "up":
                    canvas.move(chef_cursor, 0, - size/2 + size/8)
                elif chef.direction == "down":
                    canvas.move(chef_cursor, 0, size/2 - size/8)
            else:
                act = chef.keyEvent(key, canvas)
                
                direction = chef.direction
                
                if direction == "left":
                    canvas.move(chef_cursor,- size/2, 0)
                    self.after(20, lambda: 
                        canvas.move(chef_cursor, +size/2, 0)
                        )
                
                elif direction == "right":
                    canvas.move(chef_cursor, size/2, 0)
                    self.after(20, lambda: 
                        canvas.move(chef_cursor, -size/2, 0)
                        )
                elif direction == "up":
                    canvas.move(chef_cursor, 0, - size/2)
                    self.after(20, lambda: 
                        canvas.move(chef_cursor, 0, +size/2)
                        )
                elif direction == "down":
                    canvas.move(chef_cursor, 0, size/2)
                    self.after(20, lambda: 
                        canvas.move(chef_cursor, 0, -size/2)
                        )    
                
                print(act)

        # Vincular las teclas
        root.bind("<Key>", mover)
        
        # --- Body ---
        
        