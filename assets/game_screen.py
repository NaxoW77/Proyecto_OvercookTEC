
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

# Importar clase Item
from assets.classes import Item

# Importar clase Estacion
from assets.classes import Mostrador

# Se define la clase del frame
class GameFrame(StyledFrame):
    def __init__(self, parent, controller, root):
        super().__init__(parent, controller, style.colors["default"], root) # Se hereda el controlador
        
        # --- Variables globales ---
        self.debug = False
        
        self.default_item = Item("Nada", 1, "assets/img/nada.png")
        
        self.mostradores = [
            Mostrador("Mostrador 1", self.default_item),
            Mostrador("Mostrador 2", self.default_item),
            Mostrador("Mostrador 3", self.default_item),
            Mostrador("Mostrador 4", self.default_item)
        ]
        
        self.mostradores_img = []
        
        # Modo Debug
        #self.canvas_fg.place_forget()
        
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
        main_frame = tk.Frame(
            self, # Ubicación
            bg=style.colors["default"] # Color
        )
        main_frame.pack(fill="both", expand=True, pady=0)

        # --- Body izquierdo ---
        left = tk.Frame(main_frame, bg=style.colors["game"], width=500)
        
        # Ancho del panel izquierdo
        left.pack(side="left", fill="both", padx=0)

        # Contenedor para los pedidos
        floating_frame = tk.Frame(left, bg=style.colors["default"], bd=2, relief="raised")
        floating_frame.pack(padx=8, pady=12)

        left_title = tk.Label(floating_frame, text="Pedidos", bg=style.colors["default"], fg=style.colors["main"], font=("Helvetica", 14, "bold"))
        left_title.pack(pady=(12, 6))

        left_text = tk.Label(floating_frame, text="[...].", bg=style.colors["default"], justify="left", wraplength=400)
        left_text.pack(padx=10)

        # Tabla para los pedidos
        table_frame = tk.Frame(floating_frame, bg=style.colors["default"])
        table_frame.pack(padx=10, pady=12)

        card = tk.Frame(table_frame, bg=style.colors["default"], bd=2, relief="groove")
        card.pack()

        # Imagen del elemento
        self.left_item_img = tk.PhotoImage(file="assets/img/hamburguesa.png").subsample(6,6)
        img_label = tk.Label(card, image=self.left_item_img, bg=style.colors["default"])
        img_label.pack(side="left", padx=6, pady=6)

        # Contenido del pedido
        item_content = tk.Frame(card, bg=style.colors["default"])
        item_content.pack(side="left", padx=6, pady=6)

        item_title = tk.Label(item_content, text="Hamburguesa", bg=style.colors["default"], fg=style.colors["text"], font=("Helvetica", 12, "bold"))
        item_title.pack(anchor="nw")

        item_list = tk.Frame(item_content, bg=style.colors["default"])
        
        item_list.pack(anchor="nw", pady=(4,0))
        tk.Label(item_list, text="• Pan", bg=style.colors["default"], fg=style.colors["text"]).pack(anchor="w")
        tk.Label(item_list, text="• Carne", bg=style.colors["default"], fg=style.colors["text"]).pack(anchor="w")
        tk.Label(item_list, text="• Lechuga", bg=style.colors["default"], fg=style.colors["text"]).pack(anchor="w")
        tk.Label(item_list, text="• Queso", bg=style.colors["default"], fg=style.colors["text"]).pack(anchor="w")

        # --- Body derecho ---
        right = tk.Frame(main_frame, bg=style.colors["default"])
        right.pack(side="left", fill="both", expand=True)
        
        # Se carga el escenario 1
        escenario = escenarios.getEscenario("E1")
        
        self.bg_image = tk.PhotoImage(file=escenario.fondo)

        # Fondo de la pantalla
        self.bg_label = tk.Label(right, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        rows = len(escenario.layout)
        cols = len(escenario.layout[0])
        size = escenario.tamaño

        # Creamos el Canvas de fondo (grid y colisiones)
        self.canvas_bg = tk.Canvas(right, width=cols*size, height=rows*size, bg="white", highlightthickness=0)
        self.canvas_bg.pack(expand=True)

        # Creamos un Canvas superior para imágenes y elementos dinámicos
        self.canvas_fg = tk.Canvas(right, width=cols*size, height=rows*size, bg=self.canvas_bg['bg'], bd=0, highlightthickness=0)
        self.canvas_fg.place(in_=self.canvas_bg, x=0, y=0)

        # Forzar el fondo por debajo de los canvas
        self.bg_label.lower(self.canvas_bg)

        # Dibujar el Grid en el Canvas
        for r in range(0, len(escenario.layout)):
            for c in range(0, len(escenario.layout[r])):
                x1 = c * size
                y1 = r * size
                x2 = x1 + size
                y2 = y1 + size
                
                # Mantener referencias a las imágenes de bloque para evitar borrarlas
                if not hasattr(self.canvas_fg, 'images'):
                    self.canvas_fg.images = []

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
                    for i in self.mostradores:
                        if i.x == 0 and i.y == 0:
                            i.x = x1
                            i.y = y1
                            break
                    
                elif obj >= 3 and obj <= 6:
                    
                    if obj == 3:
                        tipo = "#916223"
                    elif obj == 4:
                        tipo = "#916224"
                    elif obj == 5:
                        tipo = "#916225"
                    elif obj == 6:
                        tipo = "#916226"
                        
                    block_img = tk.PhotoImage(file=escenario.cajas[obj-3].item.img).subsample(6,6)
                    
                elif obj == 7 or obj == 8 or obj == 9:
                    
                    if obj == 7:
                        tipo = "#d8d8d7"
                    elif obj == 8:
                        tipo = "#d8d8d8"
                    elif obj == 9:
                        tipo = "#d8d8d9"                    
                    
                    block_img = tk.PhotoImage(file=escenario.estaciones[obj-7].img).subsample(5,5)
                    
                self.canvas_bg.create_rectangle(x1, y1, x2, y2, outline="black", fill=tipo)
    
                self.canvas_fg.create_rectangle(x1, y1, x2, y2, outline="black", fill=tipo)
                
                self.canvas_fg.images.append(block_img)
                self.canvas_fg.create_image(x1+size/2, y1+size/2, anchor="center", image=self.canvas_fg.images[-1])

        for x in self.mostradores:
            print(x.name, x.x, x.y)
            mostrador_img = tk.PhotoImage(file="assets/img/nada.png").subsample(8,8)
            self.mostradores_img.append([mostrador_img, self.canvas_fg.create_image(x.x+size/7, x.y, image=mostrador_img, anchor="nw")])

        # Dibujar los jugadores
        
        # Jugador 1
        controller.chef1.posX = escenario.posChef1[0] * size
        controller.chef1.posY = escenario.posChef1[1] * size
        controller.chef1.size = size

        # Cajas de colisión (Canvas de fondo)
        chef1_pos = self.canvas_bg.create_rectangle(
            controller.chef1.posX,
            controller.chef1.posY,
            controller.chef1.posX + size,
            controller.chef1.posY + size,
            fill="blue")

        # Avatar (Canvas Superior)
        chef1_img = tk.PhotoImage(file="assets/img/chef1.png").subsample(6,6)
        self.canvas_fg.chef1_img = chef1_img
        chef1_avatar = self.canvas_fg.create_image(controller.chef1.posX, controller.chef1.posY, anchor="nw", image=chef1_img)

        # Cursor (Canvas inferior)
        chef1_cursor = self.canvas_bg.create_rectangle(
            controller.chef1.posX+size/2-size/8,
            controller.chef1.posY+size/2-size/8,
            controller.chef1.posX + size /2 + size/8,
            controller.chef1.posY + size/2 + size/8,
            fill="red")

        # Item (Canvas superior)
        controller.chef1.item = self.default_item
        self.chef1_item_img = tk.PhotoImage(file=self.default_item.img).subsample(8,8)
        self.chef1_item = self.canvas_fg.create_image(controller.chef1.posX-size/4, controller.chef1.posY-size/4, anchor="nw", image=self.chef1_item_img)
        
        
        # Jugador 2
        controller.chef2.posX = escenario.posChef2[0] * size
        controller.chef2.posY = escenario.posChef2[1] * size
        controller.chef2.size = size

        # Cajas de colisión (Canvas de fondo)
        chef2_pos = self.canvas_bg.create_rectangle(controller.chef2.posX, controller.chef2.posY, controller.chef2.posX + size, controller.chef2.posY + size, fill="purple")
        
        # Avatar (Canvas superior)
        chef2_img = tk.PhotoImage(file="assets/img/chef2.png").subsample(6,6)
        self.canvas_fg.chef2_img = chef2_img
        chef2_avatar = self.canvas_fg.create_image(controller.chef2.posX, controller.chef2.posY, anchor="nw", image=chef2_img)

        # Cursor (Canvas inferior)
        chef2_cursor = self.canvas_bg.create_rectangle(
            controller.chef2.posX+size/2-size/8,
            controller.chef2.posY+size/2-size/8,
            controller.chef2.posX + size /2 + size/8,
            controller.chef2.posY + size/2 + size/8,
            fill="red")

        # Item (Canvas superior)
        controller.chef2.item = self.default_item
        self.chef2_item_img = tk.PhotoImage(file=self.default_item.img).subsample(8,8)
        self.chef2_item = self.canvas_fg.create_image(controller.chef2.posX-size/4, controller.chef2.posY-size/4, anchor="nw", image=self.chef2_item_img)

        def mover(event):
            key = event.keysym
            
            if key == "Escape":
                root.destroy()
                
            if key == "p":
                if self.debug == False:
                    self.canvas_fg.place_forget()
                    self.debug = True
                else:
                    self.canvas_fg.place(relx=0.5, rely=0.5, anchor="center")
                    self.debug = False
            
            if key in controller.chef1.keySet:
                chef = controller.chef1
                chef_pos = chef1_pos
                chef_avatar = chef1_avatar
                chef_cursor = chef1_cursor
                chef_item = self.chef1_item
            
            elif key in controller.chef2.keySet:
                chef = controller.chef2
                chef_pos = chef2_pos
                chef_avatar = chef2_avatar
                chef_cursor = chef2_cursor
                chef_item = self.chef2_item
            
            else:
                return
            
            if key in chef.keySet[:-1]:
                movement = chef.keyEvent(key, self.canvas_bg)
                if movement != [0,0]:
                    self.canvas_bg.move(chef_pos, movement[0], movement[1])
                    
                    self.canvas_fg.move(chef_avatar, movement[0], movement[1])
                    self.canvas_fg.move(chef_item, movement[0], movement[1])
                    self.canvas_bg.move(chef_cursor, movement[0], movement[1])

                # Asegurar las coordenadas absolutas del cursor en el canvas superior
                self.canvas_bg.coords(chef_cursor,
                                chef.posX+size/2-size/8,chef.posY+size/2-size/8, chef.posX + size /2 + size/8, chef.posY + size/2 + size/8)
                
                if chef.direction == "left":
                    self.canvas_bg.move(chef_cursor, - size/2 + size/8, 0)
                elif chef.direction == "right":
                    self.canvas_bg.move(chef_cursor, size/2 - size/8, 0)
                elif chef.direction == "up":
                    self.canvas_bg.move(chef_cursor, 0, - size/2 + size/8)
                elif chef.direction == "down":
                    self.canvas_bg.move(chef_cursor, 0, size/2 - size/8)
                    
            elif key in chef.keySet[-1]:
                
                act = chef.keyEvent(key, self.canvas_bg)
                
                # Animación del cursor
                direction = chef.direction

                if direction == "left":
                    self.canvas_bg.move(chef_cursor,- size/2, 0)
                    self.after(20, lambda: 
                        self.canvas_bg.move(chef_cursor, +size/2, 0)
                        )
                
                elif direction == "right":
                    self.canvas_bg.move(chef_cursor, size/2, 0)
                    self.after(20, lambda: 
                        self.canvas_bg.move(chef_cursor, -size/2, 0)
                        )
                elif direction == "up":
                    self.canvas_bg.move(chef_cursor, 0, - size/2)
                    self.after(20, lambda: 
                        self.canvas_bg.move(chef_cursor, 0, +size/2)
                        )
                elif direction == "down":
                    self.canvas_bg.move(chef_cursor, 0, size/2)
                    self.after(20, lambda: 
                        self.canvas_bg.move(chef_cursor, 0, -size/2)
                        )
                    
                # Se interactuó con el mostrador
                if act == 2:
                    for mostrador in self.mostradores:
                        if mostrador.x == chef.posX and mostrador.y == chef.posY+size:
                            
                            print(mostrador.name)
                            print(chef.item.name, mostrador.item.name, self.default_item.name)
                            if chef.item.name == self.default_item.name:
                                if mostrador.item.name != self.default_item.name:
                                    chef.setItem(mostrador.item)
                                    mostrador.recoger(self.default_item)
                                    self.updateMostradores(self.mostradores, self.mostradores_img, self.canvas_fg)
                                    self.showPlayerItem(chef, chef_item, self.canvas_fg)
                                
                            elif chef.item.name != self.default_item.name:
                                    mostrador.colocar(chef.item)
                                    self.updateMostradores(self.mostradores, self.mostradores_img, self.canvas_fg)
                                    
                                    chef.setItem(self.default_item)
                                    self.showPlayerItem(chef, chef_item, self.canvas_fg)
                    print("CCCC")

                # Se interactuó con una caja
                if act >= 3 and act <= 6:
                    chef.setItem(escenario.cajas[act-3].item)
                    self.showPlayerItem(chef, chef_item, self.canvas_fg)
                    
                    
                
                # Se interactuó con una estación
                if act >= 7 and act <= 9:
                    result = escenario.estaciones[act-7].procesar(chef.item)
                    print("Result:", result)
                    
                    if result != -1:
                        if result != []:
                            chef.setItem(result)
                        else:
                            chef.setItem(self.default_item)
                        self.showPlayerItem(chef, chef_item, self.canvas_fg)
                    else:
                        return

        # Vincular las teclas
        root.bind("<Key>", mover)
        
        # --- Body ---
        
        
        