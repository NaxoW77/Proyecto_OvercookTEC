
# --- Pantalla de juego ---

# Aquí se ejecuta toda la lógica del juego,
# incluyendo cocinas, mostradores y pedidos
# los cuales hay que entregar en tiempo
# y forma adecuadamente.

# Nota: Si se modifica el tamaño normal (256x)
# de las texturas, se debe modificar el subsample
# de cada textura

# Imports necesarios
from assets.classes import tk
from assets.classes import StyledFrame
import random

# Importar escenarios
from assets.classes import EscenarioList
escenarios = EscenarioList()

# Importar clase Item
from assets.classes import Item

# Importar clase Estacion
from assets.classes import Estacion

# Importar clase Mostrador
from assets.classes import Mostrador



# Se define la clase del frame
class GameFrame(StyledFrame):
    def __init__(self, parent, controller, root):
        super().__init__(parent, controller, "white", root) # Se hereda el controlador
        self.root = root
        
        # --- Variables globales ---
        self.debug = False
        
        # Ítem por defecto
        self.default_item = Item("Nada", 1, "assets/img/nada.png")
        
        # Escenario
        self.escenario = None
        
        # Variables globales
        self.tiempo = 0
        
        self.puntaje = 0
        self.puntaje_max = 0
        
        self.pedidos_completados = 0
        self.fase_tiempo = 0 # Dificultad que irá subiendo
        
        self.mostradores = [] # Mostradores
        self.estaciones = [] # Estaciones
        self.estaciones_img = [] # Items en estaciones
        self.mostradores_img = [] # Items en mostradores

        self.pedidos = {} # Pedidos actuales
        self.tiempo_pedido = 0
        
        self.contadores_cocina = []
        
        # Modo Debug (Se puede activar pulsando "p")
        #self.canvas_fg.place_forget()
        
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
        main_frame = tk.Frame(
            self, # Ubicación
            bg="white" # Color
        )
        main_frame.pack(fill="both", expand=True, pady=0)

        # --- Body izquierdo ---
        left = tk.Frame(main_frame, bg="#db9a39", width=400)
        left.pack(side="left", fill="y", padx=0)
        left.pack_propagate(False)

        # Contenedor
        left_container = tk.Frame(left, bg="white", bd=2, relief="raised")
        left_container.pack(padx=8, pady=12, fill="both", expand=True)
    
        self.card_images = []

        # Título
        self.left_title1 = tk.Label(left_container, text="Escenario X", bg="white", fg="#dbd339", font=("Helvetica", 14, "bold"))
        self.left_title1.pack(pady=(12, 6))
        
        # Indicador de tiempo
        self.tiempo_label = tk.Label(left_container, text="Tiempo: X:XX", bg="white", fg="#333333", font=("Helvetica", 12))
        self.tiempo_label.pack(pady=(0, 12))
        
        # Indicador de pedidos completados
        self.pedidos_label = tk.Label(left_container, text="Pedidos completados: X", bg="white", fg="#333333", font=("Helvetica", 12))
        self.pedidos_label.pack(pady=(0, 0))
        
        # Indicador de puntaje total
        self.puntaje_max_label = tk.Label(left_container, text="Puntos totales: X", bg="white", fg="#333333", font=("Helvetica", 12))
        self.puntaje_max_label.pack(pady=(0, 0))
        
        # Indicador de puntaje actual
        self.puntaje_label = tk.Label(left_container, text="Puntos: X", bg="white", fg="#333333", font=("Helvetica", 12))
        self.puntaje_label.pack(pady=(0, 0))

        # Subtítulo
        left_title2 = tk.Label(left_container, text="Pedidos:", bg="white", fg="#dbd339", font=("Helvetica", 14, "bold"))
        left_title2.pack(pady=(12, 2))

        # Tabla para los pedidos
        self.table_frame = tk.Frame(left_container, bg="white")
        self.table_frame.pack(padx=10, pady=6, fill="both", expand=True)

        

        # --- Body derecho ---
        right = tk.Frame(main_frame, bg="white")
        right.pack(side="left", fill="both", expand=True)
        self.right = right # Variable para armar el layout
        
        
        # Función para mostrar mensajes cortos
        def mostrar_mensaje(mensaje, duracion=2000, color="#db9a39"):
            msg_label = tk.Label(right, text=mensaje, bg=color, fg="white", font=("Helvetica", 16, "bold"), relief="raised", bd=2)
            msg_label.place(relx=0.5, rely=0.5, anchor="center")
            
            def eliminar():
                msg_label.destroy()
            
            self.after(duracion, eliminar)


        # Función para quitar un pedido
        def quitar_pedido(pedido):
            if pedido in self.pedidos:
                
                # Cancelar el timer
                if self.pedidos[pedido]['timer_id']:
                    self.after_cancel(self.pedidos[pedido]['timer_id'])
                
                # Eliminar la carta
                self.pedidos[pedido]['widget'].destroy()
                
                # Eliminar de la lista
                del self.pedidos[pedido]
        
        # Guardar instancias
        self.func_mostrar_mensaje = mostrar_mensaje
        self.func_quitar_pedido = quitar_pedido
        
    
    # Función para finalizar el juego
    def game_over(self):
        # Guardar puntajes en el controlador
        self.controller.puntaje_max += self.puntaje_max
        self.controller.pedidos_completados = self.pedidos_completados
        
        self.root.unbind("<Key>")

        for pedido in self.pedidos.values():
            self.after_cancel(pedido['timer_id'])
            
        for contador in self.contadores_cocina:
            self.after_cancel(contador)
            
        self.tiempo = -1

        self.pedidos = {}
        self.tiempo_pedido = 0
        
        self.func_mostrar_mensaje("¡Se acabó el juego!", 3000, "#db9539")
        
        # Función para limpiar las texturas y variables
        def clear():
            self.canvas_bg.destroy()
            self.canvas_fg.destroy()
            
            self.mostradores = []
            self.mostradores_img = []
        
            # Se eliminan los pedidos
            for x in self.table_frame.winfo_children():
                x.destroy()
            
            # Se avanza a los resultados
            self.controller.show_frame("ResultsFrame")
        
        self.after(3000, lambda: clear())
        
        
    # Función para actualizar el frame
    def update_frame(self):
        # Se carga el escenario seleccionado
        self.escenario = self.controller.escenario
        
        # Se inicializan las variables
        self.puntaje = 0
        self.puntaje_max = 0
        self.pedidos_completados = 0
        
        self.tiempo = 300 # Tiempo de partida
        
        self.fase_tiempo = 1 # Fase 1
        
        # Se inicializan las estaciones y mostradores
        self.estaciones = []
        self.mostradores = []
        
        self.estaciones_img = []
        self.mostradores_img = []

        self.pedidos = {}
        self.tiempo_pedido = 0
        
        # Variables temporales
        right = self.right
        mostrar_mensaje = self.func_mostrar_mensaje
        quitar_pedido = self.func_quitar_pedido
        
        # Se carga el fondo
        self.bg_image = tk.PhotoImage(file=self.escenario.fondo)
        self.bg_label = tk.Label(right, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Se cargan los tamaños
        rows = len(self.escenario.layout)
        cols = len(self.escenario.layout[0])
        size = self.escenario.tamaño

        # Creamos el canvas inferior (Grid y colisiones)
        self.canvas_bg = tk.Canvas(right, width=cols*size, height=rows*size, bg="white", highlightthickness=0)
        self.canvas_bg.pack(expand=True)

        # Creamos el canvas superior (Texturas)
        self.canvas_fg = tk.Canvas(right, width=cols*size, height=rows*size, bg=self.canvas_bg['bg'], bd=0, highlightthickness=0)
        self.canvas_fg.place(in_=self.canvas_bg, x=0, y=0)

        # Forzar el fondo por debajo de los canvas
        self.bg_label.lower(self.canvas_bg)

        # Dibujar el grid en el Canvas
        for r in range(0, len(self.escenario.layout)):
            for c in range(0, len(self.escenario.layout[r])):
                
                # Posiciones y tamaños de las celdas
                x1 = c * size
                y1 = r * size
                x2 = x1 + size
                y2 = y1 + size
                
                # Se preservan las texturas
                if not hasattr(self.canvas_fg, 'images'):
                    self.canvas_fg.images = []

                # Variables temporales
                block_img = tk.PhotoImage(file=self.escenario.estaciones[0].img).subsample(9,9)
                tipo = "black"
                
                # Se obtiene el objeto
                obj = self.escenario.layout[r][c]
                
                # Texturas para cada objeto
                # Modificar subsample si se va a cambiar el tamaño (256x)
                if obj == 0: # Suelo
                    tipo = "black"
                    block_img = tk.PhotoImage(file="assets/img/suelo.png").subsample(5,5)
                
                elif obj == 1: # Pared
                    tipo = "red"
                    block_img = tk.PhotoImage(file="assets/img/pared.png").subsample(5,5)
                    
                elif obj == 2: # Mostrador
                    tipo = "green"
                    
                    # Guardar mostradores simples
                    if y2 != len(self.escenario.layout)*size:
                        block_img = tk.PhotoImage(file="assets/img/mostrador.png").subsample(5,5)
                    else:
                        # Guardar mostradores de entregas
                        block_img = tk.PhotoImage(file="assets/img/plato.png").subsample(5,5)
                    
                    # Se guardan las coordenadas
                    self.mostradores.append(Mostrador("Mostrador", self.default_item))
                    
                    self.mostradores[-1].x = x1
                    self.mostradores[-1].y = y1
                        
                
                # Cajas
                elif obj >= 3 and obj <= 6:
                    
                    if obj == 3: # Caja 3
                        tipo = "#916223"
                    elif obj == 4: # Caja 4
                        tipo = "#916224"
                    elif obj == 5: # Caja 5
                        tipo = "#916225"
                    elif obj == 6: # Caja 6
                        tipo = "#916226"
                        
                    block_img = tk.PhotoImage(file=self.escenario.cajas[obj-3].item.img).subsample(6,6)
                    
                    
                    
                # Estaciones
                elif obj == 7 or obj == 8 or obj == 9:
                    
                    if obj == 7: # Estación 7
                        tipo = "#d8d8d7"
                    elif obj == 8: # Estación 8
                        tipo = "#d8d8d8"
                    elif obj == 9: # Estación 9
                        tipo = "#d8d8d9"                    
                    
                    block_img = tk.PhotoImage(file=self.escenario.estaciones[obj-7].img).subsample(5,5)
                    
                    # Se guardan las coordenadas
                    if obj == 8:
                        estc = self.escenario.estaciones[obj-7]
                        self.estaciones.append(Estacion(estc.name, estc.type, estc.ingredients, estc.results, estc.img))
                        
                        self.estaciones[-1].item = self.default_item
                        self.estaciones[-1].x = x1
                        self.estaciones[-1].y = y1
                    
                # Se dibuja el bloque de colisión
                self.canvas_bg.create_rectangle(x1, y1, x2, y2, outline="black", fill=tipo)
    
                # Se dibuja la textura
                self.canvas_fg.create_rectangle(x1, y1, x2, y2, outline="black", fill=tipo)
                
                # Se guarda la textura
                self.canvas_fg.images.append(block_img)
                self.canvas_fg.create_image(x1+size/2, y1+size/2, anchor="center", image=self.canvas_fg.images[-1])

        # Dibujar los items en las estaciones
        for x in self.estaciones:
            estacion_img = tk.PhotoImage(file="assets/img/Nada.png").subsample(8,8)
            self.estaciones_img.append([estacion_img, self.canvas_fg.create_image(x.x+size/7, x.y, image=estacion_img, anchor="nw")])

        # Dibujar los items en los mostradores
        for x in self.mostradores:
            mostrador_img = tk.PhotoImage(file="assets/img/nada.png").subsample(8,8)
            self.mostradores_img.append([mostrador_img, self.canvas_fg.create_image(x.x+size/7, x.y, image=mostrador_img, anchor="nw")])

        # Se dibuja al jugador 1
        self.controller.chef1.posX = self.escenario.posChef1[0] * size
        self.controller.chef1.posY = self.escenario.posChef1[1] * size
        self.controller.chef1.size = size

        # Cajas de colisión (Canvas inferior)
        chef1_pos = self.canvas_bg.create_rectangle(
            self.controller.chef1.posX,
            self.controller.chef1.posY,
            self.controller.chef1.posX + size,
            self.controller.chef1.posY + size,
            fill="blue")

        # Avatar (Canvas superior)
        chef1_img = tk.PhotoImage(file=self.controller.chef1.img).subsample(6,6)
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
        
        
        # Se dibuja al jugador 2
        self.controller.chef2.posX = self.escenario.posChef2[0] * size
        self.controller.chef2.posY = self.escenario.posChef2[1] * size
        self.controller.chef2.size = size

        # Cajas de colisión (Canvas inferior)
        chef2_pos = self.canvas_bg.create_rectangle(self.controller.chef2.posX, self.controller.chef2.posY, self.controller.chef2.posX + size, self.controller.chef2.posY + size, fill="purple")
        
        # Avatar (Canvas superior)
        chef2_img = tk.PhotoImage(file=self.controller.chef2.img).subsample(6,6)
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
        
        
        # Función para verificar si se ha completado una receta
        def verificar_receta():
            
            # Revisar items en mostradores
            items_en_mostradores = []
            for m in self.mostradores:
                if m.y == len(self.escenario.layout)*size-size:
                    items_en_mostradores.append(m.item)
            
            if all(item.name != self.default_item.name for item in items_en_mostradores):
                
                # Obtener los items
                items_names = sorted([item.name for item in items_en_mostradores])
                
                # Revisar coincidencias con recetas en pedidos actuales
                for pedido_id, pedido_data in self.pedidos.items():
                    receta = pedido_data['receta']
                    receta_items = sorted([ing.name for ing in receta.ingredientes])
                    
                    if items_names == receta_items:
                        
                        # Si se encuentra una receta, completar el pedido
                        puntaje_calc = ((pedido_data['time_remaining']*100)/60)*0.30 # Fórmula para puntajes hasta 60s
                        self.puntaje += puntaje_calc
                        self.pedidos_completados += 1
                        
                        self.puntaje_label.config(text=f"Puntaje: {self.puntaje}")
                        self.pedidos_label.config(text=f"Pedidos entregados: {self.pedidos_completados}")
                        
                        # Se actualiza el puntaje maximo
                        if self.puntaje > self.puntaje_max:
                            self.puntaje_max = self.puntaje
                            self.puntaje_max_label.config(text=f"Puntaje máximo: {self.puntaje_max}")
                        
                        # Mostrar mensaje
                        mostrar_mensaje(f"¡Pedido entregado!\n+{puntaje_calc} pts", 1500, "#5cdb39")
                        
                        # Remover el pedido
                        for pedido_id in list(self.pedidos.keys()):
                            quitar_pedido(pedido_id)
                            break
                        
                        # Limpiar mostradores
                        for mostrador in self.mostradores:
                            mostrador.recoger(self.default_item)
                        self.updateSlots()
                        
                        # Generar nuevo pedido
                        generar_pedido()
                        return True
                
                # No se ha completado ninguna receta
                return False
        
        
        # Función para generar un nuevo pedido
        def nuevo_pedido(receta, timer_seconds=random.randint(20, 60)):
            pedido = self.tiempo_pedido
            self.tiempo_pedido += 1
            
            # Contenedor del pedido
            card = tk.Frame(self.table_frame, bg="white", bd=2, relief="groove")
            card.pack(fill="x", padx=5, pady=5)

            # Imagen del pedido
            card_item_img = tk.PhotoImage(file=receta.img).subsample(6,6)
            self.card_images.append(card_item_img)
            
            img_label = tk.Label(card, image=card_item_img, bg="white")
            img_label.pack(side="left", padx=6, pady=6)

            # Contenido del pedido
            item_content = tk.Frame(card, bg="white")
            item_content.pack(side="left", padx=6, pady=3, fill="both", expand=True)

            title_frame = tk.Frame(item_content, bg="white")
            title_frame.pack(fill="x", anchor="nw")

            # Nombre del pedido
            item_title = tk.Label(title_frame, text=receta.name, bg="white", fg="#333333", font=("Helvetica", 10, "bold"), wraplength=200)
            item_title.pack(side="left", anchor="nw", pady=(0, 0))

            # Ingredientes
            item_list = tk.Frame(item_content, bg="white")
            
            # Lista de ingredientes
            for ingrediente in receta.ingredientes:
                tk.Label(item_list, text=" • "+ingrediente.name, bg="white", fg="#333333", font=("Helvetica", 9)).pack(anchor="w")
            
            item_list.pack(anchor="nw", pady=(0, 5))
            
            # Contador
            timer_label = tk.Label(title_frame, text=f"{timer_seconds}s", bg="white", fg="#dbd339", font=("Helvetica", 16, "bold"))
            timer_label.pack(side="right", padx=(10, 0))

            # Propiedades del pedido
            self.pedidos[pedido] = {
                'widget': card,
                'timer_id': None,
                'timer_label': timer_label,
                'time_remaining': timer_seconds,
                'receta': receta
            }
            
            # Función de error
            if len(self.pedidos) > 3:
                self.game_over()

            # Intervalo del contador
            def update_timer():
                # Se actualizan todos los pedidos
                if pedido in self.pedidos:
                    self.pedidos[pedido]['time_remaining'] -= 1
                    remaining = self.pedidos[pedido]['time_remaining']
                    
                    if remaining > 0:
                        timer_label.config(text=f"{remaining}s")
                        self.pedidos[pedido]['timer_id'] = self.after(1000, update_timer) # Función recursiva
                    else:
                        
                        # Si se acaba el tiempo
                        self.puntaje -= 10
                        self.puntaje_label.config(text=f"Puntaje: {self.puntaje}")
                        
                        # Remover el pedido
                        quitar_pedido(pedido)
                
                        # Revisar si se acaba el juego
                        if self.puntaje >= 0:
                            generar_pedido()
                        else:
                            self.puntaje_label.config(text=f"Puntaje: 0")
                            self.game_over() # Función para terminar el juego
                            return
                        
                        # Mostrar mensaje
                        mostrar_mensaje("¡Pedido perdido!\n-10 pts", 1500, "#db3939")

            # Llamada recursiva
            self.pedidos[pedido]['timer_id'] = self.after(1000, update_timer)
        
        
        # Función para generar un nuevo pedido
        def generar_pedido():
            
                # Dificultad según los pedidos completados
                if self.pedidos_completados >= 3:
                    self.fase_tiempo = 2
                    
                if self.pedidos_completados >= 6:
                    self.fase_tiempo = 3
                    
                if self.pedidos_completados >= 9:
                    self.fase_tiempo = 4
                    
                if self.pedidos_completados >= 12:
                    self.fase_tiempo = 5
            
            
                # Fase 1: max 60s | min 55s | pedidos 1
                if self.fase_tiempo == 1:
                    if len(self.pedidos) < 1:
                        receta = self.escenario.recetas[random.randint(0, len(self.escenario.recetas)-1)]
                        nuevo_pedido(receta, 55+random.randint(0, 5))
                        
                # Fase 2: max 50s | min 45s | pedidos 2
                if self.fase_tiempo == 2:
                    if len(self.pedidos) < 2:
                        receta = self.escenario.recetas[random.randint(0, len(self.escenario.recetas)-1)]
                        nuevo_pedido(receta, 45+random.randint(0, 5))
                        
                        if len(self.pedidos) == 1:
                            receta = self.escenario.recetas[random.randint(0, len(self.escenario.recetas)-1)]
                            nuevo_pedido(receta, 45+random.randint(0, 5))
                
                # Fase 3: max 40s | min 30s pedidos 2
                if self.fase_tiempo == 3:
                    if len(self.pedidos) < 2:
                        receta = self.escenario.recetas[random.randint(0, len(self.escenario.recetas)-1)]
                        nuevo_pedido(receta, 30+random.randint(0, 10))
                        
                        if len(self.pedidos) == 1:
                            receta = self.escenario.recetas[random.randint(0, len(self.escenario.recetas)-1)]
                            nuevo_pedido(receta, 30+random.randint(0, 10))
                
                # Fase 4: max 30s | min 25s pedidos 3
                if self.fase_tiempo == 4:
                    if len(self.pedidos) < 3:
                        receta = self.escenario.recetas[random.randint(0, len(self.escenario.recetas)-1)]
                        nuevo_pedido(receta, 25+random.randint(0, 5))
                        
                        if len(self.pedidos) == 1:
                            receta = self.escenario.recetas[random.randint(0, len(self.escenario.recetas)-1)]
                            nuevo_pedido(receta, 25+random.randint(0, 5))
                        
                        if len(self.pedidos) == 2:
                            receta = self.escenario.recetas[random.randint(0, len(self.escenario.recetas)-1)]
                            nuevo_pedido(receta, 25+random.randint(0, 5))
                
                # Fase 5: max 20s | min 15s pedidos 3
                if self.fase_tiempo == 5:
                    if len(self.pedidos) < 3:
                        receta = self.escenario.recetas[random.randint(0, len(self.escenario.recetas)-1)]
                        nuevo_pedido(receta, 15+random.randint(0, 5))
                        
                        if len(self.pedidos) == 1:
                            receta = self.escenario.recetas[random.randint(0, len(self.escenario.recetas)-1)]
                            nuevo_pedido(receta, 15+random.randint(0, 5))
                        
                        if len(self.pedidos) == 2:
                            receta = self.escenario.recetas[random.randint(0, len(self.escenario.recetas)-1)]
                            nuevo_pedido(receta, 15+random.randint(0, 5))


        # Función para mover al jugador
        def mover(event):
            key = event.keysym
            
            # Cerrar el juego
            if key == "Escape":
                self.root.destroy()
                
            # Modo debug (Ocultar las texturas)
            if key == "g":
                if self.debug == False:
                    self.canvas_fg.place_forget()
                    self.debug = True
                else:
                    self.canvas_fg.place(relx=0.5, rely=0.5, anchor="center")
                    self.debug = False
            
            # Si es chef1
            if key in self.controller.chef1.keySet:
                chef = self.controller.chef1
                chef_pos = chef1_pos
                chef_avatar = chef1_avatar
                chef_cursor = chef1_cursor
                chef_item = self.chef1_item
            
            # Si es chef2
            elif key in self.controller.chef2.keySet:
                chef = self.controller.chef2
                chef_pos = chef2_pos
                chef_avatar = chef2_avatar
                chef_cursor = chef2_cursor
                chef_item = self.chef2_item
            
            else:
                return
            
            # Teclas de movimiento
            if key in chef.keySet[:-1]:
                movement = chef.keyEvent(key, self.canvas_bg) # Se llama a calcular el movimiento
                if movement != [0,0]: # Si el movimiento no es 0,0
                    # Se mueven las texturas
                    self.canvas_bg.move(chef_pos, movement[0], movement[1])
                    self.canvas_fg.move(chef_avatar, movement[0], movement[1])
                    self.canvas_fg.move(chef_item, movement[0], movement[1])
                    self.canvas_bg.move(chef_cursor, movement[0], movement[1])

                # Coordenadas absolutas del cursor
                self.canvas_bg.coords(chef_cursor,
                                chef.posX+size/2-size/8,chef.posY+size/2-size/8, chef.posX + size /2 + size/8, chef.posY + size/2 + size/8)
                
                # Animación del cursor
                if chef.direction == "left":
                    self.canvas_bg.move(chef_cursor, - size/2 + size/8, 0)
                elif chef.direction == "right":
                    self.canvas_bg.move(chef_cursor, size/2 - size/8, 0)
                elif chef.direction == "up":
                    self.canvas_bg.move(chef_cursor, 0, - size/2 + size/8)
                elif chef.direction == "down":
                    self.canvas_bg.move(chef_cursor, 0, size/2 - size/8)
            
            
            # Teclas de interacción
            elif key in chef.keySet[-1]:
                
                # Se llama a calcular la interacción
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
                        
                            # Se comparan los items
                            # Si el chef no tiene un item
                            if chef.item.name == self.default_item.name:
                                # Si el mostrador tiene un item
                                if mostrador.item.name != self.default_item.name:
                                    
                                    # Pasar el item del mostrador al chef
                                    chef.setItem(mostrador.item)
                                    mostrador.recoger(self.default_item)
                                    
                                    # Actualizar texturas
                                    self.updateSlots()
                                    self.showPlayerItem(chef, chef_item, self.canvas_fg)
                                
                            # Si el chef tiene un item
                            elif chef.item.name != self.default_item.name:
                                
                                    # Si el mostrador no tiene un item
                                    if mostrador.item.name == self.default_item.name:
                                        
                                        # Pasar el item del chef al mostrador
                                        mostrador.colocar(chef.item)
                                        
                                        # Actualizar texturas
                                        self.updateSlots()
                                        
                                        # Actualizar el chef
                                        chef.setItem(self.default_item)
                                        self.showPlayerItem(chef, chef_item, self.canvas_fg)
                                        
                                        # Revisar si la receta funciona
                                        verificar_receta()
                                            

                # Se interactuó con una caja
                if act >= 3 and act <= 6:
                    
                    # Se pasa el item de la caja al chef
                    chef.setItem(self.escenario.cajas[act-3].item)
                    self.showPlayerItem(chef, chef_item, self.canvas_fg)
                    
        
                # Se interactuó con una estación
                if act >= 7 and act <= 9:
                    
                    if act == 8:
                        for estacion in self.estaciones:
                            
                            # Verificar posiciones
                            if (
                                # Abajo
                                estacion.x ==chef.posX
                                and
                                estacion.y == chef.posY+size
                                
                                ) or (
                                # Arriba
                                estacion.x == chef.posX
                                and
                                estacion.y == chef.posY-size
                                
                                ) or (
                                # Izquierda
                                estacion.x == chef.posX-size
                                and
                                estacion.y == chef.posY
                                
                                ) or (
                                # Derecha
                                estacion.x == chef.posX+size
                                and
                                estacion.y == chef.posY
                                ):
                                
                                if chef.item != self.default_item and estacion.item.name != self.default_item.name:
                                    return
                                
                                # Se calcula el proceso
                                result = estacion.procesar(chef.item, self)
                                
                                # Se actualizan las texturas
                                self.updateSlots()
                                
                                # Si el proceso funcionó y se va a procesar
                                if result == 1:
                                    # Se quita el item del chef
                                    chef.setItem(self.default_item)
                                    self.showPlayerItem(chef, chef_item, self.canvas_fg)
                                    
                                    # Se preparan los callbacks
                                    def quemar(estacion):
                                            estacion.cont_cocina.place_forget()
                                            estacion.item = Item("Quemado", 1, "assets/img/comida_quemada.png")
                                            self.updateSlots()
                                    
                                    def actualiz(estacion):
                                        self.updateSlots()
                                        # Después de otros 3s, se quema
                                        
                                        if estacion.quemarIntv == None and estacion.item.name != "Nada":
                                            estacion.quemarIntv =self.after(3000, lambda: quemar(estacion))
                                
                                    
                                    def contar():
                                        estacion.cont_cocina.config(text=str(int(estacion.cont_cocina.cget("text"))-1))
                                        if int(estacion.cont_cocina.cget("text")) !=0:
                                            self.contadores_cocina.append(self.after(1000, contar))
                                        else:
                                            estacion.cont_cocina.config(text="!!")
                                            
                                    estacion.cont_cocina = tk.Label(self.canvas_fg, text="4", bg="white", fg="black", font=("Arial", 20, "bold"))
                                    estacion.cont_cocina.place(x=estacion.x+size/4, y=estacion.y-size)
                                    contar()        
                                    
                                    
                                    # Después de 2.5s, se da el resultado
                                    if estacion.resultadoIntv == None:
                                        estacion.resultadoIntv = self.after(3000, lambda: actualiz(estacion))
                                    
                                # Si el proceso aún no termina
                                if result == 0:
                                    self.showPlayerItem(chef, chef_item, self.canvas_fg)
                                    return
                                
                                # Si el proceso terminó
                                if isinstance(result, Item):
                                    # Pasar el item de la estación al chef
                                    
                                    if estacion.quemarIntv != None:
                                        self.after_cancel(estacion.quemarIntv)
                                        estacion.cont_cocina.place_forget()
                                        estacion.quemarIntv = None
                                        
                                    if estacion.resultadoIntv != None:
                                        estacion.cont_cocina.place_forget()
                                        estacion.resultadoIntv = None
                                        
                                    chef.setItem(result)
                                    self.showPlayerItem(chef, chef_item, self.canvas_fg)
                                    return
                                return
                        return
                            
                            
                    # Si la estación no es de cocina:        
                    
                    # Calcular el item procesado
                    result = self.escenario.estaciones[act-7].procesar(chef.item, self)
                    
                    
                    # Si el item no es -1 (Hubo proceso)
                    if result != -1:
                        if result != []:
                            # Se pasa el item al chef
                            chef.setItem(result)
                            
                        else: # No hubo proceso
                            # Se quita el item del chef
                            chef.setItem(self.default_item)
                        self.showPlayerItem(chef, chef_item, self.canvas_fg)
                        
                    else:
                        return
        
        # Inicializar la información del juego
        self.left_title1.config(text=f"{self.escenario.name}")
        minutos = self.tiempo/60
        segundos = self.tiempo%60
        self.tiempo_label.config(text=f"Tiempo: {minutos}:{segundos}")
        self.pedidos_label.config(text=f"Pedidos entregados: {self.pedidos_completados}")
        self.puntaje_label.config(text=f"Puntaje: {self.puntaje}")
        self.puntaje_max_label.config(text=f"Puntaje máximo: {self.puntaje_max}")
        
        # Generar el primer pedido
        generar_pedido()
        
        def tiempo_partida():
            self.tiempo -= 1
            minutos = self.tiempo//60
            segundos = self.tiempo%60
            if segundos < 10:
                segundos = f"0{segundos}"
            self.tiempo_label.config(text=f"Tiempo: {minutos}:{segundos}")
            if self.tiempo > 0:
                self.after(1000, tiempo_partida)
            else:
                self.tiempo_label.config(text=f"Tiempo: 0:00")
                self.game_over()
                
        
        tiempo_partida()
        
        # Vincular las teclas
        self.root.bind("<Key>", mover)