
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
        
        # Se carga el escenario 1
        escenario = escenarios.getEscenario("E1")
        
        self.bg_image = tk.PhotoImage(file=escenario.fondo)

        # Fondo de la pantalla
        self.bg_label = tk.Label(center, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        rows = len(escenario.layout)
        cols = len(escenario.layout[0])
        size = escenario.tamaño

        # Creamos el Canvas de fondo (grid y colisiones)
        canvas_bg = tk.Canvas(center, width=cols*size, height=rows*size, bg="white", highlightthickness=0)
        canvas_bg.pack(expand=True)

        # Creamos un Canvas superior para imágenes y elementos dinámicos
        canvas_fg = tk.Canvas(center, width=cols*size, height=rows*size, bg=canvas_bg['bg'], bd=0, highlightthickness=0)
        canvas_fg.place(in_=canvas_bg, x=0, y=0)

        # Forzar el fondo por debajo de los canvas
        self.bg_label.lower(canvas_bg)
        
        # Modo Debug
        #canvas_fg.place_forget()

        # Dibujar el Grid en el Canvas
        for r in range(0, len(escenario.layout)):
            for c in range(0, len(escenario.layout[r])):
                x1 = c * size
                y1 = r * size
                x2 = x1 + size
                y2 = y1 + size
                
                # Mantener referencias a las imágenes de bloque para evitar borrarlas
                if not hasattr(canvas_fg, 'images'):
                    canvas_fg.images = []

                block_img = tk.PhotoImage(file=escenario.estaciones[0].img).subsample(9,9)
                tipo = "black"
                
                obj = escenario.layout[r][c]
                
                # Texturas para cada objeto
                # Modificar subsample si se va a cambiar
                
                if obj == 0:
                    tipo = "black"
                    block_img = tk.PhotoImage(file="assets/img/suelo.png").subsample(5,5)
                
                elif obj == 1:
                    tipo = "red"
                    block_img = tk.PhotoImage(file="assets/img/pared.png").subsample(5,5)
                    
                elif obj == 2:
                    tipo = "green"
                    block_img = tk.PhotoImage(file="assets/img/plato.png").subsample(5,5)
                    
                elif obj >= 3 and obj <= 6:
                    tipo = "brown"
                    block_img = tk.PhotoImage(file=escenario.cajas[obj-3].item.img).subsample(6,6)
                    
                elif obj == 7 or obj == 8 or obj == 9:
                    tipo = "gray"
                    block_img = tk.PhotoImage(file=escenario.estaciones[obj-7].img).subsample(5,5)
                    
                canvas_bg.create_rectangle(x1, y1, x2, y2, outline="black", fill=tipo)
    
                canvas_fg.create_rectangle(x1, y1, x2, y2, outline="black", fill=tipo)
                
                canvas_fg.images.append(block_img)
                canvas_fg.create_image(x1+size/2, y1+size/2, anchor="center", image=canvas_fg.images[-1])
                


        # Dibujar los jugadores
        
        # Jugador 1
        controller.chef1.posX = escenario.posChef1[0] * size
        controller.chef1.posY = escenario.posChef1[1] * size
        controller.chef1.size = size

        # Cajas de colisión (Canvas de fondo)
        chef1_pos = canvas_bg.create_rectangle(
            controller.chef1.posX,
            controller.chef1.posY,
            controller.chef1.posX + size,
            controller.chef1.posY + size,
            fill="blue")

        # Avatar (Canvas Superior)
        chef1_img = tk.PhotoImage(file="assets/img/chef1.png").subsample(6,6)
        canvas_fg.chef1_img = chef1_img
        chef1_avatar = canvas_fg.create_image(controller.chef1.posX, controller.chef1.posY, anchor="nw", image=chef1_img)

        # Cursor (Canvas inferior)
        chef1_cursor = canvas_bg.create_rectangle(
            controller.chef1.posX+size/2-size/8,
            controller.chef1.posY+size/2-size/8,
            controller.chef1.posX + size /2 + size/8,
            controller.chef1.posY + size/2 + size/8,
            fill="red")

        
        img1 = tk.PhotoImage(file="assets/img/tomate.png").subsample(8,8)
        canvas_fg.img1 = img1
        chef1_item = canvas_fg.create_image(controller.chef1.posX-size/4, controller.chef1.posY-size/4, anchor="nw", image=img1)
        
        # Jugador 2
        controller.chef2.posX = escenario.posChef2[0] * size
        controller.chef2.posY = escenario.posChef2[1] * size
        controller.chef2.size = size

        # Cajas de colisión (Canvas de fondo)
        chef2_pos = canvas_bg.create_rectangle(controller.chef2.posX, controller.chef2.posY, controller.chef2.posX + size, controller.chef2.posY + size, fill="purple")
        
        # Avatar (Canvas Superior)
        chef2_img = tk.PhotoImage(file="assets/img/chef2.png").subsample(6,6)
        canvas_fg.chef2_img = chef2_img
        chef2_avatar = canvas_fg.create_image(controller.chef2.posX, controller.chef2.posY, anchor="nw", image=chef2_img)

        # Cursor (Canvas inferior)
        chef2_cursor = canvas_bg.create_rectangle(
            controller.chef2.posX+size/2-size/8,
            controller.chef2.posY+size/2-size/8,
            controller.chef2.posX + size /2 + size/8,
            controller.chef2.posY + size/2 + size/8,
            fill="red")

        # Item (Canvas Superior)
        img2 = tk.PhotoImage(file="assets/img/lechuga.png").subsample(8,8)
        canvas_fg.img2 = img2
        chef2_item = canvas_fg.create_image(controller.chef2.posX-size/4, controller.chef2.posY-size/4, anchor="nw", image=img2)

        
        # --- Body ---

        def mover(event):
            key = event.keysym
            
            if key in controller.chef1.keySet:
                chef = controller.chef1
                chef_pos = chef1_pos
                chef_avatar = chef1_avatar
                chef_cursor = chef1_cursor
                chef_item = chef1_item
            
            elif key in controller.chef2.keySet:
                chef = controller.chef2
                chef_pos = chef2_pos
                chef_avatar = chef2_avatar
                chef_cursor = chef2_cursor
                chef_item = chef2_item
            
            else:
                return
            
            if key in chef.keySet[:-1]:
                movement = chef.keyEvent(key, canvas_bg)
                if movement != [0,0]:
                    canvas_bg.move(chef_pos, movement[0], movement[1])
                    
                    canvas_fg.move(chef_avatar, movement[0], movement[1])
                    canvas_fg.move(chef_item, movement[0], movement[1])
                    canvas_bg.move(chef_cursor, movement[0], movement[1])

                # Asegurar las coordenadas absolutas del cursor en el canvas superior
                canvas_bg.coords(chef_cursor,
                                chef.posX+size/2-size/8,chef.posY+size/2-size/8, chef.posX + size /2 + size/8, chef.posY + size/2 + size/8)
                
                if chef.direction == "left":
                    canvas_bg.move(chef_cursor, - size/2 + size/8, 0)
                elif chef.direction == "right":
                    canvas_bg.move(chef_cursor, size/2 - size/8, 0)
                elif chef.direction == "up":
                    canvas_bg.move(chef_cursor, 0, - size/2 + size/8)
                elif chef.direction == "down":
                    canvas_bg.move(chef_cursor, 0, size/2 - size/8)
            else:
                
                # Animación del cursor
                direction = chef.direction

                if direction == "left":
                    canvas_bg.move(chef_cursor,- size/2, 0)
                    self.after(20, lambda: 
                        canvas_bg.move(chef_cursor, +size/2, 0)
                        )
                
                elif direction == "right":
                    canvas_bg.move(chef_cursor, size/2, 0)
                    self.after(20, lambda: 
                        canvas_bg.move(chef_cursor, -size/2, 0)
                        )
                elif direction == "up":
                    canvas_bg.move(chef_cursor, 0, - size/2)
                    self.after(20, lambda: 
                        canvas_bg.move(chef_cursor, 0, +size/2)
                        )
                elif direction == "down":
                    canvas_bg.move(chef_cursor, 0, size/2)
                    self.after(20, lambda: 
                        canvas_bg.move(chef_cursor, 0, -size/2)
                        )
                act = chef.keyEvent(key, canvas_bg)
                
                # Se interactuó con una caja
                if act >= 3 and act <= 6:
                    chef.setItem(escenario.cajas[act-3].item)
                    
                    # Cargar la imagen del item y actualizar el elemento en el canvas superior
                    chef.item.img = tk.PhotoImage(file=chef.item.img)
                    if chef is controller.chef1:
                        canvas_fg.img1 = chef.item.img
                        canvas_fg.itemconfig(chef1_item, image=canvas_fg.img1)
                    else:
                        canvas_fg.img2 = chef.item.img
                        canvas_fg.itemconfig(chef2_item, image=canvas_fg.img2)
                
                # Se interactuó con una estación
                if act >= 7 and act <= 9:
                    print("Procesando")
                    # Procesar

                print(act)

        # Vincular las teclas
        root.bind("<Key>", mover)
        
        # --- Body ---
        
        