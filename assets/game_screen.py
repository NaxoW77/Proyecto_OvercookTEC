
# --- Pantalla de juego ---

# ...

# Imports necesarios
from assets.classes import tk
from assets.classes import ttk
from assets.classes import StyledFrame
import random

# Importar textos
from assets.lang import Lang
lang = Lang().titleScreen # Se necesita únicamente el diccionario de este frame

# Importar estilos
from assets.styles import Style
style = Style()

# Importar escenarios
from assets.data import escenarios
escenarios = escenarios.EscenarioList()

# Importar clase Item
from assets.classes import Item

# Importar clase Estacion
from assets.classes import Mostrador

# Se define la clase del frame
class GameFrame(StyledFrame):
    def __init__(self, parent, controller, root):
        super().__init__(parent, controller, style.colors["default"], root) # Se hereda el controlador
        self.root = root
        
        # --- Variables globales ---
        self.debug = False
        
        self.default_item = Item("Nada", 1, "assets/img/nada.png")
        
        self.mostradores = [
            Mostrador("Mostrador 1", self.default_item),
            Mostrador("Mostrador 2", self.default_item),
            Mostrador("Mostrador 3", self.default_item),
            Mostrador("Mostrador 4", self.default_item)
        ]
        
        self.escenario = None
        
        self.puntaje = 0
        self.puntaje_max = 0
        self.vidas = 0
        
        self.pedidos_completados = 0
        self.fase_tiempo = 0
        
        self.mostradores_img = []

        self.pedidos = {}
        self.tiempo_pedido = 0
        
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
        left = tk.Frame(main_frame, bg=style.colors["game"], width=400)
        left.pack(side="left", fill="y", padx=0)
        left.pack_propagate(False)

        floating_frame = tk.Frame(left, bg=style.colors["default"], bd=2, relief="raised")
        floating_frame.pack(padx=8, pady=12, fill="both", expand=True)
    
        self.card_images = []

        self.left_title1 = tk.Label(floating_frame, text="Escenario X", bg=style.colors["default"], fg=style.colors["main"], font=("Helvetica", 14, "bold"))
        self.left_title1.pack(pady=(12, 6))
        
        self.vidas_label = tk.Label(floating_frame, text="Vidas: X", bg=style.colors["default"], fg=style.colors["text"], font=("Helvetica", 12))
        self.vidas_label.pack(pady=(0, 12))
        
        self.pedidos_label = tk.Label(floating_frame, text="Pedidos completados: X", bg=style.colors["default"], fg=style.colors["text"], font=("Helvetica", 12))
        self.pedidos_label.pack(pady=(0, 0))
        
        self.puntaje_max_label = tk.Label(floating_frame, text="Puntos totales: X", bg=style.colors["default"], fg=style.colors["text"], font=("Helvetica", 12))
        self.puntaje_max_label.pack(pady=(0, 0))
        
        self.puntaje_label = tk.Label(floating_frame, text="Puntos: X", bg=style.colors["default"], fg=style.colors["text"], font=("Helvetica", 12))
        self.puntaje_label.pack(pady=(0, 0))

        left_title2 = tk.Label(floating_frame, text="Pedidos", bg=style.colors["default"], fg=style.colors["main"], font=("Helvetica", 14, "bold"))
        left_title2.pack(pady=(12, 6))

        # Tabla para los pedidos
        self.table_frame = tk.Frame(floating_frame, bg=style.colors["default"])
        self.table_frame.pack(padx=10, pady=12, fill="both", expand=True)

        

        # --- Body derecho ---
        right = tk.Frame(main_frame, bg=style.colors["default"])
        right.pack(side="left", fill="both", expand=True)
        self.right = right  # Store as instance variable for update_frame
        
        def mostrar_mensaje(mensaje, duracion=2000, color=style.colors["game"]):
            msg_label = tk.Label(right, text=mensaje, bg=color, fg="white", font=("Helvetica", 16, "bold"), relief="raised", bd=2)
            msg_label.place(relx=0.5, rely=0.5, anchor="center")
            
            def eliminar():
                msg_label.destroy()
            
            self.after(duracion, eliminar)

        def quitarPedido(pedido):
            if pedido in self.pedidos:
                
                if self.pedidos[pedido]['timer_id']:
                    self.after_cancel(self.pedidos[pedido]['timer_id'])
                
                # Eliminar la carta
                self.pedidos[pedido]['widget'].destroy()
                
                # Eliminar de la lista
                del self.pedidos[pedido]
        
        # Store these functions as instance methods for access in update_frame
        self.mostrar_mensaje_func = mostrar_mensaje
        self.quitarPedido_func = quitarPedido
        
    def game_over(self):
        self.controller.puntaje_max += self.puntaje_max
        self.controller.pedidos_completados = self.pedidos_completados
        
        self.root.unbind("<Key>")

        for pedido in self.pedidos.values():
            self.after_cancel(pedido['timer_id'])

        self.pedidos = {}
        self.tiempo_pedido = 0
        
        self.mostrar_mensaje_func("¡Has perdido!", 3000, style.colors["fail"])
        
        def clear():
            self.canvas_bg.destroy()
            self.canvas_fg.destroy()
            
            self.mostradores = [
                Mostrador("Mostrador 1", self.default_item),
                Mostrador("Mostrador 2", self.default_item),
                Mostrador("Mostrador 3", self.default_item),
                Mostrador("Mostrador 4", self.default_item)
            ]
            self.mostradores_img = []
        
            for x in self.table_frame.winfo_children():
                x.destroy()
            
            self.controller.show_frame("ResultsFrame")
        
        self.after(3000, lambda: clear())
        
    def update_frame(self):
        # Se carga el escenario
        self.escenario = self.controller.escenario
        
        self.puntaje = 0
        self.puntaje_max = 0
        self.vidas = 5
        
        self.pedidos_completados = 0
        self.fase_tiempo = 5
        
        self.mostradores = [
            Mostrador("Mostrador 1", self.default_item),
            Mostrador("Mostrador 2", self.default_item),
            Mostrador("Mostrador 3", self.default_item),
            Mostrador("Mostrador 4", self.default_item)
        ]
        
        self.mostradores_img = []

        self.pedidos = {}
        self.tiempo_pedido = 0
        
        right = self.right
        mostrar_mensaje = self.mostrar_mensaje_func
        quitarPedido = self.quitarPedido_func
        
        # --- Setup del canvas y elementos del juego ---
        
        self.bg_image = tk.PhotoImage(file=self.escenario.fondo)

        # Fondo de la pantalla
        self.bg_label = tk.Label(right, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        rows = len(self.escenario.layout)
        cols = len(self.escenario.layout[0])
        size = self.escenario.tamaño

        # Creamos el Canvas de fondo (grid y colisiones)
        self.canvas_bg = tk.Canvas(right, width=cols*size, height=rows*size, bg="white", highlightthickness=0)
        self.canvas_bg.pack(expand=True)

        # Creamos un Canvas superior para imágenes y elementos dinámicos
        self.canvas_fg = tk.Canvas(right, width=cols*size, height=rows*size, bg=self.canvas_bg['bg'], bd=0, highlightthickness=0)
        self.canvas_fg.place(in_=self.canvas_bg, x=0, y=0)

        # Forzar el fondo por debajo de los canvas
        self.bg_label.lower(self.canvas_bg)

        # Dibujar el Grid en el Canvas
        for r in range(0, len(self.escenario.layout)):
            for c in range(0, len(self.escenario.layout[r])):
                x1 = c * size
                y1 = r * size
                x2 = x1 + size
                y2 = y1 + size
                
                # Mantener referencias a las imágenes de bloque para evitar borrarlas
                if not hasattr(self.canvas_fg, 'images'):
                    self.canvas_fg.images = []

                block_img = tk.PhotoImage(file=self.escenario.estaciones[0].img).subsample(9,9)
                tipo = "black"
                
                obj = self.escenario.layout[r][c]
                
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
                        
                    block_img = tk.PhotoImage(file=self.escenario.cajas[obj-3].item.img).subsample(6,6)
                    
                elif obj == 7 or obj == 8 or obj == 9:
                    
                    if obj == 7:
                        tipo = "#d8d8d7"
                    elif obj == 8:
                        tipo = "#d8d8d8"
                    elif obj == 9:
                        tipo = "#d8d8d9"                    
                    
                    block_img = tk.PhotoImage(file=self.escenario.estaciones[obj-7].img).subsample(5,5)
                    
                self.canvas_bg.create_rectangle(x1, y1, x2, y2, outline="black", fill=tipo)
    
                self.canvas_fg.create_rectangle(x1, y1, x2, y2, outline="black", fill=tipo)
                
                self.canvas_fg.images.append(block_img)
                self.canvas_fg.create_image(x1+size/2, y1+size/2, anchor="center", image=self.canvas_fg.images[-1])

        for x in self.mostradores:
            mostrador_img = tk.PhotoImage(file="assets/img/nada.png").subsample(8,8)
            self.mostradores_img.append([mostrador_img, self.canvas_fg.create_image(x.x+size/7, x.y, image=mostrador_img, anchor="nw")])

        # Dibujar los jugadores
        
        # Jugador 1
        self.controller.chef1.posX = self.escenario.posChef1[0] * size
        self.controller.chef1.posY = self.escenario.posChef1[1] * size
        self.controller.chef1.size = size

        # Cajas de colisión (Canvas de fondo)
        chef1_pos = self.canvas_bg.create_rectangle(
            self.controller.chef1.posX,
            self.controller.chef1.posY,
            self.controller.chef1.posX + size,
            self.controller.chef1.posY + size,
            fill="blue")

        # Avatar (Canvas Superior)
        chef1_img = tk.PhotoImage(file="assets/img/chef1.png").subsample(6,6)
        self.canvas_fg.chef1_img = chef1_img
        chef1_avatar = self.canvas_fg.create_image(self.controller.chef1.posX, self.controller.chef1.posY, anchor="nw", image=chef1_img)

        # Cursor (Canvas inferior)
        chef1_cursor = self.canvas_bg.create_rectangle(
            self.controller.chef1.posX+size/2-size/8,
            self.controller.chef1.posY+size/2-size/8,
            self.controller.chef1.posX + size /2 + size/8,
            self.controller.chef1.posY + size/2 + size/8,
            fill="red")

        # Item (Canvas superior)
        self.controller.chef1.item = self.default_item
        self.chef1_item_img = tk.PhotoImage(file=self.default_item.img).subsample(8,8)
        self.chef1_item = self.canvas_fg.create_image(self.controller.chef1.posX-size/4, self.controller.chef1.posY-size/4, anchor="nw", image=self.chef1_item_img)
        
        
        # Jugador 2
        self.controller.chef2.posX = self.escenario.posChef2[0] * size
        self.controller.chef2.posY = self.escenario.posChef2[1] * size
        self.controller.chef2.size = size

        # Cajas de colisión (Canvas de fondo)
        chef2_pos = self.canvas_bg.create_rectangle(self.controller.chef2.posX, self.controller.chef2.posY, self.controller.chef2.posX + size, self.controller.chef2.posY + size, fill="purple")
        
        # Avatar (Canvas superior)
        chef2_img = tk.PhotoImage(file="assets/img/chef2.png").subsample(6,6)
        self.canvas_fg.chef2_img = chef2_img
        chef2_avatar = self.canvas_fg.create_image(self.controller.chef2.posX, self.controller.chef2.posY, anchor="nw", image=chef2_img)

        # Cursor (Canvas inferior)
        chef2_cursor = self.canvas_bg.create_rectangle(
            self.controller.chef2.posX+size/2-size/8,
            self.controller.chef2.posY+size/2-size/8,
            self.controller.chef2.posX + size /2 + size/8,
            self.controller.chef2.posY + size/2 + size/8,
            fill="red")

        # Item (Canvas superior)
        self.controller.chef2.item = self.default_item
        self.chef2_item_img = tk.PhotoImage(file=self.default_item.img).subsample(8,8)
        self.chef2_item = self.canvas_fg.create_image(self.controller.chef2.posX-size/4, self.controller.chef2.posY-size/4, anchor="nw", image=self.chef2_item_img)
        
        # --- Scenario-dependent functions ---
        
        def verificar_receta():
            
            # Revisar items en mostradores
            items_en_mostradores = [m.item for m in self.mostradores]
            
            if all(item.name != self.default_item.name for item in items_en_mostradores):
                
                # Obtener los items
                items_names = sorted([item.name for item in items_en_mostradores])
                
                # Revisar solo las recetas en pedidos actuales
                for pedido_id, pedido_data in self.pedidos.items():
                    receta = pedido_data['receta']
                    receta_items = sorted([ing.name for ing in receta.ingredientes])
                    
                    if items_names == receta_items:
                        
                        # Si se encuentra una receta, completar el pedido
                        self.puntaje += 25
                        self.pedidos_completados += 1
                        
                        self.puntaje_label.config(text=f"Puntaje: {self.puntaje}")
                        self.pedidos_label.config(text=f"Pedidos entregados: {self.pedidos_completados}")
                        
                        if self.puntaje > self.puntaje_max:
                            self.puntaje_max = self.puntaje
                            self.puntaje_max_label.config(text=f"Puntaje máximo: {self.puntaje_max}")
                            
                        mostrar_mensaje(f"¡Pedido entregado!\n+25 pts", 1500, style.colors["correct"])
                        
                        # Remover el pedido
                        for pedido_id in list(self.pedidos.keys()):
                            quitarPedido(pedido_id)
                            break
                        
                        # Limpiar mostradores
                        for mostrador in self.mostradores:
                            mostrador.recoger(self.default_item)
                        self.updateMostradores(self.mostradores, self.mostradores_img, self.canvas_fg)
                        
                        generarPedido()
                        return True
                
                return False
        
        def nuevoPedido(receta, timer_seconds=random.randint(20, 60)):
            pedido = self.tiempo_pedido
            self.tiempo_pedido += 1
            
            card = tk.Frame(self.table_frame, bg=style.colors["default"], bd=2, relief="groove")
            card.pack(fill="x", padx=5, pady=5)

            # Imagen del elemento
            card_item_img = tk.PhotoImage(file=receta.img).subsample(6,6)
            self.card_images.append(card_item_img)
            
            img_label = tk.Label(card, image=card_item_img, bg=style.colors["default"])
            img_label.pack(side="left", padx=6, pady=6)

            # Contenido del pedido
            item_content = tk.Frame(card, bg=style.colors["default"])
            item_content.pack(side="left", padx=6, pady=6, fill="both", expand=True)

            title_frame = tk.Frame(item_content, bg=style.colors["default"])
            title_frame.pack(fill="x", anchor="nw")

            item_title = tk.Label(title_frame, text=receta.name, bg=style.colors["default"], fg=style.colors["text"], font=("Helvetica", 12, "bold"), wraplength=200)
            item_title.pack(side="left", anchor="nw")

            # Contador
            timer_label = tk.Label(title_frame, text=f"{timer_seconds}s", bg=style.colors["default"], fg=style.colors["main"], font=("Helvetica", 20, "bold"))
            timer_label.pack(side="right", padx=(10, 0))

            item_list = tk.Frame(item_content, bg=style.colors["default"])
            
            for ingrediente in receta.ingredientes:
                tk.Label(item_list, text=" • "+ingrediente.name, bg=style.colors["default"], fg=style.colors["text"]).pack(anchor="w")
            
            item_list.pack(anchor="nw")

            # Propiedades del pedido
            self.pedidos[pedido] = {
                'widget': card,
                'timer_id': None,
                'timer_label': timer_label,
                'time_remaining': timer_seconds,
                'receta': receta
            }
            
            if len(self.pedidos) > 3:
                self.game_over()

            # Contador
            def update_timer():
                if pedido in self.pedidos:
                    self.pedidos[pedido]['time_remaining'] -= 1
                    remaining = self.pedidos[pedido]['time_remaining']
                    
                    if remaining > 0:
                        timer_label.config(text=f"{remaining}s")
                        self.pedidos[pedido]['timer_id'] = self.after(1000, update_timer)
                    else:
                        
                        # Si se acaba el tiempo
                        self.puntaje -= 10
                        if self.puntaje < 0:
                            self.puntaje = 0
                        self.vidas -= 1
                        self.puntaje_label.config(text=f"Puntaje: {self.puntaje}")
                        self.vidas_label.config(text=f"Vidas: {self.vidas}")
                        
                        quitarPedido(pedido)
                
                        if self.vidas > 0:
                            generarPedido()
                        else:
                            self.game_over()
                            return
                        
                        mostrar_mensaje("¡Pedido perdido!\n-10 pts", 1500, style.colors["fail"])

            self.pedidos[pedido]['timer_id'] = self.after(1000, update_timer)
        
        def generarPedido():
                if self.pedidos_completados >= 3:
                    self.fase_tiempo = 2
                    
                if self.pedidos_completados >= 6:
                    self.fase_tiempo = 3
                    
                if self.pedidos_completados >= 9:
                    self.fase_tiempo = 4
                    
                if self.pedidos_completados >= 12:
                    self.fase_tiempo = 5
            
                # Fase 1: max 60 | min 55 | pedidos 1
                if self.fase_tiempo == 1:
                    if len(self.pedidos) < 1:
                        receta = self.escenario.recetas[random.randint(0, len(self.escenario.recetas)-1)]
                        nuevoPedido(receta, 55+random.randint(0, 5))
                        
                # Fase 2: max 50 | min 45 | pedidos 2
                if self.fase_tiempo == 2:
                    if len(self.pedidos) < 2:
                        receta = self.escenario.recetas[random.randint(0, len(self.escenario.recetas)-1)]
                        nuevoPedido(receta, 45+random.randint(0, 5))
                        
                        if len(self.pedidos) == 1:
                            receta = self.escenario.recetas[random.randint(0, len(self.escenario.recetas)-1)]
                            nuevoPedido(receta, 45+random.randint(0, 5))
                
                # Fase 3: max 40 | min 30 pedidos 2
                if self.fase_tiempo == 3:
                    if len(self.pedidos) < 2:
                        receta = self.escenario.recetas[random.randint(0, len(self.escenario.recetas)-1)]
                        nuevoPedido(receta, 30+random.randint(0, 10))
                        
                        if len(self.pedidos) == 1:
                            receta = self.escenario.recetas[random.randint(0, len(self.escenario.recetas)-1)]
                            nuevoPedido(receta, 30+random.randint(0, 10))
                
                # Fase 4: max 30 | min 25 pedidos 3
                if self.fase_tiempo == 4:
                    if len(self.pedidos) < 3:
                        receta = self.escenario.recetas[random.randint(0, len(self.escenario.recetas)-1)]
                        nuevoPedido(receta, 25+random.randint(0, 5))
                        
                        if len(self.pedidos) == 1:
                            receta = self.escenario.recetas[random.randint(0, len(self.escenario.recetas)-1)]
                            nuevoPedido(receta, 25+random.randint(0, 5))
                        
                        if len(self.pedidos) == 2:
                            receta = self.escenario.recetas[random.randint(0, len(self.escenario.recetas)-1)]
                            nuevoPedido(receta, 25+random.randint(0, 5))
                
                # Fase 5: max 20 | min 15 pedidos 3
                if self.fase_tiempo == 5:
                    if len(self.pedidos) < 3:
                        receta = self.escenario.recetas[random.randint(0, len(self.escenario.recetas)-1)]
                        nuevoPedido(receta, 15+random.randint(0, 5))
                        
                        if len(self.pedidos) == 1:
                            receta = self.escenario.recetas[random.randint(0, len(self.escenario.recetas)-1)]
                            nuevoPedido(receta, 15+random.randint(0, 5))
                        
                        if len(self.pedidos) == 2:
                            receta = self.escenario.recetas[random.randint(0, len(self.escenario.recetas)-1)]
                            nuevoPedido(receta, 15+random.randint(0, 5))

        def mover(event):
            key = event.keysym
            
            if key == "Escape":
                self.root.destroy()
                
            if key == "p":
                if self.debug == False:
                    self.canvas_fg.place_forget()
                    self.debug = True
                else:
                    self.canvas_fg.place(relx=0.5, rely=0.5, anchor="center")
                    self.debug = False
            
            if key in self.controller.chef1.keySet:
                chef = self.controller.chef1
                chef_pos = chef1_pos
                chef_avatar = chef1_avatar
                chef_cursor = chef1_cursor
                chef_item = self.chef1_item
            
            elif key in self.controller.chef2.keySet:
                chef = self.controller.chef2
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

                # Coordenadas absolutas del cursor
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
                        
                        # Verificar posiciones
                        if (
                            # Abajo
                            mostrador.x ==chef.posX
                            and
                            mostrador.y == chef.posY+size
                            
                            ) or (
                            # Arriba
                            mostrador.x == chef.posX
                            and
                            mostrador.y == chef.posY-size
                            
                            ) or (
                            # Izquierda
                            mostrador.x == chef.posX-size
                            and
                            mostrador.y == chef.posY
                            
                            ) or (
                            # Derecha
                            mostrador.x == chef.posX+size
                            and
                            mostrador.y == chef.posY
                            ):
                        
                            if chef.item.name == self.default_item.name:
                                if mostrador.item.name != self.default_item.name:
                                    chef.setItem(mostrador.item)
                                    mostrador.recoger(self.default_item)
                                    self.updateMostradores(self.mostradores, self.mostradores_img, self.canvas_fg)
                                    self.showPlayerItem(chef, chef_item, self.canvas_fg)
                                
                            elif chef.item.name != self.default_item.name:
                                    if mostrador.item.name == self.default_item.name:
                                        mostrador.colocar(chef.item)
                                        self.updateMostradores(self.mostradores, self.mostradores_img, self.canvas_fg)
                                        
                                        chef.setItem(self.default_item)
                                        self.showPlayerItem(chef, chef_item, self.canvas_fg)
                                        
                                        # Revisar si la receta funciona
                                        verificar_receta()
                                            

                # Se interactuó con una caja
                if act >= 3 and act <= 6:
                    chef.setItem(self.escenario.cajas[act-3].item)
                    self.showPlayerItem(chef, chef_item, self.canvas_fg)
                    
                    
                
                # Se interactuó con una estación
                if act >= 7 and act <= 9:
                    
                    result = self.escenario.estaciones[act-7].procesar(chef.item)
                    
                    if result != -1:
                        if result != []:
                            chef.setItem(result)
                        else:
                            chef.setItem(self.default_item)
                        self.showPlayerItem(chef, chef_item, self.canvas_fg)
                    else:
                        return
        
        # Inicializar el juego
        self.left_title1.config(text=f"Escenario: {self.escenario.name}")
        self.vidas_label.config(text=f"Vidas: {self.vidas}")
        self.pedidos_label.config(text=f"Pedidos entregados: {self.pedidos_completados}")
        self.puntaje_label.config(text=f"Puntaje: {self.puntaje}")
        self.puntaje_max_label.config(text=f"Puntaje máximo: {self.puntaje_max}")
        
        generarPedido()
        
        # Vincular las teclas
        self.root.bind("<Key>", mover)
        
        
        